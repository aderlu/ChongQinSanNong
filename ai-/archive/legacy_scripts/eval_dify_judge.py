"""
Dify 公司模型诊断 vs 黄金标准诊断 对比评估
用已有的高分数据做标准答案（gold standard），对比 Dify 模型输出
流程: user_query -> Dify (盲诊) -> 提取诊断/处方 -> 与标准诊断对比

对比方式:
  1. 规则层: 疾病名称匹配、关键词覆盖、药品重叠度、结构完整性
  2. 语义层: 对差异大的 case 用 LLM 做深度诊断比对
"""
import csv, time, json, os, re, hashlib, random
import requests
from datetime import datetime
from collections import defaultdict
from typing import Optional, Dict, Any, Tuple
from difflib import SequenceMatcher

# ============ 配置 ============
DIFY_BASE_URL = 'https://dify.amdu.dtyunxi.cn/v1'
DIFY_COMPANY_KEY = 'app-lh3ByE1G9M0PIU4c2509iG1Y'
LLM_BASE_URL = 'https://api.nonelinear.com/v1'

LLM_API_KEYS = {
    'deepseek-v3.2': 'sk-2aee4f263dad2d98046bb67515e900c0',
    'gpt-5.5-low': 'sk-2aee4f263dad2d98046bb67515e900c0',
}

INPUT_FILE = 'D:/projects/鸡病数据合成系统/results/chicken_disease_dataset_production_20260429_220628.csv'
SAMPLE_SIZE = 50
RANDOM_SEED = 42
TOP_SCORE_ONLY = True          # 只从高分段（>=80分）抽样作为黄金标准
TOP_SCORE_THRESHOLD = 80       # 高分阈值

TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_DIR = f'results/dify_vs_gold_{TIMESTAMP}'
os.makedirs(OUTPUT_DIR, exist_ok=True)
RESULT_FILE = f'{OUTPUT_DIR}/dify_comparison_results.csv'
SUMMARY_FILE = f'{OUTPUT_DIR}/dify_comparison_summary.csv'
SAMPLED_FILE = f'{OUTPUT_DIR}/sampled_cases.csv'
DEEP_EVAL_FILE = f'{OUTPUT_DIR}/deep_eval_cases.csv'

FIELDNAMES = [
    'case_id', 'disease_name', 'gold_score', 'success', 'error',
    'user_query',
    'gold_diagnosis_excerpt', 'dify_diagnosis_excerpt',
    'gold_prescription_excerpt', 'dify_prescription_excerpt',
    'primary_disease_match', 'gold_diseases', 'dify_diseases',
    'disease_jaccard', 'diagnosis_similarity', 'drug_jaccard',
    'gold_drugs', 'dify_drugs',
    'gold_structured', 'dify_structured', 'term_coverage',
    'overall_match_score',
    'deep_missed_findings', 'deep_extra_findings', 'deep_prescription_issues',
    'deep_quality', 'deep_score', 'deep_accept',
]

# ============ 疾病名称与药品知识库 ============

# 常见鸡病列表（用于名称匹配）
CHICKEN_DISEASES = [
    '新城疫', '禽流感', '传染性法氏囊病', '马立克氏病', '鸡传染性贫血',
    '鸡白痢', '沙门氏菌', '大肠杆菌病', '坏死性肠炎', '球虫病',
    '盲肠球虫', '小肠球虫', '慢性呼吸道病', '支原体', '滑液囊支原体',
    '传染性支气管炎', '传染性喉气管炎', '禽霍乱', '巴氏杆菌',
    '鸡痘', '脑脊髓炎', '腺胃炎', '肌胃炎', '腺肌胃炎',
    '霉菌毒素中毒', '痛风', '脂肪肝综合征', '腹水综合征',
    '中暑', '应激', '啄癖', '维生素缺乏', '盲肠肝炎',
    '组织滴虫', '鼻炎', '传染性鼻炎', '弯曲杆菌', '鼻气管鸟杆菌',
]

# 常见兽药关键词
VET_DRUG_KEYWORDS = [
    '氟苯尼考', '多西环素', '恩诺沙星', '阿莫西林', '头孢', '庆大霉素',
    '卡那霉素', '新霉素', '黏杆菌素', '黏菌素', '林可霉素', '壮观霉素',
    '泰妙菌素', '泰乐菌素', '替米考星', '沃尼妙林', '磺胺', '甲氧苄啶',
    '二甲硝唑', '地美硝唑', '妥曲珠利', '地克珠利', '莫能菌素', '盐霉素',
    '马杜霉素', '那拉菌素', '尼卡巴嗪', '氯羟吡啶', '氨丙啉',
    '维生素', '电解多维', '鱼肝油', '黄芪多糖', '清瘟解毒', '荆防败毒',
    '双黄连', '穿心莲', '板蓝根', '大青叶', '鱼腥草', '金银花',
    '聚维酮碘', '戊二醛', '过氧乙酸',
]


# ============ 黄金标准数据 ============

def filter_high_quality(cases: list[dict], threshold: int = 80) -> list[dict]:
    """筛选高分数据作为黄金标准"""
    filtered = [c for c in cases if float(c.get('final_total_score', 0) or 0) >= threshold]
    print(f"    高分数据 (总分>={threshold}): {len(filtered)}/{len(cases)} 条")
    return filtered


def stratified_sample(cases: list[dict], n: int) -> list[dict]:
    """分层抽样: 保证15种疾病全覆盖 + 均匀分布"""
    random.seed(RANDOM_SEED)

    by_disease = defaultdict(list)
    for c in cases:
        by_disease[c.get('disease_name', '未知')].append(c)

    diseases = list(by_disease.keys())
    selected = []
    selected_ids = set()

    # 第一轮: 每种病至少抽2条
    per_disease_base = max(2, n // len(diseases) // 3)
    for d in diseases:
        pool = sorted(by_disease[d], key=lambda x: float(x.get('final_total_score') or 100), reverse=True)
        take = min(per_disease_base, len(pool))
        for c in pool[:take]:
            cid = c.get('case_id', '') or c.get('user_query', '')[:40]
            if cid not in selected_ids:
                selected.append(c)
                selected_ids.add(cid)

    # 第二轮: 补满
    if len(selected) < n:
        remaining = n - len(selected)
        leftover = [c for c in cases if (c.get('case_id', '') or c.get('user_query', '')[:40]) not in selected_ids]
        random.shuffle(leftover)
        for c in leftover[:remaining]:
            cid = c.get('case_id', '') or c.get('user_query', '')[:40]
            if cid not in selected_ids:
                selected.append(c)
                selected_ids.add(cid)

    random.shuffle(selected)
    print(f"分层抽样完成: 共 {len(selected)} 条 (目标 {n})")
    dist = defaultdict(int)
    for c in selected:
        dist[c.get('disease_name', '未知')] += 1
    for d in sorted(dist):
        print(f"  {d}: {dist[d]}条")
    score_avg = sum(float(c.get('final_total_score') or 0) for c in selected) / len(selected)
    print(f"  样本平均分: {score_avg:.1f}")
    return selected


# ============ Dify 调用 ============

def dify_diagnose(user_query: str, timeout: int = 180) -> Dict[str, Any]:
    """调用 Dify API，超时后重试一次"""
    for attempt in range(2):
        try:
            resp = requests.post(
                f'{DIFY_BASE_URL}/chat-messages',
                headers={'Authorization': f'Bearer {DIFY_COMPANY_KEY}', 'Content-Type': 'application/json'},
                json={'query': user_query, 'inputs': {'pop_num': '500'}, 'response_mode': 'blocking', 'user': 'eval-system'},
                timeout=timeout
            )
            if resp.status_code == 200:
                return {'success': True, 'answer': resp.json().get('answer', '')}
            return {'success': False, 'error': f'HTTP {resp.status_code}'}
        except Exception as e:
            if attempt == 0:
                print(f"    - 重试 (原因: {type(e).__name__})")
                time.sleep(2)
                continue
            return {'success': False, 'error': str(e)}


def extract_diagnosis_and_prescription(answer: str) -> Tuple[str, str]:
    """从公司模型返回中提取诊断和处方"""
    diagnosis = ""
    prescription = ""

    brief_match = re.search(r'(.*?)(?=```处理建议|处理建议)', answer, re.DOTALL)
    if brief_match:
        diagnosis = brief_match.group(1).strip()

    diag_list_match = re.search(r'```诊断结果\s*(.*?)```', answer, re.DOTALL)
    if diag_list_match:
        diagnosis = (diagnosis + "\n" + diag_list_match.group(1)).strip()

    rx_match = re.search(r'```处理建议\s*(.*?)```', answer, re.DOTALL)
    if rx_match:
        prescription = rx_match.group(1).strip()
    else:
        rx_section = re.search(r'处理建议[：:]*\s*\n*(.*)', answer, re.DOTALL)
        if rx_section:
            prescription = rx_section.group(1).strip()[:2000]

    return diagnosis, prescription


# ============ 对比分析层 ============

def extract_disease_name(text: str) -> list[str]:
    """从诊断文本中提取提到的疾病名称"""
    found = []
    for disease in CHICKEN_DISEASES:
        if disease in text:
            found.append(disease)
    return found


def extract_drug_names(text: str) -> list[str]:
    """从文本中提取药品名称"""
    found = []
    for drug in VET_DRUG_KEYWORDS:
        if drug in text:
            found.append(drug)
    return found


def extract_primary_diagnosis(text: str) -> str:
    """提取主要诊断（取"主要诊断："后面的内容）"""
    m = re.search(r'主要诊断[：:]\s*(.*?)(?:[。\n]|鉴别诊断)', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # 没找到则取疾病名
    diseases = extract_disease_name(text)
    return diseases[0] if diseases else ""


def jaccard_similarity(set1: set, set2: set) -> float:
    """Jaccard 相似度"""
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / len(set1 | set2)


def text_similarity(text1: str, text2: str) -> float:
    """文本相似度 (SequenceMatcher)"""
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, text1[:1000], text2[:1000]).ratio()


def has_structured_output(text: str) -> bool:
    """检查是否有结构化输出格式（如```代码块、编号列表等）"""
    checks = [
        bool(re.search(r'```(?:诊断结果|处理建议)', text)),
        bool(re.search(r'(?:^|\n)\s*[1-9]', text)),
        bool(re.search(r'处理建议', text)),
        bool(re.search(r'诊断', text)),
    ]
    return sum(checks) >= 2


def compare_diagnosis_vs_gold(
    gold_diagnosis: str,
    gold_prescription: str,
    gold_disease: str,
    dify_diagnosis: str,
    dify_prescription: str,
) -> Dict[str, Any]:
    """
    将 Dify 诊断与黄金标准进行全面对比。
    返回各维度匹配度分数 (0-100)。
    """
    # ---- 1. 疾病名称匹配 ----
    gold_diseases = set(extract_disease_name(gold_diagnosis))
    dify_diseases = set(extract_disease_name(dify_diagnosis))
    disease_jaccard = round(jaccard_similarity(gold_diseases, dify_diseases) * 100, 1)
    gold_primary = extract_primary_diagnosis(gold_diagnosis)
    dify_primary = extract_primary_diagnosis(dify_diagnosis)
    primary_match = gold_primary and dify_primary and (
        gold_primary[:10] in dify_primary or dify_primary[:10] in gold_primary
    )

    # ---- 2. 诊断文本相似度 ----
    diag_similarity = round(text_similarity(gold_diagnosis, dify_diagnosis) * 100, 1)

    # ---- 3. 药品匹配 ----
    gold_drugs = set(extract_drug_names(gold_prescription))
    dify_drugs = set(extract_drug_names(dify_prescription))
    drug_jaccard = round(jaccard_similarity(gold_drugs, dify_drugs) * 100, 1)

    # ---- 4. 结构化输出 ----
    gold_structured = has_structured_output(gold_diagnosis)
    dify_structured = has_structured_output(dify_diagnosis)

    # ---- 5. 关键术语覆盖 ----
    key_terms = ['诊断', '鉴别诊断', '病理逻辑', '处理建议', '休药期']
    gold_terms = sum(1 for t in key_terms if t in gold_diagnosis + gold_prescription)
    dify_terms = sum(1 for t in key_terms if t in dify_diagnosis + dify_prescription)
    term_coverage = round(min(dify_terms / max(gold_terms, 1), 1.0) * 100, 1)

    # ---- 6. 综合评分（加权） ----
    overall_match = round(
        disease_jaccard * 0.35 +        # 疾病匹配权重最高
        diag_similarity * 0.20 +         # 诊断文本相似度
        drug_jaccard * 0.25 +            # 处方一致性
        term_coverage * 0.20,            # 关键术语覆盖
        1
    )

    return {
        'gold_diseases': '、'.join(sorted(gold_diseases)) if gold_diseases else gold_disease,
        'dify_diseases': '、'.join(sorted(dify_diseases)) if dify_diseases else '',
        'gold_disease_primary': gold_primary[:80],
        'dify_disease_primary': dify_primary[:80],
        'primary_disease_match': primary_match,
        'disease_jaccard': disease_jaccard,
        'gold_drugs': '、'.join(sorted(gold_drugs)),
        'dify_drugs': '、'.join(sorted(dify_drugs)),
        'drug_jaccard': drug_jaccard,
        'diagnosis_similarity': diag_similarity,
        'gold_structured': gold_structured,
        'dify_structured': dify_structured,
        'term_coverage': term_coverage,
        'overall_match_score': overall_match,
    }


# ============ LLM 深度评估（仅对差异大的 case） ============

from openai import OpenAI as OAI

DEEP_EVAL_PROMPT = """你是鸡病诊断质量评估专家，负责对比 Dify 模型诊断与黄金标准诊断的差异。

请严格只输出 JSON（不要多余文字），schema 如下：
{{
  "dify_missed_key_findings": "Dify 遗漏了哪些黄金标准中的关键发现，用极短中文短语概括。无遗漏写'无'",
  "dify_extra_findings": "Dify 额外提出了哪些黄金标准中没有的内容，合理or不合理？",
  "dify_prescription_issues": "Dify 处方与黄金标准的差异，是否有安全隐患？无问题写'无'",
  "dify_overall_quality": "Dify 诊断整体质量评级: excellent/good/fair/poor",
  "overall_score": 0-100,
  "would_accept": true/false
}}

黄金标准诊断（标准答案）:
{{
  "diagnosis": "{gold_diag}",
  "prescription": "{gold_rx}"
}}

Dify 模型诊断（待评估）:
{{
  "diagnosis": "{dify_diag}",
  "prescription": "{dify_rx}"
}}
"""


def call_llm(prompt: str, model: str = "deepseek-v3.2") -> Dict[str, Any]:
    """调用 LLM，遇到 thinking mode 错误时重试"""
    api_key = LLM_API_KEYS.get(model, 'sk-2aee4f263dad2d98046bb67515e900c0')
    for attempt in range(2):
        try:
            client = OAI(api_key=api_key, base_url=LLM_BASE_URL)
            kwargs = dict(
                model=model, messages=[
                    {"role": "system", "content": "你只输出JSON，不输出任何其他文字。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1, max_tokens=1000, timeout=90
            )
            if attempt == 1:
                kwargs.pop('temperature')
                kwargs['extra_body'] = {"reasoning_content": None}
            response = client.chat.completions.create(**kwargs)
            return {'success': True, 'content': response.choices[0].message.content or ''}
        except Exception as e:
            if attempt == 0 and 'reasoning_content' in str(e):
                continue
            return {'success': False, 'error': str(e)}


def parse_json(text: str) -> Optional[Dict[str, Any]]:
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])
    except:
        pass
    return None


def deep_evaluation(gold_diag: str, gold_rx: str, dify_diag: str, dify_rx: str) -> Dict[str, Any]:
    """对差异大的 case 进行 LLM 深度评估"""
    prompt = DEEP_EVAL_PROMPT.format(
        gold_diag=gold_diag[:1500].replace('"', "'").replace('{', '(').replace('}', ')'),
        gold_rx=gold_rx[:800].replace('"', "'").replace('{', '(').replace('}', ')'),
        dify_diag=dify_diag[:1500].replace('"', "'").replace('{', '(').replace('}', ')'),
        dify_rx=dify_rx[:800].replace('"', "'").replace('{', '(').replace(')', ')'),
    )
    result = call_llm(prompt)
    if result.get('success'):
        data = parse_json(result.get('content', ''))
        if data:
            return {
                'deep_missed_findings': data.get('dify_missed_key_findings', ''),
                'deep_extra_findings': data.get('dify_extra_findings', ''),
                'deep_prescription_issues': data.get('dify_prescription_issues', ''),
                'deep_quality': data.get('dify_overall_quality', ''),
                'deep_score': data.get('overall_score', ''),
                'deep_accept': data.get('would_accept', ''),
            }
    return {
        'deep_missed_findings': result.get('error', '评估失败'),
        'deep_extra_findings': '',
        'deep_prescription_issues': '',
        'deep_quality': 'error',
        'deep_score': '',
        'deep_accept': '',
    }


# ============ 主流程 ============

def main():
    print("=" * 60)
    print("Dify 诊断 vs 黄金标准诊断 对比评估")
    print("=" * 60)

    # [1] 读取并筛选黄金标准数据
    print(f"\n[1] 读取并筛选黄金标准数据...")
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as f:
        all_cases = list(csv.DictReader(f))
    print(f"    总数据: {len(all_cases)} 条")

    if TOP_SCORE_ONLY:
        gold_cases = filter_high_quality(all_cases, TOP_SCORE_THRESHOLD)
        if len(gold_cases) < 20:
            print(f"    高分数据不足20条，降低阈值到60分...")
            gold_cases = filter_high_quality(all_cases, 60)
    else:
        gold_cases = all_cases

    # 分层抽样
    test_cases = stratified_sample(gold_cases, SAMPLE_SIZE)

    # 保存抽样清单
    with open(SAMPLED_FILE, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=test_cases[0].keys())
        writer.writeheader()
        writer.writerows(test_cases)
    print(f"    抽样清单已保存: {SAMPLED_FILE}")

    # [2] 逐条对比评估
    results = []
    need_deep = []  # 需要深度评估的 case

    for idx, case in enumerate(test_cases):
        cid = case.get('case_id', '') or case.get('user_query', '')[:40]
        disease_name = case.get('disease_name', '未知')
        gold_score = case.get('final_total_score', '')
        print(f"\n[{idx+1}/{len(test_cases)}] {disease_name} 原始分:{gold_score}")

        user_query = case.get('user_query', '')
        gold_diagnosis = case.get('diagnosis', '')
        gold_prescription = case.get('prescription', '')
        gold_withdrawal = case.get('withdrawal_period', '')

        # 2a. Dify 诊断
        print(f"    - Dify 诊断中...")
        dify_result = dify_diagnose(user_query)
        if not dify_result['success']:
            print(f"    - Dify 失败: {dify_result.get('error', '')}")
            results.append({
                'case_id': cid,
                'disease_name': disease_name,
                'gold_score': gold_score,
                'success': False,
                'error': dify_result.get('error', ''),
            })
            continue

        answer = dify_result['answer']
        dify_diag, dify_rx = extract_diagnosis_and_prescription(answer)
        print(f"    - 诊断提取完成 ({len(dify_diag)}字 / {len(dify_rx)}字处方)")
        if not dify_diag and not dify_rx:
            print(f"    - Dify 返回为空，跳过此条")
            results.append({
                'case_id': cid, 'disease_name': disease_name, 'gold_score': gold_score,
                'success': False, 'error': 'empty response',
            })
            continue

        # 2b. 对比分析（规则层）
        comparison = compare_diagnosis_vs_gold(
            gold_diagnosis, gold_prescription, disease_name,
            dify_diag, dify_rx,
        )
        overall = comparison['overall_match_score']
        print(f"    - 规则层匹配: 疾病={comparison['disease_jaccard']}% "
              f"药品={comparison['drug_jaccard']}% "
              f"文本={comparison['diagnosis_similarity']}% "
              f"综合={overall}%")

        # 2c. 差异大的 case 标记待深度评估
        if overall < 60:
            need_deep.append((idx, cid, gold_diagnosis, gold_prescription, dify_diag, dify_rx))
            print(f"    - 匹配度低 (<60%)，标记待深度评估")

        result = {
            'case_id': cid,
            'disease_name': disease_name,
            'gold_score': gold_score,
            'success': True,
            'error': '',
            'user_query': user_query[:100],
            'gold_diagnosis_excerpt': gold_diagnosis[:200],
            'dify_diagnosis_excerpt': dify_diag[:200],
            'gold_prescription_excerpt': gold_prescription[:150],
            'dify_prescription_excerpt': dify_rx[:150],
            # 对比指标
            'primary_disease_match': comparison['primary_disease_match'],
            'gold_diseases': comparison['gold_diseases'],
            'dify_diseases': comparison['dify_diseases'],
            'disease_jaccard': comparison['disease_jaccard'],
            'diagnosis_similarity': comparison['diagnosis_similarity'],
            'drug_jaccard': comparison['drug_jaccard'],
            'gold_drugs': comparison['gold_drugs'],
            'dify_drugs': comparison['dify_drugs'],
            'gold_structured': comparison['gold_structured'],
            'dify_structured': comparison['dify_structured'],
            'term_coverage': comparison['term_coverage'],
            'overall_match_score': overall,
            # 深度评估占位
            'deep_missed_findings': '',
            'deep_extra_findings': '',
            'deep_prescription_issues': '',
            'deep_quality': '',
            'deep_score': '',
            'deep_accept': '',
        }
        results.append(result)

        # 每 10 条保存一次中间结果
        if (idx + 1) % 10 == 0:
            with open(RESULT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()
                writer.writerows(results)

        time.sleep(0.5)

    # [3] 深度评估（差异大的 case）
    if need_deep:
        print(f"\n[3] 深度评估差异大的 case ({len(need_deep)} 条)...")
        for orig_idx, cid, gd, gp, dd, dr in need_deep:
            print(f"    - 深度评估: {cid[:30]}...")
            deep = deep_evaluation(gd, gp, dd, dr)
            # 更新原有结果
            for r in results:
                if r['case_id'] == cid:
                    r.update(deep)
                    break
            time.sleep(0.5)

    # [4] 保存结果
    print(f"\n[4] 保存结果...")

    with open(RESULT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(results)

    # 汇总统计
    valid = [r for r in results if r.get('success')]
    print(f"\n[5] 统计汇总")
    print(f"    ========================================")
    if valid:
        avg_match = sum(float(r.get('overall_match_score', 0) or 0) for r in valid) / len(valid)
        avg_disease = sum(float(r.get('disease_jaccard', 0) or 0) for r in valid) / len(valid)
        avg_drug = sum(float(r.get('drug_jaccard', 0) or 0) for r in valid) / len(valid)
        avg_diag_sim = sum(float(r.get('diagnosis_similarity', 0) or 0) for r in valid) / len(valid)
        primary_match_rate = sum(1 for r in valid if r.get('primary_disease_match') == 'True') / len(valid)

        print(f"    有效比对: {len(valid)}/{len(results)} 条")
        print(f"    主要诊断匹配率: {primary_match_rate*100:.1f}%")
        print(f"    疾病名称平均匹配: {avg_disease:.1f}%")
        print(f"    诊断文本相似度: {avg_diag_sim:.1f}%")
        print(f"    处方药品平均匹配: {avg_drug:.1f}%")
        print(f"    综合匹配分: {avg_match:.1f}/100")
        if need_deep:
            deep_valid = [r for r in valid if r.get('deep_quality')]
            if deep_valid:
                print(f"    深度评估: {len(deep_valid)} 条")
                accept_rate = sum(1 for r in deep_valid if r.get('deep_accept') == 'True') / len(deep_valid)
                print(f"    深度可接受率: {accept_rate*100:.1f}%")
    print(f"    ========================================")
    print(f"    结果文件: {RESULT_FILE}")

    # 打印排名（综合匹配分最低的 TOP10）
    valid_sorted = sorted(valid, key=lambda r: float(r.get('overall_match_score', 100) or 100))
    print(f"\n{'='*80}")
    print("Dify vs 黄金标准 匹配度最差 TOP 10")
    print(f"{'='*80}")
    for r in valid_sorted[:10]:
        diag_match = "✓" if r.get('primary_disease_match') == 'True' else "✗"
        print(f"  {diag_match} {r['disease_name']:<12} "
              f"综合:{r['overall_match_score']:>5}% "
              f"疾病:{r['disease_jaccard']:>5}% "
              f"药品:{r['drug_jaccard']:>5}%")
        print(f"    黄金疾病: {r.get('gold_diseases', '')}")
        print(f"    Dify疾病: {r.get('dify_diseases', '')}")


if __name__ == '__main__':
    main()
