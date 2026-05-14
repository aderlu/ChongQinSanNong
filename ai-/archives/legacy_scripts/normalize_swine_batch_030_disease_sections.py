from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge" / "llm_wiki_swine_authoritative"


REPLACEMENTS = {
    "DIS-065-nutrient-deficiencies-and-excesses.md": {
        "实验室诊断": "- 营养缺乏或过量诊断很少是单一直线式归因；应结合配方、原料变更、混合均匀性、热加工、储存、采食量、水源、临床表现、病变、生产记录和实验室结果解释（`SRC-0084`, PDF page 1067-1070）。",
        "鉴别诊断": "- 营养异常需要与感染性疾病、管理问题、饮水中断、毒物暴露和霉菌毒素问题鉴别；单个体征或单项指标不足以定因（`SRC-0084`, PDF page 1067-1070）。",
        "防控要点": "- 防控重点是日粮和原料审查、加工与储存控制、混料核查、水源保障以及按阶段营养需求管理（`SRC-0084`, PDF page 1068-1076）。",
    },
    "DIS-066-mycotoxins-in-grains-and-feeds.md": {
        "传播途径": "- 猪霉菌毒素问题多数与污染饲料谷物有关，风险可出现在收获、储存、运输或饲喂环节（`SRC-0085`, PDF page 1079-1080）。",
        "临床症状": "- 霉菌毒素中毒表现可为急性、亚急性或慢性，常见问题包括采食下降、生产性能变化、肝毒性、繁殖异常或特定胆碱/神经样问题，需按毒素类别解释（`SRC-0085`, PDF page 1080-1092）。",
        "实验室诊断": "- 谷物或饲料检测支持暴露判断，但需结合批次、采食量、临床、病变和其他疾病鉴别，不得把单项检测直接等同病因（`SRC-0085`, PDF page 1082）。",
    },
    "DIS-067-aflatoxin-toxicosis.md": {
        "临床症状": "- 急性至亚急性黄曲霉毒素中毒可出现沉郁和肝毒性相关表现（`SRC-0085`, PDF page 1082-1083）。",
        "剖检变化": "- 黄曲霉毒素中毒可见肝脏相关病变，回答时应与饲料暴露和检测结果共同解释（`SRC-0085`, PDF page 1083）。",
        "用药/处置边界": "- 教材关于添加剂或饲料处理的讨论不得直接生成通用治疗、剂量、休药期或中国饲料放行结论（`SRC-0085`, PDF page 1084）。",
    },
    "DIS-068-don-trichothecene-toxicosis.md": {
        "临床症状": "- DON 是玉米、大麦和小麦等饲料中常见霉菌毒素，可与采食下降或拒食相关（`SRC-0085`, PDF page 1085-1086）。",
        "鉴别诊断": "- 采食下降或拒食不是 DON 的特异表现，必须结合饲料检测、批次暴露、其他霉菌毒素和非毒素性原因鉴别（`SRC-0085`, PDF page 1086）。",
    },
    "DIS-069-zearalenone-toxicosis.md": {
        "临床症状": "- ZEA 是具有雌激素样作用的霉菌毒素，解释阴户肿胀或繁殖道相关表现时应纳入饲料暴露鉴别（`SRC-0085`, PDF page 1088）。",
        "鉴别诊断": "- ZEA 相关表现需与正常发情、繁殖系统疾病、管理因素和其他饲料问题区分（`SRC-0085`, PDF page 1088）。",
    },
    "DIS-070-fumonisin-toxicosis.md": {
        "临床症状": "- 高水平富马毒素暴露可造成肺水肿或肝毒性相关问题；解释时需要饲料检测、临床病理和群体暴露证据（`SRC-0085`, PDF page 1091-1092）。",
        "用药/处置边界": "- 富马毒素安全水平或监管限量不能从教材讨论直接外推，需另引官方饲料或监管标准（`SRC-0085`, PDF page 1092）。",
    },
    "DIS-071-toxic-minerals-chemicals-plants-and-gases.md": {
        "传播途径": "- 毒物暴露可来自饲料、水源、环境、工业污染、药物/添加剂、杀虫剂、植物、垫料或粪污气体（`SRC-0086`, PDF page 1096-1109）。",
        "实验室诊断": "- 毒物病例需要建立暴露史并结合毒理检测、病理、群体分布和鉴别诊断；非特异症状不能单独定因（`SRC-0086`, PDF page 1096-1111）。",
        "鉴别诊断": "- 有机砷、钠离子中毒、有机汞中毒和部分病毒性神经病可互相混淆，需结合暴露史和组织学/毒理证据（`SRC-0086`, PDF page 1099-1107）。",
    },
    "DIS-072-nitrite-toxicosis.md": {
        "临床症状": "- 急性亚硝酸盐中毒可快速出现全身性缺氧相关表现，需结合水源或饲料暴露和实验室证据解释（`SRC-0086`, PDF page 1105）。",
        "鉴别诊断": "- 突然死亡或发绀不能单独定因亚硝酸盐中毒，应与其他窒息性、循环性和毒物性事件鉴别（`SRC-0086`, PDF page 1105）。",
    },
    "DIS-073-toxic-gases-ventilation-failure.md": {
        "传播途径": "- 粪污分解可释放氨、硫化氢等有害气体；通风失败、搅动粪池或封闭空间可增加暴露风险（`SRC-0086`, PDF page 1108-1109）。",
        "防控要点": "- 疑似粪污气体或通风失败事件应按群体环境暴露处理，优先核查通风、粪池搅动、封闭空间和人员安全（`SRC-0086`, PDF page 1108-1109）。",
    },
}


def replace_section(text: str, heading: str, body: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return text
    body_start = start + len(marker)
    next_start = text.find("\n## ", body_start)
    if next_start < 0:
        next_start = len(text)
    return text[:body_start].rstrip() + "\n\n" + body.rstrip() + "\n" + text[next_start:]


def main() -> None:
    for filename, sections in REPLACEMENTS.items():
        path = WIKI / "wiki" / "diseases" / filename
        text = path.read_text(encoding="utf-8")
        for heading, body in sections.items():
            text = replace_section(text, heading, body)
        path.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
