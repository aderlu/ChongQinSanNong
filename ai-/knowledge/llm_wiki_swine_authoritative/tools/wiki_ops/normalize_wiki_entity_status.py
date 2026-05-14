from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"

# 只清洗当前知识图谱真正作为实体页/综合页入口的目录。
# sources、rule_cards、rules 等目录承载的是来源和规则本身，不在这里批量改写，
# 避免把“事实来源”和“实体页使用范围”两种概念混在一起。
TARGET_DIRS = ["diseases", "drugs", "comparisons", "syndromes", "synthesis"]


def parse_inline_list(value: str) -> list[str]:
    """解析 frontmatter 中的一行列表。

    当前项目没有强依赖 PyYAML，因此本脚本只处理最常见的两种写法：
    1. `[a, b, c]`
    2. `a, b, c`

    这足够覆盖 usage_scope/tags/sources 这类简单字段，同时避免引入新的依赖。
    """
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    return [item.strip().strip("'\"") for item in value.split(",") if item.strip()]


def format_inline_list(items: list[str]) -> str:
    """把 usage_scope 统一写成 `[a, b, c]`，方便人工阅读和 rg 检索。"""
    return "[" + ", ".join(items) + "]"


def split_frontmatter(text: str) -> tuple[list[str], str] | None:
    """拆分 Markdown frontmatter 和正文。

    只处理以 `---` 开头的标准 Markdown 页面。没有 frontmatter 的页面会跳过；
    这能防止脚本误改普通说明文档。对于确实需要进入图谱的无 frontmatter 矩阵页，
    已经单独补过最小 frontmatter。
    """
    if not text.startswith("---\n"):
        return None
    lines = text.splitlines()
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return None
    return lines[1:end], "\n".join(lines[end + 1 :]) + ("\n" if text.endswith("\n") else "")


def frontmatter_dict(lines: list[str]) -> dict[str, str]:
    """把 frontmatter 的顶层 `key: value` 行转成字典。

    这里故意不解析缩进结构，因为本项目实体页 frontmatter 主要是扁平字段。
    如果遇到缩进行，直接保留原文，避免破坏可能存在的复杂 YAML 片段。
    """
    values: dict[str, str] = {}
    for line in lines:
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def infer_status(path: Path, values: dict[str, str], body: str) -> tuple[str, str, list[str]]:
    """根据页面类型、旧状态和正文线索推断三字段状态。

    三字段含义：
    - source_trust: 来源可信度。当前 wiki 数据默认来自权威官网、文献、书籍和规则卡，
      因此除非显式标 `needs_source_check`，统一归一为 `authoritative`。
    - evidence_coverage: 页面证据覆盖度。只表达页面覆盖是否完整，不再表达来源是否权威。
    - usage_scope: 页面可服务的任务范围。它是页面级路由标签，不等同于语义边 verified。

    注意：这个函数不会判断某条“疾病-药物”关系是否医学上成立；
    关系是否成立仍由后续 edge validator、source alignment 和 medical entailment 判断。
    """
    page_type = path.parent.name
    legacy = values.get("legacy_evidence_status", "")
    old_gold = values.get("gold_dataset_use", "")
    existing_scope = parse_inline_list(values.get("usage_scope", "[]")) if values.get("usage_scope") else []
    usage = {item for item in existing_scope if item}

    # source_trust 只保留两个枚举：authoritative / needs_source_check。
    # 过去一些页面把 human_reviewed、source_anchored 等写到 source_trust 里，
    # 这些其实描述的是审核或覆盖状态，不是来源可信度，因此统一折叠为 authoritative。
    raw_source_trust = values.get("source_trust", "authoritative") or "authoritative"
    source_trust = "needs_source_check" if raw_source_trust == "needs_source_check" else "authoritative"

    # evidence_coverage 只保留 complete / partial / minimal。
    # 旧值里包含 source_anchored、human_reviewed、regulatory_boundary_page 等，
    # 它们来自不同历史阶段，粒度不一致；这里统一映射，降低后续判断复杂度。
    evidence_coverage = values.get("evidence_coverage", "")
    if evidence_coverage in {
        "source_anchored_drug_evidence_page",
        "source_anchored_clinical_page",
        "human_reviewed",
        "curated_source_anchored",
        "processed_source_anchored",
        "regulatory_boundary_page",
    }:
        evidence_coverage = "complete"
    elif evidence_coverage in {"partial_source_anchored_page", "partial_evidence_page", "partial_drug_evidence_page", "needs_review"}:
        evidence_coverage = "partial"
    if not evidence_coverage:
        # 兼容旧 frontmatter：没有新字段时，从 legacy_evidence_status 推断覆盖度。
        # HUMAN_REVIEWED/PROCESSED_SOURCE_ANCHORED 表示页面证据覆盖相对完整；
        # NEEDS_REVIEW 或 partial 页面表示只用于召回、缺口路由和边界提示。
        if legacy in {"HUMAN_REVIEWED", "PROCESSED_SOURCE_ANCHORED"}:
            evidence_coverage = "complete"
        elif legacy == "NEEDS_REVIEW" or "partial_evidence_page" in values.get("tags", ""):
            evidence_coverage = "partial"
        else:
            evidence_coverage = "complete"

    # retrieval 是最基础的页面级用途：页面可以被检索召回。
    # 它不代表页面可以直接生成诊疗结论，也不代表页面中的每条关系已经 verified。
    usage.add("retrieval")
    if page_type == "diseases":
        # 完整疾病页可用于诊断、鉴别、防控和黄金数据候选；
        # 部分疾病页只作为召回和缺口路由，避免模型补全缺失栏目。
        if evidence_coverage == "complete":
            usage.update({"diagnosis_support", "differential_support", "control_support", "gold_candidate"})
        else:
            usage.add("gap_routing")
        # 疾病页可以承载治疗/监管边界提示，但疾病页本身不能单独生成执行性处方、
        # 休药期、MRL 或法域监管结论；这些仍需要药物页、标签/法规来源和 rule card。
        usage.update({"treatment_boundary", "regulatory_boundary"})
    elif page_type == "drugs":
        # 药物页默认可用于药物边界判断，包括标签、适应症、禁用、休药期、MRL、
        # 法域限制和处方管理等。是否能正向推荐用药，还要看具体标签/事实来源。
        usage.add("drug_boundary")
        if old_gold == "boundary_only" or "boundary_only" in body:
            # boundary_only 不能作为正向用药来源，只能用于边界、拒答、审计和风险提示。
            usage.update({"audit_only"})
            usage.discard("positive_drug_candidate")
            usage.discard("gold_candidate")
        if old_gold == "evidence_linked_candidate" or "positive_label_candidate" in body:
            # positive_drug_candidate 只是“可作为正向用药候选来源”，不是直接可训练正例。
            # 最终仍要检查靶动物、剂型、适应症、剂量/疗程、休药期/MRL 和法域一致性。
            usage.add("positive_drug_candidate")
        if evidence_coverage != "complete":
            usage.add("gap_routing")
    elif page_type == "comparisons":
        # comparison 页面天然用于鉴别诊断、相似疾病区分和评估题构造。
        usage.update({"differential_support", "gold_candidate"})
    elif page_type == "syndromes":
        # syndrome 页面用于症候入口、问诊组织和鉴别路径，不直接替代具体疾病结论。
        usage.update({"diagnosis_support", "differential_support"})
    elif page_type == "synthesis":
        # synthesis 多数是规则、矩阵、门控或摘要页，默认偏审计/辅助用途。
        usage.add("audit_only")
        if "dataset" in values.get("tags", "") or "generation_gate" in values.get("tags", ""):
            usage.add("gold_candidate")

    # 固定 usage_scope 输出顺序，让 diff 稳定，后续 review 不会被集合随机顺序干扰。
    order = [
        "retrieval",
        "diagnosis_support",
        "differential_support",
        "control_support",
        "regulatory_boundary",
        "treatment_boundary",
        "drug_boundary",
        "positive_drug_candidate",
        "gold_candidate",
        "gap_routing",
        "audit_only",
        "negative_trap",
    ]
    sorted_usage = [item for item in order if item in usage] + sorted(usage - set(order))
    return source_trust, evidence_coverage, sorted_usage


def rewrite_frontmatter(lines: list[str], source_trust: str, evidence_coverage: str, usage_scope: list[str]) -> list[str]:
    """重写 frontmatter 中的状态字段。

    这个函数只替换状态字段，不动 `sources`、`tags`、`disease_id`、`drug_id`、
    `updated` 等实体身份和来源字段。新三字段插入到 `sources` 前，方便打开页面时
    第一屏就能看到页面可信度、覆盖度和用途范围。
    """
    drop = {"legacy_evidence_status", "gold_dataset_use", "task_use_status", "risk_class", "source_trust", "evidence_coverage", "usage_scope"}
    rewritten: list[str] = []
    inserted = False
    for line in lines:
        key = line.split(":", 1)[0].strip() if ":" in line and not line.startswith(" ") else ""
        if key in drop:
            continue
        if not inserted and key == "sources":
            rewritten.extend(
                [
                    f"source_trust: {source_trust}",
                    f"evidence_coverage: {evidence_coverage}",
                    f"usage_scope: {format_inline_list(usage_scope)}",
                ]
            )
            inserted = True
        rewritten.append(line)
    if not inserted:
        rewritten.extend(
            [
                f"source_trust: {source_trust}",
                f"evidence_coverage: {evidence_coverage}",
                f"usage_scope: {format_inline_list(usage_scope)}",
            ]
        )
    return rewritten


REDUNDANT_LINE_PATTERNS = [
    # 以下只删除历史模板噪声，不删除医学事实或证据锚点。
    # “可用边界”“不得生成处方”“休药期/MRL 需复核”等安全边界是正文知识，
    # 不属于冗余状态，应该继续保留。
    re.compile(r"^- Runtime task use:.*$", re.MULTILINE),
    re.compile(r"^- Legacy audit status, if present, is not a usability gate;.*$", re.MULTILINE),
    re.compile(r"^- Runtime tier: `runtime_core_(?:reviewed|partial)`; evidence status: `[^`]+`\.\n?", re.MULTILINE),
    re.compile(r"^- 页面状态：[^。\n]+。?；?`?evidence_status=[^`\n]+`?。?\n?", re.MULTILINE),
]


def normalize_body(body: str) -> str:
    """压缩正文中的历史状态模板行。

    只做保守清理：
    - 删除重复的 runtime/legacy 状态说明；
    - 把少量旧标签说法替换成新的 usage_scope 说法；
    - 合并多余空行。

    不会删除 source_id/fact_id/anchor、证据句、药物禁用、剂量、休药期、
    MRL、监管限制等高风险医学内容。
    """
    updated = body
    for pattern in REDUNDANT_LINE_PATTERNS:
        updated = pattern.sub("", updated)
    updated = updated.replace("gold dataset role:", "usage scope role:")
    updated = updated.replace("boundary_only, negative_trap, exclude_from_positive_generation, or NEEDS_REVIEW drug page", "drug_boundary/audit_only/gap_routing page")
    updated = re.sub(r"\n{3,}", "\n\n", updated)
    return updated


def normalize_file(path: Path) -> bool:
    """规范化单个 Markdown 页面。

    返回 True 表示文件内容发生变化。所有读写都显式使用 UTF-8，并用 `newline="\\n"`
    统一换行，减少 Windows 环境下的编码和换行噪声。
    """
    text = path.read_text(encoding="utf-8")
    split = split_frontmatter(text)
    if split is None:
        return False
    lines, body = split
    values = frontmatter_dict(lines)
    source_trust, evidence_coverage, usage_scope = infer_status(path, values, body)
    new_lines = rewrite_frontmatter(lines, source_trust, evidence_coverage, usage_scope)
    new_body = normalize_body(body)
    new_text = "---\n" + "\n".join(new_lines) + "\n---\n\n" + new_body.lstrip("\n")
    if new_text != text:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    """批量清洗目标目录并打印最多 200 个变更文件。

    输出用于工作留痕和人工复核。脚本可以重复运行；当页面已经规范化后，
    再次运行应尽量保持 no-op 或只产生极少量可解释变更。
    """
    changed: list[str] = []
    for dirname in TARGET_DIRS:
        for path in sorted((WIKI / dirname).glob("*.md")):
            if normalize_file(path):
                changed.append(path.relative_to(ROOT).as_posix())
    print(f"normalized_files={len(changed)}")
    for item in changed[:200]:
        print(item)


if __name__ == "__main__":
    main()
