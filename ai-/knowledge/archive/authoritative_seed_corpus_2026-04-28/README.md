# 鸡病知识底座权威种子语料包

## 概览

本目录用于作为“完整覆盖鸡病 + 可审计 + 可用于黄金数据集”的第一批权威种子语料。

- 下载日期：2026-04-28
- 下载位置：`knowledge/authoritative_seed_corpus_2026-04-28/`
- 成功下载文件数：23
- 覆盖范围：
  - 中国官方监管与法规
  - 鸡病相关诊断与净化标准
  - 国际动物卫生组织疾病页与法典入口
  - 开放获取的研究综述补充页

原始下载明细见：

- `metadata/download_manifest.csv`

## 目录结构

```text
authoritative_seed_corpus_2026-04-28/
├── cn_official/      # 中国官方监管、法规、公告、PDF
├── standards/        # 鸡病相关国标/行标/标准导航页
├── international/    # WOAH 与开放获取研究页面
├── metadata/
│   └── download_manifest.csv
└── README.md
```

## 使用原则

这批文件适合作为鸡病知识底座建设的第一批权威来源，但不是最终全量库。

- `cn_official/` 优先用于：
  - 动物疫病分级
  - 监管边界
  - 兽药标签/说明书制度
  - 批准文号制度
  - 兽药残留与 MRL 约束
- `standards/` 优先用于：
  - 诊断技术
  - 净化规程
  - 送检与实验室确认边界
- `international/` 优先用于：
  - 国际疾病定义
  - 跨来源病原学与防控背景
  - 对长尾病与英文术语的补充

## 已下载来源清单

### 1. 中国官方监管与法规

| 本地文件 | 来源机构 | 类型 | 主要用途 | 原始链接 |
|---|---|---|---|---|
| `cn_official/moa_2022_573_animal_disease_catalog.html` | 农业农村部 | 公告 | 一、二、三类动物疫病病种名录，确定鸡病监管分级 | [链接](https://www.moa.gov.cn/govpublic/xmsyj/202206/t20220629_6403635.htm) |
| `cn_official/moa_2022_574_animal_health_standards_notice.html` | 农业农村部 | 公告 | 动物健康标准相关公告入口 | [链接](https://www.moa.gov.cn/xw/bmdt/202206/t20220629_6403636.htm) |
| `cn_official/moa_2022_three_category_disease_prevention_spec.html` | 农业农村部 | 公告 | 三类动物疫病防治规范，补充监管处置边界 | [链接](https://www.moa.gov.cn/govpublic/xmsyj/202206/t20220629_6403637.htm) |
| `cn_official/moa_2022_national_mandatory_immunization_guidance.html` | 农业农村部 | 公告 | 国家动物疫病强制免疫指导意见 | [链接](https://www.moa.gov.cn/govpublic/xmsyj/202201/t20220107_6386445.htm) |
| `cn_official/moa_animal_epidemic_prevention_law.html` | 农业农村部 | 法律页面 | 动物防疫法，适合定义法定处置、报告、检疫要求 | [链接](https://www.moa.gov.cn/gk/zcfg/fl/202104/t20210425_6366545.htm) |
| `cn_official/moa_veterinary_label_and_insert_management.html` | 农业农村部 | 制度文件 | 兽药标签和说明书管理办法，适合约束 `label_basis` | [链接](https://www.moa.gov.cn/gk/nyncbgzk/gzk/202210/t20221012_6413171.htm) |
| `cn_official/moa_veterinary_approval_number_management.html` | 农业农村部 | 制度文件 | 兽药产品批准文号管理办法，适合约束批准状态与标签来源 | [链接](https://www.moa.gov.cn/gk/nyncbgzk/gzk/202210/t20221012_6413161.htm) |
| `cn_official/moa_veterinary_base_info_query_trial_notice.html` | 农业农村部办公厅 | 通知 | 国家兽药基础信息查询系统的官方存在证明 | [链接](https://www.moa.gov.cn/govpublic/SYJ/201208/t20120824_2897256.htm) |
| `cn_official/moa_veterinary_query_app_launch.html` | 农业农村部 | 新闻通稿 | 国家兽药综合查询 APP 上线说明，证明查询体系的官方用途 | [链接](https://www.moa.gov.cn/xw/zwdt/201807/t20180710_6153816.htm) |
| `cn_official/moa_2022_594_veterinary_residue_limits.pdf` | 农业农村部 / 国家卫生健康委 / 市场监管总局 | PDF 公告 | 含 GB 31650.1-2022 等残留限量标准，适合构建兽药残留与休药期风险框架 | [链接](https://www.moa.gov.cn/nybgb/2022/202210/202211/P020221115556927766576.pdf) |

### 2. 鸡病相关标准与净化规程

| 本地文件 | 来源机构 | 类型 | 主要用途 | 原始链接 |
|---|---|---|---|---|
| `standards/cahec_poultry_national_standards_index.html` | 全国动物卫生标准化技术委员会 | 标准导航页 | 鸡病相关国家标准总入口，适合持续扩抓 | [链接](https://std.cahec.cn/gb/12_2.html) |
| `standards/openstd_gbt_16550_2020_newcastle_diagnosis.html` | 国家标准全文公开系统 | 标准详情页 | GB/T 16550-2020 新城疫诊断技术 | [链接](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=DAA58A6FCC696F91339EED5BF8460CAB) |
| `standards/openstd_gbt_23197_2022_ib_diagnosis.html` | 国家标准全文公开系统 | 标准详情页 | GB/T 23197-2022 鸡传染性支气管炎诊断技术 | [链接](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=E047C85709682D29ABE9153B0D2154AD) |
| `standards/cahec_gbt_18936_2020_hpai_diagnosis.html` | 全国动物卫生标准化技术委员会 | 标准详情页 | GB/T 18936-2020 高致病性禽流感诊断技术 | [链接](https://std.cahec.cn/gb/details/493.html) |
| `standards/cahec_gbt_19167_2020_ibd_diagnosis.html` | 全国动物卫生标准化技术委员会 | 标准详情页 | GB/T 19167-2020 传染性法氏囊病诊断技术 | [链接](https://std.cahec.cn/gb/details/494.html) |
| `standards/cahec_nyt_556_2020_ilt_diagnosis.html` | 全国动物卫生标准化技术委员会 | 标准详情页 | NY/T 556-2020 鸡传染性喉气管炎诊断技术 | [链接](https://std.cahec.cn/qb/details/537.html) |
| `standards/openstd_gbt_43173_2023_pullorum_purification.html` | 国家标准全文公开系统 | 标准详情页 | GB/T 43173-2023 种鸡场鸡白痢沙门菌净化规程 | [链接](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=B5722D3A5519C618E966E9290DE31E08) |
| `standards/cahec_gbt_36873_2018_avian_leukosis_purification.html` | 全国动物卫生标准化技术委员会 | 标准详情页 | GB/T 36873-2018 原种鸡群禽白血病净化检测规程 | [链接](https://std.cahec.cn/gb/details/415.html) |

### 3. 国际组织与开放获取研究补充

| 本地文件 | 来源机构 | 类型 | 主要用途 | 原始链接 |
|---|---|---|---|---|
| `international/woah_avian_influenza_disease_page.html` | WOAH | 疾病页 | 国际禽流感定义、背景和关联标准入口 | [链接](https://www.woah.org/en/blog/disease/avian-influenza/) |
| `international/woah_newcastle_disease_page.html` | WOAH | 疾病页 | 国际新城疫定义、背景和关联标准入口 | [链接](https://www.woah.org/en/animal-health-in-the-world/animal-diseases/Newcastle-disease/) |
| `international/woah_terrestrial_code_index.html` | WOAH | 法典索引页 | 陆生动物卫生法典入口，适合扩展高监管疾病边界 | [链接](https://www.woah.org/fileadmin/Home/eng/Health_standards/tahc/2021/en_index.htm) |
| `international/pmc_nd_review_detection.html` | PubMed Central | 开放获取综述页 | 新城疫病毒检测方法综述，适合补充诊断技术演进 | [链接](https://pmc.ncbi.nlm.nih.gov/articles/PMC9378970/) |
| `international/pmc_avian_influenza_systematic_review.html` | PubMed Central | 开放获取系统综述页 | 禽流感病毒在家禽中的排毒系统综述，适合补充流行病学和风险因子 | [链接](https://pmc.ncbi.nlm.nih.gov/articles/PMC6784017/) |

## 审核建议

这批文件进入正式知识底座前，建议按以下顺序进行审核：

1. 先审 `cn_official/`
   - 用于建立 `authority_level = A0`
   - 先抽取监管、病种名录、标签和批准文号规则
2. 再审 `standards/`
   - 用于建立 `diagnostic_notes`、`lab_confirmation_required`、`reportable_boundary`
   - 重点抽取送检条件、诊断方法、净化与监测要求
3. 最后审 `international/`
   - 用于补充病原学、症候群、国际术语和长尾病背景
   - 不得覆盖中国官方监管约束

## 本批次未纳入自动下载但建议后续补充的权威源

以下来源权威性高，但本次没有纳入自动下载主包：

- 中国兽药信息网 / 国家兽药基础信息查询系统
  - 原因：官方性已由农业农村部文件证明，但页面体系更适合浏览器交互或人工导出
  - 用途：批准文号、标签说明书、批签发、抽检、追溯
- Merck Veterinary Manual
  - 原因：页面对脚本化批量抓取限制较强
  - 用途：鸡病临床表现、病理、鉴别诊断、处置边界
- 更多 PMC 开放获取综述
  - 原因：本次只下载了高价值示例页，后续可按病种扩展

## 下一步建议

基于这批种子文件，建议直接创建以下结构化资产：

- `knowledge/masters/source_inventory.csv`
- `knowledge/masters/evidence_registry.csv`
- `knowledge/masters/disease_universe.csv`
- `knowledge/masters/coverage_backlog.csv`

并对每份下载文件至少补录：

- `source_id`
- `source_org`
- `source_type`
- `authority_level`
- `scope`
- `usable_for`
- `record_status`
- `last_verified`
- `source_url`
- `saved_path`

这样这批文件就能从“下载包”升级成“可审计知识底座的证据起点”。
