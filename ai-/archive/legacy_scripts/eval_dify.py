"""
Dify 公司模型诊断 + 原有裁判打分评估脚本
"""

import csv
import time
import re
import json
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List, Dict, Any

# ============ 配置 ============
DIFY_BASE_URL = 'https://dify.amdu.dtyunxi.cn/v1'
DIFY_COMPANY_KEY = 'app-lh3ByE1G9M0PIU4c2509iG1Y'

# 使用项目原有 LLM 配置
LLM_BASE_URL = 'https://api.nonelinear.com/v1'
LLM_API_KEY = 'sk-2aee4f263dad2d98046bb67515e900c0'

# 数据源
INPUT_FILE = 'C:/Users/admin/Desktop/每日内容/ai兽医问诊_wt_benchmark/鸡病数据合成系统/results/chicken_disease_dataset_production_20260420_212855.csv'
OUTPUT_FILE = f'results/dify_evaluation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

# 并发配置
MAX_PARALLEL = 4
BATCH_SIZE = 20

# ============ Dify API 调用 ============

def call_dify_chat(query: str, inputs: dict, timeout: int = 120) -> dict:
    """调用 Dify chat-messages API"""
    try:
        resp = requests.post(
            f'{DIFY_BASE_URL}/chat-messages',
            headers={'Authorization': f'Bearer {DIFY_COMPANY_KEY}', 'Content-Type': 'application/json'},
            json={
                'query': query,
                'inputs': inputs,
                'response_mode': 'blocking',
                'user': 'eval-system'
            },
            timeout=timeout
        )
        if resp.status_code == 200:
            data = resp.json()
            return {'success': True, 'answer': data.get('answer', '')}
        else:
            return {'success': False, 'error': f'HTTP {resp.status_code}: {resp.text[:200]}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def company_diagnose(user_query: str) -> dict:
    """公司模型诊断 (Dify)"""
    return call_dify_chat(
        query=user_query,
        inputs={'pop_num': '500'},
        timeout=120
    )


# ============ 原有裁判模型 (使用非线性 API) ============

from openai import OpenAI

def call_llm_judge(messages: List[dict], model: str = "deepseek-v3.2", temperature: float = 0.2) -> dict:
    """调用 LLM 裁判"""
    try:
        client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=1600,
            timeout=60
        )
        return {'success': True, 'content': response.choices[0].message.content or ''}
    except Exception as e:
        return {'success': False, 'error': str(e), 'content': ''}


JUDGE_SYSTEM_PROMPT = """你是鸡病黄金数据集评审专家，请按接近 G-Eval 的方式进行多维度评分，并严格只输出 JSON。

评分维度：
1. diagnosis_accuracy: 0-30
2. pathology_logic: 0-20
3. prescription_safety: 0-30
4. data_quality: 0-20

额外要求：
- fatal_risk 仅在明显禁药、明显错误剂量、缺失关键安全信息时为 true。
- structured_pass 用于判断结构化输出是否合格。
- summary、strengths、weaknesses 用极短中文短语。

JSON schema:
{
  "diagnosis_accuracy": 0,
  "pathology_logic": 0,
  "prescription_safety": 0,
  "data_quality": 0,
  "total_score": 0,
  "fatal_risk": false,
  "structured_pass": true,
  "summary": "...",
  "strengths": "...",
  "weaknesses": "..."
}"""


def build_judge_prompt(user_query: str, diagnosis: str, prescription: str) -> List[dict]:
    """构建裁判 prompt"""
    return [
        {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
        {"role": "user", "content": f"""请评估下面这条鸡病黄金数据样本：

user_query:
{user_query[:1000]}

diagnosis:
{diagnosis[:1500]}

prescription:
{prescription[:1000]}"""}
    ]


def extract_score(text: str) -> Optional[float]:
    """从裁判JSON回答中提取总分"""
    import json as _json
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            data = _json.loads(text[start:end])
            return float(data.get('total_score', 0))
    except:
        pass
    return None


# ============ 数据处理 ============

def process_single_case(case: dict, case_idx: int) -> dict:
    """处理单个案例"""
    user_query = case.get('user_query', '')
    original_diagnosis = case.get('diagnosis', '')
    original_prescription = case.get('prescription', '')

    result = {
        'case_id': case.get('case_id', ''),
        'disease_name': case.get('disease_name', ''),
        'user_query': user_query[:200],
        'original_score': case.get('final_total_score', ''),
        'company_diagnosis': '',
        'judge1_answer': '',
        'judge1_score': None,
        'judge2_answer': '',
        'judge2_score': None,
        'final_score': None,
        'process_status': 'pending'
    }

    # 1. 公司模型诊断
    print(f"[{case_idx}] 公司模型诊断中...")
    company_result = company_diagnose(user_query)
    if company_result['success']:
        result['company_diagnosis'] = company_result['answer']
    else:
        result['process_status'] = f"公司模型失败: {company_result.get('error', '')}"
        print(f"[{case_idx}] 公司模型失败")
        return result

    # 2. 裁判1打分
    print(f"[{case_idx}] 裁判1打分中...")
    judge1 = call_llm_judge(build_judge_prompt(
        user_query,
        result['company_diagnosis'],
        original_prescription
    ))
    result['judge1_answer'] = judge1.get('content', '')[:800]
    result['judge1_score'] = extract_score(judge1.get('content', ''))

    # 3. 裁判2打分 (使用 gpt-5.4-mini)
    print(f"[{case_idx}] 裁判2打分中...")
    judge2 = call_llm_judge(
        build_judge_prompt(user_query, result['company_diagnosis'], original_prescription),
        model="gpt-5.4-mini"
    )
    result['judge2_answer'] = judge2.get('content', '')[:800]
    result['judge2_score'] = extract_score(judge2.get('content', ''))

    # 计算最终分数
    scores = [s for s in [result['judge1_score'], result['judge2_score']] if s]
    if scores:
        result['final_score'] = sum(scores) / len(scores)

    result['process_status'] = 'completed'
    print(f"[{case_idx}] 完成! 裁判1:{result['judge1_score']}分 裁判2:{result['judge2_score']}分 最终:{result['final_score']}分")

    return result


def process_batch(cases: List[dict], start_idx: int) -> List[dict]:
    """并发处理一批案例"""
    results = []
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as executor:
        futures = {
            executor.submit(process_single_case, case, start_idx + i): i
            for i, case in enumerate(cases)
        }
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"处理异常: {e}")
    return results


# ============ 主流程 ============

def main():
    print("=" * 60)
    print("Dify 公司模型诊断 + 裁判打分评估")
    print("=" * 60)

    # 读取数据
    print(f"\n[1] 读取数据...")
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        all_cases = list(reader)
    print(f"    总数据: {len(all_cases)} 条")

    # 取前2条测试
    test_cases = all_cases[:2]
    print(f"    测试数据: {len(test_cases)} 条")

    # 处理数据
    print(f"\n[2] 开始处理 (并发数: {MAX_PARALLEL})...")
    results = []

    for batch_start in range(0, len(test_cases), BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, len(test_cases))
        batch = test_cases[batch_start:batch_end]
        print(f"    处理批次 {batch_start}-{batch_end}...")

        batch_results = process_batch(batch, batch_start)
        results.extend(batch_results)

        if batch_end < len(test_cases):
            time.sleep(1)

    # 保存结果
    print(f"\n[3] 保存结果...")
    if results:
        fieldnames = [
            'case_id', 'disease_name', 'user_query', 'original_score',
            'company_diagnosis',
            'judge1_answer', 'judge1_score',
            'judge2_answer', 'judge2_score',
            'final_score', 'process_status'
        ]

        with open(OUTPUT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    # 统计
    success = sum(1 for r in results if r.get('process_status') == 'completed')
    print(f"\n[4] 处理完成! 成功:{success} 失败:{len(results)-success}")
    print(f"    结果已保存到: {OUTPUT_FILE}")

    # 预览
    print("\n" + "=" * 60)
    print("结果预览:")
    for i, r in enumerate(results):
        print(f"\n案例 {i+1}: {r.get('disease_name', '未知')}")
        print(f"  原始分数: {r.get('original_score', 'N/A')}")
        print(f"  裁判1: {r.get('judge1_score', 'N/A')}分")
        print(f"  裁判2: {r.get('judge2_score', 'N/A')}分")
        print(f"  最终: {r.get('final_score', 'N/A')}分")


if __name__ == '__main__':
    main()
