# 鸡病权威资料汇编

## 1. 说明

这份汇编基于本目录已真实下载或已真实核验可访问的权威来源整理，目标是为“完整覆盖鸡病 + 可审计 + 可用于黄金数据集”的知识底座提供第一版可用资料。

严格边界如下：

- 只写本次已获取到的真实来源内容。
- 对于只拿到标准元信息、未拿到标准全文的资料，明确标注“仅获取到标准元信息”。
- 对于遇到反爬、验证码、浏览器预览限制而未拿到正文的资料，明确标注“当前未成功获取正文”。
- 不杜撰用药方案、不编造病例数据、不伪造统计数字。

## 2. 本批资料覆盖结论

### 已覆盖得较好的部分

- 中国官方监管边界
- 鸡病法定病种分级
- 强制免疫政策
- 三类动物疫病防治原则
- 兽药标签、说明书、批准文号制度
- 禽病诊断技术标准入口与部分标准正文/规程
- 种禽健康标准
- 禽白血病净化规程正文
- 行业统计中的家禽存出栏、禽肉、禽蛋产量
- 国际权威疾病描述中的主要病因、症状、诊断、控制原则

### 当前仍不完整的部分

- 中国兽药标签说明书数据库的批量导出正文
- 多数鸡病国家标准/行业标准全文 PDF
- 高质量、结构化、可直接核验的临床病例库
- 统一口径的“疾病级行业发病率/死亡率”公开统计
- 全病种官方“标准化治疗处方”公开资料

以上缺口在本汇编中不会被虚构内容填补。

## 3. 中国官方病种覆盖框架

### 3.1 法定动物疫病分级

来源：

- [农业农村部公告第573号](https://www.moa.gov.cn/govpublic/xmsyj/202206/t20220629_6403635.htm)
- 本地文件：[moa_2022_573_animal_disease_catalog.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_2022_573_animal_disease_catalog.html)

核心信息：

- **一类动物疫病**中，鸡相关最关键的是：`高致病性禽流感`
- **二类动物疫病**中，鸡相关明确列出：`新城疫`
- **三类动物疫病**中，禽病列出 21 种，包括：
  - 禽传染性喉气管炎
  - 禽传染性支气管炎
  - 禽白血病
  - 传染性法氏囊病
  - 马立克病
  - 禽痘
  - 鸡球虫病
  - 低致病性禽流感
  - 鸡病毒性关节炎
  - 禽传染性脑脊髓炎
  - 鸡传染性鼻炎
  - 禽坦布苏病毒感染
  - 禽腺病毒感染
  - 鸡传染性贫血
  - 禽偏肺病毒感染
  - 鸡红螨病
  - 鸡坏死性肠炎
  - 以及部分鸭、鹅相关病

对知识底座的直接意义：

- `reportable_level` 可直接以此为中国官方锚点
- `disease_universe` 可先以该目录为监管病种骨架
- `regulatory_risk` 可以按一类/二类/三类直接分层

## 4. 中国官方防控与管理边界

### 4.1 种用动物健康标准

来源：

- [农业农村部公告第574号](https://www.moa.gov.cn/xw/bmdt/202206/t20220629_6403636.htm)
- 本地文件：[moa_2022_574_animal_health_standards_notice.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_2022_574_animal_health_standards_notice.html)

对种禽的核心要求：

- 种禽范围明确包括：鸡、鸭、番鸭、鹅等
- 种禽健康标准要求：
  - 未发生高致病性禽流感
  - 未发生新城疫
  - 未发生禽白血病
  - 未发生鸡白痢
  - 并应临床健康
- 对高致病性禽流感、新城疫、禽白血病应进行监测，病原学监测结果应为阴性

对知识底座的直接意义：

- `breeder_risk`、`seed_stock_risk`、`purification_priority` 可以直接引用
- 对种鸡场场景，`send_for_testing` 和 `eradication_required` 的阈值更高

### 4.2 三类动物疫病防治规范

来源：

- [农业农村部关于印发《三类动物疫病防治规范》的通知](https://www.moa.gov.cn/govpublic/xmsyj/202206/t20220629_6403637.htm)
- 本地文件：[moa_2022_three_category_disease_prevention_spec.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_2022_three_category_disease_prevention_spec.html)

核心要求：

- 从业者发现动物患病或疑似患病时，应立即报告农业农村主管部门或动物疫病预防控制机构
- 养殖场户应加强环境卫生、通风、清洁饮水、消毒、无害化处理
- 可根据流行情况合理制定免疫程序
- 使用抗菌药、抗病毒药、驱虫药、消毒剂等治疗时，应符合国家兽药管理规定
- 必须严格执行用药时间、剂量、疗程、休药期，并建立用药记录，保存 2 年以上
- 患病畜禽应隔离，必要时对同群动物采取预防性措施

对知识底座的直接意义：

- 可以作为“鸡病治疗输出不得脱离国家兽药管理规定”的总规则来源
- `treatment_boundary`、`record_required`、`quarantine_required` 可直接抽取

### 4.3 国家动物疫病强制免疫指导意见

来源：

- [国家动物疫病强制免疫指导意见（2022—2025年）](https://www.moa.gov.cn/govpublic/xmsyj/202201/t20220107_6386445.htm)
- 本地文件：[moa_2022_national_mandatory_immunization_guidance.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_2022_national_mandatory_immunization_guidance.html)

鸡相关核心信息：

- 强制免疫总体目标：
  - 群体免疫密度常年保持在 90% 以上
  - 应免畜禽免疫密度达到 100%
  - 高致病性禽流感免疫抗体合格率常年保持在 70% 以上
- 对全国所有鸡、鸭、鹅、鹌鹑等人工饲养禽类，可根据当地实际与科学评估，选择适宜疫苗，实施 H5 和/或 H7 亚型高致病性禽流感免疫
- 省级农业农村部门可根据辖区流行情况，对 `新城疫` 等实施强制免疫
- 养殖场户要记录疫苗种类、生产厂家、生产批号等信息

对知识底座的直接意义：

- `immunization_policy`
- `mandatory_vaccine_context`
- `vaccine_record_required`
- `high-risk_nonimmune_exception`

都可以从此页抽取。

### 4.4 动物防疫法

来源：

- [中华人民共和国动物防疫法（农业农村部公开页）](https://www.moa.gov.cn/gk/zcfg/fl/202104/t20210425_6366545.htm)
- 本地文件：[moa_animal_epidemic_prevention_law.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_animal_epidemic_prevention_law.html)

本批次状态：

- 已下载到公开页面
- 本次未逐条抽取法条细目

建议用途：

- 后续作为 `reporting_obligation`、`quarantine_obligation`、`biosecurity_obligation` 的最高位法律来源

## 5. 兽药标签、批准文号、停药期与合规约束

### 5.1 兽药标签和说明书管理办法

来源：

- [兽药标签和说明书管理办法](https://www.moa.gov.cn/gk/nyncbgzk/gzk/202210/t20221012_6413171.htm)
- 本地文件：[moa_veterinary_label_and_insert_management.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_veterinary_label_and_insert_management.html)

核心信息：

- 兽药外包装标签必须标注：
  - 适应症
  - 用法与用量
  - 批准文号
  - 生产日期
  - 有效期
  - **停药期**
  - 生产企业信息
- 兽用化学药品、抗生素产品说明书必须注明：
  - 主要成分
  - 药理作用
  - 适应症
  - 用法与用量
  - 不良反应
  - 注意事项
  - **停药期**
- 标签和说明书内容必须真实、准确，不得虚假、夸大，不得有广告色彩
- 标签和说明书内容不得扩大疗效和应用范围
- 用法与用量、停药期、有效期等项目必须与法定兽药标准一致

对知识底座的直接意义：

- `label_basis` 和 `withdrawal_days_default` 不能凭经验写，必须锚定批准标签或法定标准
- 黄金样本中“处方建议”不得超出标签适应症边界
- “休药期不清”时，不能伪造具体天数

### 5.2 兽药产品批准文号管理办法

来源：

- [兽药产品批准文号管理办法](https://www.moa.gov.cn/gk/nyncbgzk/gzk/202210/t20221012_6413161.htm)
- 本地文件：[moa_veterinary_approval_number_management.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_veterinary_approval_number_management.html)

核心信息：

- 兽药生产企业生产兽药，应当取得农业农村部核发的兽药产品批准文号
- 批准文号是对“特定企业生产特定产品”的批准文件
- 审批时会同时批准标签和说明书
- 申请材料中明确包含：
  - 标签和说明书样本
  - 产品工艺、配方等资料
  - 检验/复核资料

对知识底座的直接意义：

- 不能把“某成分”简单等同于“任何鸡用产品都合法”
- 应以“批准文号对应标签与说明书”为产品级合规单位
- `drug_master` 应支持区分“成分级知识”和“产品级合规性”

### 5.3 国家兽药综合查询系统的官方性

来源：

- [兽药基础信息查询系统试运行通知](https://www.moa.gov.cn/govpublic/SYJ/201208/t20120824_2897256.htm)
- [国家兽药综合查询APP升级版全面上线运行](https://www.moa.gov.cn/xw/zwdt/201807/t20180710_6153816.htm)
- 本地文件：
  - [moa_veterinary_base_info_query_trial_notice.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_veterinary_base_info_query_trial_notice.html)
  - [moa_veterinary_query_app_launch.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_veterinary_query_app_launch.html)

结论：

- 官方文件已证明“国家兽药基础信息查询系统/国家兽药综合查询体系”具备权威性
- 但本次未成功批量抓取其产品级正文数据

因此本轮只能得到：

- `权威性确认`
- `系统用途确认`

尚未得到：

- `完整鸡用产品清单`
- `逐产品停药期`
- `逐产品标签全文`

这部分必须如实标记为“当前未完成采集”。

### 5.4 兽药残留与 MRL 公告

来源：

- [公告第594号 PDF](https://www.moa.gov.cn/nybgb/2022/202210/202211/P020221115556927766576.pdf)
- 本地文件：[moa_2022_594_veterinary_residue_limits.pdf](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/moa_2022_594_veterinary_residue_limits.pdf)

已确认信息：

- 公告中包含 `GB 31650.1-2022 食品中41种兽药最大残留限量`
- 还包含多项残留检测相关标准

本批次状态：

- PDF 已成功下载
- 本轮未抽取具体每种药的残留限量表

对知识底座的直接意义：

- 可以作为 `food_animal_residue_risk` 的官方基础源
- 后续应继续抽表，构建 `drug_residue_limit_master`

## 6. 鸡病诊断技术与净化规程

### 6.1 已获取到标准元信息的疾病

来源：

- [GB/T 16550-2020 新城疫诊断技术](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=DAA58A6FCC696F91339EED5BF8460CAB)
- [GB/T 23197-2022 鸡传染性支气管炎诊断技术](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=E047C85709682D29ABE9153B0D2154AD)
- [GB/T 18936-2020 高致病性禽流感诊断技术](https://std.cahec.cn/gb/details/493.html)
- [GB/T 19167-2020 传染性法氏囊病诊断技术](https://std.cahec.cn/gb/details/494.html)
- [NY/T 556-2020 鸡传染性喉气管炎诊断技术](https://std.cahec.cn/qb/details/537.html)

本地文件：

- [openstd_gbt_16550_2020_newcastle_diagnosis.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/standards/openstd_gbt_16550_2020_newcastle_diagnosis.html)
- [openstd_gbt_23197_2022_ib_diagnosis.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/standards/openstd_gbt_23197_2022_ib_diagnosis.html)
- [cahec_gbt_18936_2020_hpai_diagnosis.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/standards/cahec_gbt_18936_2020_hpai_diagnosis.html)
- [cahec_gbt_19167_2020_ibd_diagnosis.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/standards/cahec_gbt_19167_2020_ibd_diagnosis.html)
- [cahec_nyt_556_2020_ilt_diagnosis.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/standards/cahec_nyt_556_2020_ilt_diagnosis.html)

当前能确认的关键信息：

- 五项标准均为真实可核验标准页面
- 均由中国官方标准体系或全国动物卫生标准化技术委员会收录
- 可确认标准名称、标准号、状态、发布日期、实施日期、主管部门

当前不能声称已拿到的内容：

- 各标准全文逐章细节
- 样品采集、PCR 引物、判定阈值等完整正文

因此对这些标准，当前能安全写入知识底座的只有：

- `exists_official_standard = yes`
- `standard_no`
- `standard_name`
- `status = current`
- `effective_date`
- `source_link`

全文内容需后续在现代浏览器或正式标准下载途径中继续补全。

### 6.2 已获取到规程正文的标准：原种鸡群禽白血病净化检测规程

来源：

- [GB/T 36873-2018 原种鸡群禽白血病净化检测规程（CAHEC页）](https://std.cahec.cn/gb/details/415.html)
- 本地 PDF：[cahec_gbt_36873_2018_avian_leukosis_purification.pdf](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/standards/cahec_gbt_36873_2018_avian_leukosis_purification.pdf)

已提取到的正文核心信息：

- 适用对象：`原种鸡群`
- 标准目标：实施针对禽白血病的净化
- 规范性引用文件：
  - `GB/T 26436-2010 禽白血病诊断技术`
  - `NY/T 680-2003 禽白血病病毒 p27 抗原酶联免疫吸附试验方法`
- 重要流程节点包括：
  - 出壳雏鸡胎粪检测与淘汰
  - 育雏后期全血病毒分离检测与淘汰
  - 开产初期检测与淘汰
  - 留种前检测与淘汰
  - 种蛋选留和孵化
  - 不同世代持续检测与净化

关键技术细节：

- 雏鸡胎粪样品可用 PBS 稀释后冻融处理，再进行 p27 抗原检测
- 若同一母鸡所产雏鸡中有 1 只胎粪检测为阳性，则该袋中同胞雏鸡及对应母鸡均视为阳性
- 阳性鸡不再列为育种选育个体，应淘汰并无害化处理
- 育雏后期、开产初期和留种前，都要求进行病毒分离 / p27 抗原相关检测
- 公鸡检测不仅涉及全血，还涉及新鲜精液病毒分离
- 净化不是一次性行为，而是跨世代循环实施

对知识底座的直接意义：

- `eradication_protocol`
- `sampling_stage`
- `positive_disposition`
- `breeder_control_flow`

都可以从这份标准正文中直接结构化抽取。

### 6.3 鸡传染性喉气管炎诊断技术 PDF

来源：

- [NY/T 556-2020 鸡传染性喉气管炎诊断技术](https://std.cahec.cn/qb/details/537.html)
- 本地 PDF：[cahec_nyt_556_2020_ilt_diagnosis.pdf](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/standards/cahec_nyt_556_2020_ilt_diagnosis.pdf)

本批次状态：

- PDF 已成功下载
- 当前文本抽取失败，疑似扫描版或图像版 PDF

因此本轮只能确认：

- 标准真实存在
- PDF 已本地保存

不能声称已提取到全文诊断流程。

## 7. 国际权威疾病技术资料

### 7.1 禽流感

来源：

- [WOAH Avian Influenza](https://www.woah.org/en/blog/disease/avian-influenza/)
- [Merck Avian Influenza in Poultry and Wild Birds](https://www.merckvetmanual.com/poultry/avian-influenza/avian-influenza)

可确认的核心信息：

- 禽流感存在两种临床类型：
  - `LPAI`：可表现为亚临床感染、呼吸道症状或产蛋下降
  - `HPAI`：可表现为严重全身性疾病、多器官衰竭和高死亡率
- 家禽和多种野鸟均可感染

中国官方对应关系：

- 高致病性禽流感在中国为 `一类动物疫病`
- 低致病性禽流感在中国为 `三类动物疫病`

当前局限：

- 本轮未下载到可稳定抽取正文的中国标准全文
- 未获取到统一公开病例数据表

### 7.2 新城疫

来源：

- [GB/T 16550-2020 新城疫诊断技术](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=DAA58A6FCC696F91339EED5BF8460CAB)
- [WOAH Newcastle disease](https://www.woah.org/en/animal-health-in-the-world/animal-diseases/Newcastle-disease/)
- [Merck Newcastle Disease in Poultry](https://www.merckvetmanual.com/poultry/newcastle-disease-and-other-paramyxovirus-infections/newcastle-disease-in-poultry)

可确认的核心信息：

- 新城疫在中国列为 `二类动物疫病`
- 中国有现行国家标准 `GB/T 16550-2020`
- Merck 明确：
  - 新城疫由毒力型新城疫病毒引起
  - 可对家禽造成破坏性后果
  - 可通过口咽拭子、泄殖腔拭子或组织进行病毒分离
  - 商业家禽中可通过疫苗成功控制
  - `无特效治疗`

对知识底座的直接意义：

- `diagnosis_priority = lab_confirm + virus_isolation_or_molecular`
- `treatment_boundary = no_specific_treatment`
- `control_priority = vaccination + biosecurity`

### 7.3 鸡传染性支气管炎

来源：

- [GB/T 23197-2022 鸡传染性支气管炎诊断技术](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=E047C85709682D29ABE9153B0D2154AD)
- [Merck Infectious Bronchitis in Chickens](https://www.merckvetmanual.com/poultry/infectious-bronchitis/infectious-bronchitis-in-chickens)

可确认的核心信息：

- 这是鸡的急性、高度接触性上呼吸道病
- 常见临床特征不仅有呼吸道症状，还包括：
  - 产蛋下降
  - 蛋品质下降
  - 某些毒株可引起肾炎
- 可用诊断方法包括：
  - ELISA
  - HI
  - RT-PCR
  - 实时 RT-PCR
  - 胚蛋分离
  - 刺突基因序列分析
- 没有药物能改变 IBV 感染进程
- 抗菌药只能用于降低并发细菌感染导致的死亡

对知识底座的直接意义：

- 病毒病场景下不能把抗菌药写成“主治”
- `secondary_bacterial_complication_possible = yes`
- `egg_drop_context = important`

### 7.4 传染性法氏囊病

来源：

- [GB/T 19167-2020 传染性法氏囊病诊断技术](https://std.cahec.cn/gb/details/494.html)
- [Merck Infectious Bursal Disease in Poultry](https://www.merckvetmanual.com/poultry/infectious-bursal-disease/infectious-bursal-disease-in-poultry)

可确认的核心信息：

- IBD 见于全球幼龄家鸡，由 IBDV 引起
- 典型临床表现包括：
  - 精神沉郁
  - 水样腹泻
  - 羽毛蓬乱
  - 脱水
- 发病率高
- 常见情况下死亡率较低，但高毒株可高达 60% 或以上
- 诊断依赖：
  - 泄殖腔法氏囊大体和显微病变
  - 病毒基因组分子检测
- 免疫抑制与法氏囊 B 淋巴细胞丢失相关

对知识底座的直接意义：

- `young_chicken_priority = high`
- `immunosuppression_risk = high`
- `gross_lesion_key = cloacal_bursa`

### 7.5 鸡传染性喉气管炎

来源：

- [NY/T 556-2020 鸡传染性喉气管炎诊断技术](https://std.cahec.cn/qb/details/537.html)
- [Merck Infectious Laryngotracheitis](https://www.merckvetmanual.com/poultry/infectious-laryngotracheitis/infectious-laryngotracheitis)

可确认的核心信息：

- ILT 是鸡等禽类急性呼吸道病
- 病原为 `gallid alpha herpesvirus type 1`
- 关键临床特征包括：
  - 严重呼吸困难
  - 咳嗽
  - 啰音
  - 张口喘气
  - 咳出血性黏液
- 传播与感染鸟、垫料、设备、人员衣物及近距离气溶胶扩散有关
- 诊断依赖：
  - PCR
  - 组织病理学
  - 气管、喉和结膜黏膜中的合胞体与核内包涵体具有诊断意义
- 控制依赖疫苗和生物安全

### 7.6 鸡白痢

来源：

- [GB/T 43173-2023 种鸡场鸡白痢沙门菌净化规程](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=B5722D3A5519C618E966E9290DE31E08)
- [Merck Pullorum Disease in Poultry](https://www.merckvetmanual.com/poultry/salmonelloses-in-poultry/pullorum-disease-in-poultry)

可确认的核心信息：

- 鸡白痢由垂直传播的 `Salmonella enterica serotype Gallinarum biovar Pullorum` 引起
- 幼龄鸡和火鸡可出现很高死亡率
- 典型临床表现包括：
  - 靠近热源扎堆
  - 厌食、虚弱、嗜睡
  - 白色粪便糊肛
  - 也可见呼吸道症状、失明或关节肿胀
- 血清学检测可用于监测
- 确诊仍需病原分离和鉴定

对知识底座的直接意义：

- `vertical_transmission = yes`
- `breeder_purification_priority = very_high`
- `young_chick_high_mortality = yes`

### 7.7 禽白血病

来源：

- [GB/T 36873-2018 原种鸡群禽白血病净化检测规程](https://std.cahec.cn/gb/details/415.html)
- [Merck Avian Leukosis in Poultry](https://www.merckvetmanual.com/poultry/neoplasms-in-poultry/avian-leukosis-in-poultry)

可确认的核心信息：

- 禽白血病属于肿瘤性疾病
- 表现为造血组织肿瘤和肉瘤
- 常见于 16 周龄以上鸡
- 诊断标准包括：
  - 病史
  - 临床症状
  - 剖检
  - 组织学检查
- 没有有效治疗或疫苗
- 从种群中净化病毒是最有效控制方法

对知识底座的直接意义：

- `treatment_available = no`
- `vaccine_available = no`
- `eradication_from_breeding_flocks = primary_control`

### 7.8 鸡毒支原体感染

来源：

- [Merck Mycoplasma gallisepticum Infection in Poultry](https://www.merckvetmanual.com/poultry/mycoplasmosis/mycoplasma-gallisepticum-infection-in-poultry)

可确认的核心信息：

- 可引起鸡和火鸡呼吸道及全身性疾病
- 典型特征：
  - 发病率高
  - 单纯感染时死亡率低
  - 常与呼吸道病毒和大肠杆菌等形成多病原慢性呼吸道病
- 诊断常用：
  - 实时 PCR
  - 拭子分离培养
  - 血清学监测
- 抗菌药可减轻临床症状并减少经蛋传播，但**不能清除感染**
- 控制依赖：
  - 从阴性种鸡群引种
  - 生物安全
  - 监测
  - 高挑战情境下可考虑疫苗

## 8. 行业统计数据

### 8.1 2025 年全年家禽生产数据

来源：

- [国家统计局：2025年全国畜牧业生产情况解读](https://www.stats.gov.cn/zt_18555/zthd/lhfw/2026lhzt/2026sjjd/202602/t20260202_1962443.html)
- 本地文件：[stats_2025_national_livestock_summary.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/stats_2025_national_livestock_summary.html)

核心数据：

- `全国家禽出栏 183.2 亿只`
- `禽肉产量 2837 万吨`
- `禽蛋产量 3498 万吨`
- `年末家禽存栏 62.7 亿只`

补充价格信息：

- `活家禽价格下降 4.0%`

### 8.2 2025 年一季度家禽数据

来源：

- [国家统计局：一季度农业生产形势良好](https://www.stats.gov.cn/sj/sjjd/202504/t20250417_1959352.html)
- 本地文件：[stats_2025_q1_agriculture_summary.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/stats_2025_q1_agriculture_summary.html)

核心数据：

- `一季度全国家禽出栏 41.5 亿只`
- `禽肉产量 641 万吨`
- `禽蛋产量 866 万吨`
- `一季度末家禽存栏 61.1 亿只`

价格信息：

- `活家禽价格同比下降 5.3%`
- `禽蛋价格同比下降 2.8%`

### 8.3 2024 年上半年家禽数据

来源：

- [国家统计局：2024年上半年农业经济情况](https://www.stats.gov.cn/xxgk/jd/sjjd2020/202407/t20240715_1955608.html)
- 本地文件：[stats_2024_h1_agriculture_summary.html](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/cn_official/stats_2024_h1_agriculture_summary.html)

核心数据：

- `上半年全国家禽出栏 76.0 亿只`
- `禽肉产量 1182 万吨`
- `禽蛋产量 1703 万吨`
- `二季度末家禽存栏 63.2 亿只`

价格信息：

- `活家禽价格同比下降 3.3%`
- `禽蛋价格同比下降 10.6%`

对知识底座的直接意义：

- 可建立 `industry_context_master`
- 用于样本生成时的行业背景、出栏前压力、蛋价/肉禽价变化等场景变量

## 9. 当前没有成功获取到的真实资料

以下内容本轮没有拿到可核验正文，因此不能被写成“已有事实”：

1. 中国兽药信息网中全部鸡用产品的逐产品说明书正文
2. 全病种国家标准全文
3. 官方开放式鸡病病例库
4. 全国鸡病分病种发病率、病死率公开数据库
5. 可统一引用的中国官方“标准治疗处方库”
6. 本轮 PMC 两个页面的无验证码正文

对这些空白位，必须继续补采，不能编造。

## 10. 对知识底座建设的直接建议

基于本汇编，最适合先落地为结构化表的内容有：

- `disease_universe.csv`
  - 先录入农业农村部 573 号公告中的全部鸡病监管骨架
- `regulatory_rule_master.csv`
  - 录入强制免疫、报告义务、隔离、种禽健康标准
- `diagnostic_standard_master.csv`
  - 录入每个疾病已确认存在的标准号、状态、主管部门、实施日期
- `veterinary_label_rule_master.csv`
  - 录入标签、说明书、批准文号、停药期的法定要求
- `industry_context_master.csv`
  - 录入家禽出栏、存栏、禽肉、禽蛋、价格等行业背景数据
- `purification_protocol_master.csv`
  - 先录入禽白血病净化规程正文

## 11. 本地文件与清单

核心清单：

- [README.md](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/README.md)
- [download_manifest.csv](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/metadata/download_manifest.csv)
- [download_manifest_stats_supplement.csv](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/metadata/download_manifest_stats_supplement.csv)
- [download_manifest_pdfs_supplement.csv](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/metadata/download_manifest_pdfs_supplement.csv)

这份汇编本身：

- [authoritative_chicken_disease_digest.md](D:/ChongQinSanNong/knowledge/authoritative_seed_corpus_2026-04-28/authoritative_chicken_disease_digest.md)
