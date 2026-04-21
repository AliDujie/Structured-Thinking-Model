---
name: skill01
description: 像咨询公司资深总监一样，系统化地研究一家公司。涵盖企业外部环境分析、行业竞争格局、消费者洞察、客户满意度与忠诚度、品牌价值、战略规划等全维度研究框架与方法论。适用于企业调研、竞争分析、投资尽调、战略咨询、品牌诊断等场景。
---

# 研究公司 - 企业全维度调研方法论

像一位咨询公司资深总监一样，运用系统化的框架和方法论，对一家公司进行全面、深入、专业的研究。本skill整合了战略分析、消费者洞察、客户忠诚度、品牌价值、商业模型等领域的核心方法论，形成一套完整的企业研究体系。

## 适用场景

- 对目标公司进行全面调研（投资尽调、合作评估、竞争分析）
- 为企业制定战略规划提供分析基础
- 品牌诊断与消费者洞察研究
- 客户满意度与忠诚度体系构建
- 行业竞争格局与市场机会分析
- 企业内部能力评估与战略匹配

## 核心原则

作为资深总监，研究公司时必须遵循以下原则：

1. **由外而内**：先理解宏观环境与行业格局，再深入企业内部
2. **竞争视角**：一切分析必须置于竞争语境中，孤立评价毫无意义
3. **消费者导向**：最终价值由消费者定义，所有分析回归消费者需求
4. **数据驱动**：定性洞察必须有定量验证，避免主观臆断
5. **行动导向**：每一项分析必须指向可执行的战略建议

## 执行能力

本skill提供以下8大可执行能力，每个能力对应一个Python分析模块：

### 能力1：宏观环境分析（PEST/PESTEL）

**触发条件**: 用户需要分析企业所处的宏观环境、政策影响、经济趋势、社会变迁、技术变革等

**输入要求**:
- 公司名称、所属行业
- 各维度的关键因素（名称、描述、评分1-5、权重0-1、趋势）

**执行步骤**:
1. 创建 `MacroAnalyzer(company, industry, mode="pestel")`
2. 逐一添加各维度因素 `add_factor(dimension, name, description, score, weight, trend, impact)`
3. 调用 `render_markdown()` 或 `render_json()` 输出分析结果

**输出格式**: 包含各维度评分表、EFE加权总分、环境态势判断、关键发现、战略启示

**Python API**:
```python
from skill01 import CompanyResearchSkill
skill = CompanyResearchSkill("目标公司", "零售行业")
skill.macro.add_factor("political", "产业政策", "政府对行业的支持力度", score=4.0, weight=0.15, trend="上升")
skill.macro.add_factor("economic", "GDP增长", "宏观经济增长趋势", score=3.5, weight=0.12, trend="稳定")
print(skill.macro.render_markdown())
```

### 能力2：行业竞争格局分析（五力模型+CPM+生命周期）

**触发条件**: 用户需要分析行业竞争结构、竞争强度、关键成功因素、行业生命周期

**输入要求**:
- 公司名称、所属行业
- 五力模型各力量的驱动因素
- 竞争对手信息、关键成功因素评分

**执行步骤**:
1. 创建 `IndustryAnalyzer(company, industry)`
2. 设置生命周期阶段 `set_lifecycle_stage(stage)`
3. 添加五力驱动因素 `add_force_driver(force, name, description, score, weight)`
4. 添加竞争对手 `add_competitor(name, market_share, strengths, weaknesses)`
5. 添加关键成功因素 `add_ksf(name, weight, company_score, competitor_scores)`
6. 调用 `render_markdown()` 输出

**输出格式**: 五力评分表、行业吸引力评估、竞争态势矩阵(CPM)、生命周期判断

**Python API**:
```python
skill.industry.set_lifecycle_stage("maturity")
skill.industry.add_force_driver("rivalry", "竞争者数量", "行业内主要竞争者超过10家", score=4.0, weight=0.3)
skill.industry.add_ksf("品牌知名度", weight=0.2, company_score=4.0, competitor_scores={"竞品A": 3.5})
print(skill.industry.render_markdown())
```

### 能力3：企业战略与能力分析（SWOT+BCG+GE+价值链+7S+安索夫）

**触发条件**: 用户需要评估企业战略选择、业务组合、内部能力、组织协调性、增长方向

**输入要求**:
- SWOT各象限条目（内容+重要性评分）
- 业务单元信息（增长率、相对市场份额）
- GE矩阵因素（行业吸引力+业务竞争力）
- 价值链活动表现评分
- 7S要素评估

**执行步骤**:
1. 创建 `StrategyAnalyzer(company, industry)`
2. 添加SWOT条目 `add_swot_item(quadrant, content, importance)`
3. 添加SWOT组合策略 `add_swot_strategy(strategy_type, description, actions)`
4. 添加业务单元 `add_business_unit(name, market_growth_rate, relative_market_share)`
5. 添加GE因素 `add_ge_factor(name, weight, score, category)`
6. 添加价值链活动 `add_value_chain_activity(name, category, performance, competitor_benchmark)`
7. 添加7S评估 `add_seven_s(element, assessment, score, issues)`
8. 设置安索夫策略 `set_ansoff_choice(strategy)`
9. 调用 `render_markdown()` 输出

**输出格式**: SWOT矩阵+组合策略、BCG矩阵定位图、GE九象限定位、价值链对比、7S协调性评估

**Python API**:
```python
skill.strategy.add_swot_item("strengths", "品牌知名度高", importance=5)
skill.strategy.add_swot_item("weaknesses", "线上渠道薄弱", importance=4)
skill.strategy.add_business_unit("核心业务", market_growth_rate=15.0, relative_market_share=1.5)
skill.strategy.add_seven_s("strategy", "聚焦高端市场", score=4.0)
print(skill.strategy.render_markdown())
```

### 能力4：消费者洞察分析（价值要素金字塔+STP+营销组合）

**触发条件**: 用户需要理解消费者价值感知、市场细分与定位、营销组合评估

**输入要求**:
- 消费者价值要素评分（30个要素中的关键要素）
- 市场细分信息、目标市场选择、定位策略
- 4P/4C/4R营销组合评估

**执行步骤**:
1. 创建 `ConsumerAnalyzer(company, industry)`
2. 添加价值要素评分 `add_value_score(element, score, competitor_scores, importance)`
3. 添加市场细分 `add_segment(name, size, growth, characteristics, needs, is_target)`
4. 设置定位 `set_positioning(target_segment, value_proposition, differentiation)`
5. 添加营销组合评估 `add_marketing_mix(dimension, assessment, score, recommendations)`
6. 调用 `render_markdown()` 输出

**输出格式**: 价值要素金字塔评分、行业标杆对比、NPS预测、STP分析、营销组合评估表

**关键洞察**: 在四个以上价值要素上获得高分的企业，NPS约为仅1个高分要素企业的3倍。质量是所有价值要素的基础。

**Python API**:
```python
skill.consumer.add_value_score("质量", score=4.5, competitor_scores={"竞品A": 4.0}, importance=5.0)
skill.consumer.add_value_score("感官体验", score=4.0, importance=4.0)
skill.consumer.add_segment("年轻白领", size="3000万", growth="15%", is_target=True)
skill.consumer.set_positioning("年轻白领", "高品质生活方式", "天然健康")
print(skill.consumer.render_markdown())
```

### 能力5：客户满意度与忠诚度分析（WAO+Satisfactor+Loyalty Optimizer+ICE）

**触发条件**: 用户需要分析客户钱包份额、满意度驱动因素、忠诚度分层、客户体验

**输入要求**:
- 品牌排名与满意度数据（WAO公式输入）
- 满意度驱动因素（重要性+表现评分）
- 客户分层数据
- 竞争品牌流失数据
- ICE体验维度评估

**执行步骤**:
1. 创建 `LoyaltyAnalyzer(company, industry)`
2. 添加品牌排名 `add_brand_ranking(brand, satisfaction_score, rank, brand_count)`
3. 添加满意度驱动因素 `add_satisfaction_driver(name, importance, performance, is_delight, is_dissatisfaction)`
4. 添加客户分层 `add_loyalty_segment(segment_type, count, percentage, strategy)`
5. 添加竞争流失 `add_competitive_loss(competitor, lost_customers, lost_revenue, reasons)`
6. 添加ICE评估 `add_ice_assessment(dimension, current_score, target_score, gap_description)`
7. 调用 `render_markdown()` 输出

**输出格式**: WAO钱包份额计算表、满意度驱动因素矩阵、客户分层策略、竞争流失分析、ICE差距分析

**关键洞察**: 满意度与钱包份额相关性仅0.1，排名与钱包份额相关性高达0.9。制胜之道是取得比竞争对手更高的排名。

**Python API**:
```python
skill.loyalty.add_brand_ranking("目标公司", satisfaction_score=4.2, rank=1, brand_count=5)
skill.loyalty.add_brand_ranking("竞品A", satisfaction_score=4.0, rank=2, brand_count=5)
skill.loyalty.add_satisfaction_driver("服务响应速度", importance=4.5, performance=3.0, is_dissatisfaction=True)
skill.loyalty.add_loyalty_segment("core", count=5000, percentage=35.0)
print(skill.loyalty.render_markdown())
```

### 能力6：品牌价值分析（品牌资产+竞争品牌对比+差异化策略）

**触发条件**: 用户需要评估品牌资产、品牌竞争定位、差异化策略

**输入要求**:
- 品牌知名度数据
- 品牌联想属性评分
- 品牌形象维度评分
- 品牌忠诚度层级
- 竞争品牌信息
- 差异化策略方案

**执行步骤**:
1. 创建 `BrandAnalyzer(company, industry)`
2. 设置知名度 `set_awareness(top_of_mind, aided_awareness, recognition)`
3. 添加品牌联想 `add_association(attribute, strength, uniqueness, favorability)`
4. 添加形象维度 `add_image_dimension(dimension, score, competitor_scores)`
5. 设置忠诚度 `set_loyalty(level, distribution)`
6. 添加竞争品牌 `add_competitor_brand(name, awareness, image_score, loyalty_level, key_strengths)`
7. 添加差异化策略 `add_differentiation(strategy_type, description, feasibility, impact, actions)`
8. 调用 `render_markdown()` 输出

**输出格式**: 品牌知名度数据、联想属性评分表、形象维度对比、忠诚度分布、竞争品牌矩阵、差异化策略优先级

**Python API**:
```python
skill.brand.set_awareness(top_of_mind=25.0, aided_awareness=75.0, recognition=90.0)
skill.brand.add_association("高品质", strength=4.5, uniqueness=3.5, favorability=4.0)
skill.brand.set_loyalty(level=3, distribution={1: 10, 2: 25, 3: 35, 4: 20, 5: 10})
skill.brand.add_differentiation("客户体验差异化", "打造全渠道无缝体验", feasibility=4.0, impact=4.5)
print(skill.brand.render_markdown())
```

### 能力7：综合研究报告生成

**触发条件**: 用户需要生成完整的企业研究报告

**输入要求**:
- 各模块分析结果（通过能力1-6生成）
- 执行摘要、企业概况
- 综合诊断发现
- 战略建议

**执行步骤**:
1. 完成能力1-6的分析
2. 设置报告元信息 `report.set_executive_summary(summary)`, `report.set_company_overview(overview)`
3. 添加诊断发现 `report.add_finding(category, finding, severity, evidence, recommendation)`
4. 添加战略建议 `report.add_recommendation(title, description, timeframe, priority, actions)`
5. 调用 `generate_full_report()` 自动整合所有模块输出

**输出格式**: 十章完整研究报告（执行摘要→宏观环境→行业分析→企业概况→战略分析→消费者洞察→品牌诊断→客户体验→综合诊断→战略建议）

**Python API**:
```python
skill.report.set_executive_summary("本报告对目标公司进行了全维度研究...")
skill.report.add_finding("战略", "线上渠道布局滞后于竞争对手", severity="高")
skill.report.add_recommendation("加速数字化转型", "投资线上渠道建设", timeframe="短期", priority="高")
print(skill.generate_full_report())
```

### 能力8：知识库搜索与访谈提纲生成

**触发条件**: 用户需要查阅特定分析框架的方法论，或生成研究访谈问题

**执行方式**:
```python
# 搜索知识库
results = skill.search_knowledge("五力模型")
# 加载特定主题知识
knowledge = skill.load_knowledge("strategy_capability")
# 获取访谈问题
questions = skill.get_interview_questions("consumer_insight")
# 获取创新检查清单
checklist = skill.get_innovation_checklist()
```

## 触发条件速查表

| 用户意图 | 触发能力 | 核心工具 |
|----------|----------|----------|
| 分析宏观环境/政策/经济趋势 | 能力1 | MacroAnalyzer |
| 分析行业竞争/五力/生命周期 | 能力2 | IndustryAnalyzer |
| 评估企业战略/SWOT/业务组合 | 能力3 | StrategyAnalyzer |
| 理解消费者需求/价值/定位 | 能力4 | ConsumerAnalyzer |
| 分析客户满意度/忠诚度/钱包份额 | 能力5 | LoyaltyAnalyzer |
| 评估品牌价值/差异化/竞争定位 | 能力6 | BrandAnalyzer |
| 生成完整研究报告 | 能力7 | ReportGenerator |
| 查阅方法论/生成访谈提纲 | 能力8 | search_knowledge |

## 研究框架总览

一个完整的公司研究包含六大模块，按以下顺序推进：

| 序号 | 模块 | 核心问题 | 参考文档 |
|------|------|----------|----------|
| 1 | 宏观环境分析 | 企业所处的政治、经济、社会、技术环境如何？ | [macro-environment](references/macro-environment.md) |
| 2 | 行业竞争格局 | 行业结构如何？竞争态势怎样？企业处于什么位置？ | [industry-competition](references/industry-competition.md) |
| 3 | 企业战略与能力 | 企业的战略选择是什么？核心竞争力在哪里？ | [strategy-capability](references/strategy-capability.md) |
| 4 | 消费者洞察 | 消费者真正看重什么？需求如何被满足？ | [consumer-insight](references/consumer-insight.md) |
| 5 | 客户满意度与忠诚度 | 客户体验如何？忠诚度驱动因素是什么？钱包份额如何？ | [loyalty-satisfaction](references/loyalty-satisfaction.md) |
| 6 | 品牌与价值体系 | 品牌价值如何？消费者价值要素如何构成？ | [brand-value](references/brand-value.md) |

## 分析工具速查

### 第一层：宏观与行业分析工具

| 工具 | 用途 | 核心维度 |
|------|------|----------|
| PEST/PESTEL分析 | 宏观环境扫描 | 政治、经济、社会、技术、环境、法律 |
| 波特五力模型 | 行业竞争结构分析 | 新进入者、替代品、供应商、买方、现有竞争 |
| 行业生命周期 | 判断行业发展阶段 | 导入期、成长期、成熟期、衰退期 |
| 战略集团分析 | 行业内竞争格局细分 | 战略维度聚类、移动壁垒 |

### 第二层：企业战略分析工具

| 工具 | 用途 | 核心维度 |
|------|------|----------|
| SWOT分析 | 企业综合态势评估 | 优势、劣势、机会、威胁 |
| 波士顿矩阵(BCG) | 业务组合规划 | 市场增长率、相对市场份额 |
| GE矩阵 | 多因素业务评估 | 行业吸引力、业务竞争力 |
| 价值链分析 | 竞争优势来源识别 | 基本活动、支持活动 |
| 核心竞争力分析 | 持续竞争优势评估 | 价值性、稀缺性、难以模仿性、组织性 |
| 安索夫矩阵 | 增长战略选择 | 市场渗透、市场开发、产品开发、多元化 |
| 麦肯锡7S模型 | 组织能力诊断 | 战略、结构、制度、风格、人员、技能、共同价值观 |

### 第三层：消费者与品牌分析工具

| 工具 | 用途 | 核心维度 |
|------|------|----------|
| 消费者价值要素金字塔 | 解构消费者价值感知 | 功能、情感、改变生活、社会影响（30个要素） |
| STP分析 | 市场细分与定位 | 细分、目标选择、定位 |
| 4P/4C/4R营销分析 | 营销组合评估 | 产品/消费者、价格/成本、渠道/便利、促销/沟通 |
| 品牌资产模型 | 品牌价值评估 | 知名度、形象、联想、忠诚度 |

### 第四层：客户忠诚度分析工具

| 工具 | 用途 | 核心维度 |
|------|------|----------|
| 钱包分配法则(WAO) | 预测与提升钱包份额 | 品牌排名、品牌数量、钱包份额 |
| Satisfactor模型 | 满意度驱动因素识别 | 客户期望、不满与愉悦、竞争地位 |
| Loyalty Optimizer | 忠诚度细分与策略 | 客户价值、忠诚度指数、驱动因素 |
| ICE完美顾客体验 | 客户体验设计与优化 | 接触点、情境、感觉、区段、地理、时间 |
| Rewards Optimizer | 奖励计划优化 | 奖励类型、返利方法、客户参与度 |

### 第五层：决策与思维工具

| 工具 | 用途 |
|------|------|
| 六顶思考帽 | 多角度决策 |
| KT决策法 | 系统化决策 |
| 5W2H分析法 | 问题拆解 |
| 平衡计分卡 | 绩效评估 |
| 杜邦分析法 | 财务分析 |
| PDCA循环 | 持续改善 |

## 知识库文件清单

| 主题 | 文件 | 描述 |
|------|------|------|
| 宏观环境分析 | [macro-environment.md](references/macro-environment.md) | PEST/PESTEL分析框架与操作方法 |
| 行业竞争格局 | [industry-competition.md](references/industry-competition.md) | 五力模型、战略集团、行业生命周期 |
| 企业战略与能力 | [strategy-capability.md](references/strategy-capability.md) | SWOT、BCG、GE、价值链、7S、安索夫等 |
| 消费者洞察 | [consumer-insight.md](references/consumer-insight.md) | 价值要素金字塔、STP、4P/4C/4R |
| 客户满意度与忠诚度 | [loyalty-satisfaction.md](references/loyalty-satisfaction.md) | WAO、Satisfactor、Loyalty Optimizer、ICE |
| 品牌与价值体系 | [brand-value.md](references/brand-value.md) | 品牌资产模型、差异化策略 |
| 思维模型与决策工具 | [thinking-models.md](references/thinking-models.md) | 六顶思考帽、KT决策法、平衡计分卡等 |
| 战略矩阵工具集 | [strategy-matrices.md](references/strategy-matrices.md) | IE矩阵、定向政策矩阵、大战略矩阵等 |
| 商业框架速查 | [business-frameworks.md](references/business-frameworks.md) | 70个商业框架索引 |

## 关键提醒

研究公司时，务必注意以下几点。不能像在真空中一样评估品牌表现，必须始终在竞争语境中进行分析。满意度得分高不代表钱包份额高，沃尔玛的教训证明了这一点——满意度上升的同时，钱包份额却在下降。消费者价值是多层次的，不能只关注功能价值而忽视情感和生活改变层面的价值。质量是所有价值要素的基础，任何其他要素都无法弥补质量的重大缺失。在数字化时代，"节省时间"和"避免麻烦"是数字品牌的天然优势，实体品牌需要在"徽章价值""归属感"等情感要素上建立差异化。
