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


## 八、Python 可执行工具包

### 8.1 安装与依赖

skill01 仅使用 Python 标准库（dataclasses、json、re、pathlib、datetime），无需安装第三方依赖，Python >= 3.8 即可运行。

安装方式一：将 skill01 目录解压到 `~/.aoneclaw/skills/` 下即可使用。

安装方式二：从代码仓库克隆后，在项目根目录下直接 import：

```python
import sys
sys.path.insert(0, "/path/to/skill01-repo")
from skill01 import CompanyResearchSkill
```

### 8.2 CompanyResearchSkill 统一入口类

`CompanyResearchSkill` 是整个工具包的统一入口，封装了全部 8 大执行能力。初始化时只需传入公司名称和行业：

```python
from skill01 import CompanyResearchSkill

skill = CompanyResearchSkill("目标公司", "零售行业")
```

**属性列表**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `config` | `AnalysisConfig` | 全局配置（公司名、行业、模块选择、评分标准等） |
| `macro` | `MacroAnalyzer` | 宏观环境分析器（PEST/PESTEL） |
| `industry` | `IndustryAnalyzer` | 行业竞争分析器（五力+CPM+生命周期） |
| `strategy` | `StrategyAnalyzer` | 企业战略分析器（SWOT+BCG+GE+价值链+7S+安索夫） |
| `consumer` | `ConsumerAnalyzer` | 消费者洞察分析器（价值要素+STP+营销组合） |
| `loyalty` | `LoyaltyAnalyzer` | 客户忠诚度分析器（WAO+Satisfactor+ICE） |
| `brand` | `BrandAnalyzer` | 品牌价值分析器（品牌资产+差异化） |
| `report` | `ReportGenerator` | 综合报告生成器 |

**方法列表**：

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `search_knowledge(keyword, topics)` | `List[Dict]` | 搜索知识库 |
| `load_knowledge(topic)` | `str` | 加载指定主题知识 |
| `load_all_knowledge()` | `Dict[str, str]` | 加载全部知识库 |
| `get_interview_questions(module)` | `List[str]` 或 `Dict` | 获取访谈问题 |
| `get_innovation_checklist()` | `List[str]` | 获取创新检查清单 |
| `generate_full_report()` | `str` | 生成完整研究报告 |
| `validate_config()` | `List[str]` | 验证配置，返回错误列表 |

### 8.3 六大核心分析模块

#### 8.3.1 MacroAnalyzer — 宏观环境分析

**使用场景**: 分析企业所处的政治、经济、社会、技术、环境、法律等宏观因素，评估外部环境的机会与威胁。

**核心方法**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `add_factor()` | `dimension`(str), `name`(str), `description`(str), `score`(float,1-5), `weight`(float,0-1), `trend`(str), `impact`(str) | `MacroAnalyzer` | 添加PEST因素 |
| `add_factors_batch()` | `factors`(List[Dict]) | `MacroAnalyzer` | 批量添加因素 |
| `get_key_findings()` | 无 | `List[str]` | 获取关键发现 |
| `get_implications()` | 无 | `List[str]` | 获取战略启示 |
| `render_markdown()` | 无 | `str` | 输出Markdown报告 |
| `render_json()` | 无 | `str` | 输出JSON数据 |
| `get_knowledge()` | 无 | `str` | 加载宏观环境知识库 |

**dimension 可选值**: `political`, `economic`, `social`, `technological`, `environmental`, `legal`

**trend 可选值**: `上升`, `稳定`, `下降`

**示例**:

```python
skill.macro.add_factor("political", "产业政策", "政府支持力度加大", score=4.0, weight=0.15, trend="上升")
skill.macro.add_factor("economic", "GDP增长", "经济增速放缓", score=3.0, weight=0.12, trend="下降")
skill.macro.add_factor("technological", "AI技术", "人工智能加速渗透", score=4.5, weight=0.13, trend="上升")
print(skill.macro.render_markdown())
```

#### 8.3.2 IndustryAnalyzer — 行业竞争格局分析

**使用场景**: 分析行业竞争结构、竞争强度、关键成功因素、行业生命周期阶段，评估行业吸引力。

**核心方法**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `set_lifecycle_stage()` | `stage`(str) | `IndustryAnalyzer` | 设置行业生命周期阶段 |
| `add_force_driver()` | `force`(str), `name`(str), `description`(str), `score`(float), `weight`(float) | `IndustryAnalyzer` | 添加五力驱动因素 |
| `add_competitor()` | `name`(str), `market_share`(float), `strengths`(List), `weaknesses`(List), `strategy`(str) | `IndustryAnalyzer` | 添加竞争对手 |
| `add_ksf()` | `name`(str), `weight`(float), `company_score`(float), `competitor_scores`(Dict) | `IndustryAnalyzer` | 添加关键成功因素 |
| `get_attractiveness_assessment()` | 无 | `str` | 获取行业吸引力评估 |
| `get_lifecycle_insights()` | 无 | `List[str]` | 获取生命周期洞察 |
| `render_markdown()` / `render_json()` | 无 | `str` | 输出报告 |

**force 可选值**: `new_entrants`, `substitutes`, `supplier_power`, `buyer_power`, `rivalry`

**stage 可选值**: `introduction`, `growth`, `maturity`, `decline`

**示例**:

```python
skill.industry.set_lifecycle_stage("maturity")
skill.industry.add_force_driver("rivalry", "竞争者数量", "行业内超过10家主要企业", score=4.0, weight=0.3)
skill.industry.add_force_driver("substitutes", "电商替代", "线上渠道替代加速", score=4.5, weight=0.2)
skill.industry.add_ksf("品牌知名度", weight=0.2, company_score=4.0, competitor_scores={"竞品A": 4.5})
print(skill.industry.render_markdown())
```

#### 8.3.3 StrategyAnalyzer — 企业战略与能力分析

**使用场景**: 评估企业战略选择、业务组合健康度、内部能力、组织协调性、增长方向。

**核心方法**:

| 方法 | 关键参数 | 说明 |
|------|----------|------|
| `add_swot_item()` | `quadrant`(strengths/weaknesses/opportunities/threats), `content`, `importance`(1-5) | 添加SWOT条目 |
| `add_swot_strategy()` | `strategy_type`(SO/WO/ST/WT), `description`, `actions` | 添加组合策略 |
| `add_business_unit()` | `name`, `market_growth_rate`, `relative_market_share` | 添加BCG业务单元 |
| `add_ge_factor()` | `name`, `weight`, `score`, `category`(attractiveness/competitiveness) | 添加GE因素 |
| `add_value_chain_activity()` | `name`, `category`(primary/support), `performance`, `competitor_benchmark` | 添加价值链活动 |
| `add_seven_s()` | `element`(strategy/structure/systems/style/staff/skills/shared_values), `assessment`, `score` | 添加7S评估 |
| `set_ansoff_choice()` | `strategy`(market_penetration/market_development/product_development/diversification) | 设置安索夫策略 |
| `render_markdown()` / `render_json()` | 无 | 输出报告 |

**示例**:

```python
skill.strategy.add_swot_item("strengths", "品牌知名度高", importance=5)
skill.strategy.add_swot_item("weaknesses", "线上渠道薄弱", importance=4)
skill.strategy.add_swot_strategy("SO", "利用品牌优势拓展下沉市场", actions=["开设社区店", "发展加盟"])
skill.strategy.add_business_unit("核心零售", market_growth_rate=5.0, relative_market_share=1.5)
skill.strategy.add_seven_s("strategy", "聚焦高端零售", score=4.0)
skill.strategy.set_ansoff_choice("market_development")
print(skill.strategy.render_markdown())
```
#### 8.3.4 ConsumerAnalyzer — 消费者洞察分析

**使用场景**: 理解消费者价值感知结构、市场细分与定位、营销组合评估，识别高价值要素和NPS预测。

**核心方法**:

| 方法 | 关键参数 | 说明 |
|------|----------|------|
| `add_value_score()` | `element`(30个价值要素之一), `score`(1-5), `competitor_scores`(Dict), `importance`(float) | 添加价值要素评分 |
| `add_segment()` | `name`, `size`, `growth`, `characteristics`(List), `needs`(List), `is_target`(bool) | 添加市场细分 |
| `set_positioning()` | `target_segment`, `value_proposition`, `differentiation`, `reason_to_believe` | 设置市场定位 |
| `add_marketing_mix()` | `dimension`, `assessment`, `score`, `recommendations`(List) | 添加营销组合评估 |
| `get_high_performing_elements()` | `threshold`(float, 默认4.0) | 获取高分价值要素 |
| `get_value_pyramid_summary()` | 无 | 按金字塔层次汇总 |
| `get_nps_prediction()` | 无 | NPS预测 |
| `get_industry_benchmark()` | 无 | 获取行业标杆要素 |

**30个价值要素（按金字塔层次）**:

第一层功能价值：节省时间、减少努力、简化流程、避免麻烦、赚钱、降低成本、降低风险、质量、组织整理、多样性、整合连接、感官体验、联结沟通、信息告知。

第二层情感价值：减少焦虑、健康/保健、奖励自我、治愈价值、怀旧感、趣味/娱乐、设计/美学、徽章价值、吸引力、提供接触渠道。

第三层改变生活价值：提供希望、自我激励、自我实现、传承价值、归属感。

第四层社会影响价值：自我超越。

**示例**:

```python
skill.consumer.add_value_score("质量", score=4.5, competitor_scores={"竞品A": 4.0}, importance=5.0)
skill.consumer.add_value_score("感官体验", score=4.0, importance=4.5)
skill.consumer.add_segment("年轻白领", size="3000万", growth="15%",
    characteristics=["25-35岁", "一二线城市"], needs=["健康", "便捷"], is_target=True)
skill.consumer.set_positioning("年轻白领", "高品质健康生活", "天然有机原料", "十年有机认证")
print(skill.consumer.render_markdown())
print(f"高分要素数量: {skill.consumer.count_high_elements()}")
print(f"NPS预测: {skill.consumer.get_nps_prediction()}")
```

#### 8.3.5 LoyaltyAnalyzer — 客户满意度与忠诚度分析

**使用场景**: 分析客户钱包份额（WAO法则）、满意度驱动因素（Satisfactor）、忠诚度分层（Loyalty Optimizer）、客户体验（ICE）、竞争流失分析。

**核心方法**:

| 方法 | 关键参数 | 说明 |
|------|----------|------|
| `add_brand_ranking()` | `brand`, `satisfaction_score`, `rank`, `brand_count` | 添加品牌排名（自动计算WAO钱包份额） |
| `add_satisfaction_driver()` | `name`, `importance`, `performance`, `is_delight`, `is_dissatisfaction` | 添加满意度驱动因素 |
| `add_loyalty_segment()` | `segment_type`(core/high_value_at_risk/low_value_at_risk/low_value_satisfied), `count`, `percentage`, `strategy` | 添加客户分层 |
| `add_competitive_loss()` | `competitor`, `lost_customers`, `lost_revenue`, `reasons`(List), `recovery_cost` | 添加竞争流失 |
| `add_ice_assessment()` | `dimension`(接触点/情境/感觉/区段/地理/时间), `current_score`, `target_score`, `gap_description`, `improvement_actions` | 添加ICE评估 |
| `get_company_wallet_share()` | 无 | 获取企业钱包份额 |
| `get_priority_drivers()` | `top_n` | 获取优先改善驱动因素 |

**WAO核心公式**: 钱包份额 = (1 - 排名/(品牌数量+1)) × (2/品牌数量)

**示例**:

```python
skill.loyalty.add_brand_ranking("目标公司", satisfaction_score=4.2, rank=1, brand_count=5)
skill.loyalty.add_brand_ranking("竞品A", satisfaction_score=4.0, rank=2, brand_count=5)
skill.loyalty.add_satisfaction_driver("服务响应速度", importance=4.5, performance=3.0, is_dissatisfaction=True)
skill.loyalty.add_loyalty_segment("core", count=5000, percentage=35.0, strategy="VIP维护计划")
skill.loyalty.add_competitive_loss("竞品A", lost_customers=500, lost_revenue=250000,
    reasons=["配送慢", "促销不足"], recovery_cost=50000)
skill.loyalty.add_ice_assessment("接触点", current_score=3.5, target_score=5.0,
    gap_description="线上接触点体验不一致", improvement_actions=["统一UI", "优化速度"])
print(f"钱包份额: {skill.loyalty.get_company_wallet_share():.1%}")
print(skill.loyalty.render_markdown())
```

#### 8.3.6 BrandAnalyzer — 品牌价值分析

**使用场景**: 评估品牌资产（知名度、联想、形象、忠诚度）、竞争品牌对比、差异化策略优先级排序。

**核心方法**:

| 方法 | 关键参数 | 说明 |
|------|----------|------|
| `set_awareness()` | `top_of_mind`, `aided_awareness`, `recognition`, `assessment` | 设置品牌知名度 |
| `add_association()` | `attribute`, `strength`(1-5), `uniqueness`(1-5), `favorability`(1-5) | 添加品牌联想 |
| `add_image_dimension()` | `dimension`, `score`, `competitor_scores`(Dict), `description` | 添加品牌形象维度 |
| `set_loyalty()` | `level`(1-5), `distribution`(Dict[int,float]) | 设置忠诚度层级 |
| `add_competitor_brand()` | `name`, `awareness`, `image_score`, `loyalty_level`, `key_strengths`, `key_weaknesses` | 添加竞争品牌 |
| `add_differentiation()` | `strategy_type`(产品/服务/品牌形象/客户体验差异化), `description`, `feasibility`, `impact`, `actions` | 添加差异化策略 |

**品牌忠诚度五层级**: 1-价格敏感型转换者、2-习惯性购买者、3-满意型购买者、4-情感型忠诚者、5-承诺型忠诚者

**示例**:

```python
skill.brand.set_awareness(top_of_mind=25.0, aided_awareness=75.0, recognition=90.0)
skill.brand.add_association("高品质", strength=4.5, uniqueness=3.5, favorability=4.0)
skill.brand.set_loyalty(level=3, distribution={1: 10, 2: 25, 3: 35, 4: 20, 5: 10})
skill.brand.add_competitor_brand("竞品A", awareness=30.0, image_score=4.0, loyalty_level=4,
    key_strengths=["创新能力强"], key_weaknesses=["价格偏高"])
skill.brand.add_differentiation("客户体验差异化", "全渠道无缝体验",
    feasibility=4.0, impact=4.5, actions=["统一会员", "价格同步"])
print(skill.brand.render_markdown())
```

### 8.4 完整报告生成

`ReportGenerator` 负责将各模块分析结果整合为十章完整研究报告。

**核心方法**:

| 方法 | 说明 |
|------|------|
| `set_executive_summary(summary)` | 设置执行摘要 |
| `set_company_overview(overview)` | 设置企业概况 |
| `add_section(chapter, content, sub_sections)` | 添加报告章节 |
| `add_module_output(module, markdown_output)` | 添加模块分析输出 |
| `add_finding(category, finding, severity, evidence, recommendation)` | 添加诊断发现 |
| `add_recommendation(title, description, timeframe, priority, actions)` | 添加战略建议 |
| `render_markdown()` / `render_json()` | 输出报告 |

通过 `skill.generate_full_report()` 可一键整合所有模块输出生成完整报告。

### 8.5 知识检索

```python
results = skill.search_knowledge("五力模型")
for r in results:
    print(f"[{r['topic']}] {r['section']}: {r['content'][:100]}...")

knowledge = skill.load_knowledge("strategy_capability")
all_knowledge = skill.load_all_knowledge()
```

可搜索的知识库主题：`macro_environment`, `industry_competition`, `strategy_capability`, `consumer_insight`, `loyalty_satisfaction`, `brand_value`, `thinking_models`, `strategy_matrices`, `business_frameworks`。

### 8.6 访谈问题生成

```python
all_questions = skill.get_interview_questions()
macro_questions = skill.get_interview_questions("macro_environment")
for q in macro_questions:
    print(f"- {q}")

checklist = skill.get_innovation_checklist()
for item in checklist:
    print(f"☐ {item}")
```

覆盖六大模块：宏观环境、行业竞争、企业战略、消费者洞察、客户忠诚度、品牌价值，每个模块5个标准问题。

### 8.7 完整使用示例

#### 示例1：快速企业诊断

```python
from skill01 import CompanyResearchSkill

skill = CompanyResearchSkill("星巴克中国", "餐饮连锁")

# 1. 宏观环境
skill.macro.add_factor("economic", "消费升级", "中产阶级扩大带动咖啡消费", score=4.5, weight=0.15, trend="上升")
skill.macro.add_factor("social", "咖啡文化", "年轻人咖啡消费习惯形成", score=4.0, weight=0.12, trend="上升")
skill.macro.add_factor("technological", "数字化点单", "移动支付和小程序普及", score=4.0, weight=0.10, trend="上升")
skill.macro.add_factor("political", "食品安全", "食品安全监管趋严", score=3.0, weight=0.08, trend="稳定")

# 2. 行业竞争
skill.industry.set_lifecycle_stage("growth")
skill.industry.add_force_driver("rivalry", "本土品牌崛起", "瑞幸等本土品牌快速扩张", score=4.5, weight=0.3)
skill.industry.add_force_driver("new_entrants", "低门槛", "精品咖啡店进入门槛降低", score=3.5, weight=0.2)
skill.industry.add_ksf("品牌溢价", weight=0.25, company_score=5.0, competitor_scores={"瑞幸": 2.5, "Manner": 3.0})
skill.industry.add_ksf("门店密度", weight=0.20, company_score=4.0, competitor_scores={"瑞幸": 5.0, "Manner": 3.0})

# 3. 战略分析
skill.strategy.add_swot_item("strengths", "全球品牌影响力", importance=5)
skill.strategy.add_swot_item("strengths", "第三空间体验", importance=5)
skill.strategy.add_swot_item("weaknesses", "价格敏感度高的市场适应性不足", importance=4)
skill.strategy.add_swot_item("opportunities", "下沉市场渗透空间大", importance=4)
skill.strategy.add_swot_item("threats", "本土品牌性价比优势", importance=5)

# 4. 消费者洞察
skill.consumer.add_value_score("质量", score=4.5, competitor_scores={"瑞幸": 3.5}, importance=5.0)
skill.consumer.add_value_score("设计/美学", score=5.0, competitor_scores={"瑞幸": 3.0}, importance=4.0)
skill.consumer.add_value_score("徽章价值", score=4.5, importance=3.5)
skill.consumer.add_value_score("归属感", score=4.0, importance=3.0)
skill.consumer.add_value_score("降低成本", score=2.0, competitor_scores={"瑞幸": 4.5}, importance=4.0)

# 5. 忠诚度
skill.loyalty.add_brand_ranking("星巴克中国", satisfaction_score=4.3, rank=1, brand_count=4)
skill.loyalty.add_brand_ranking("瑞幸", satisfaction_score=3.8, rank=2, brand_count=4)
skill.loyalty.add_competitive_loss("瑞幸", lost_customers=2000, lost_revenue=500000,
    reasons=["价格更低", "配送更快", "优惠券多"])

# 6. 品牌
skill.brand.set_awareness(top_of_mind=45.0, aided_awareness=95.0, recognition=98.0)
skill.brand.set_loyalty(level=4, distribution={1: 5, 2: 15, 3: 30, 4: 35, 5: 15})

# 7. 生成报告
skill.report.set_executive_summary("星巴克中国在品牌力和体验方面保持领先，但面临本土品牌在性价比和便捷性上的强力挑战。")
skill.report.add_finding("竞争", "本土品牌在价格和便捷性上形成显著优势", severity="高")
skill.report.add_finding("消费者", "在'降低成本'价值要素上显著落后于竞争对手", severity="高")
skill.report.add_recommendation("差异化体验升级", "强化第三空间体验，拉开与外卖咖啡的体验差距",
    timeframe="短期", priority="高", actions=["升级门店设计", "推出限定体验活动"])
skill.report.add_recommendation("数字化会员深耕", "通过会员体系提升复购和钱包份额",
    timeframe="中期", priority="高", actions=["优化积分体系", "个性化推荐"])

report = skill.generate_full_report()
print(report)
```

#### 示例2：投资尽调快速评估

```python
from skill01 import CompanyResearchSkill

skill = CompanyResearchSkill("目标企业", "新能源汽车")

# 快速五力评估
for force, name, desc, score in [
    ("rivalry", "竞争强度", "头部企业激烈竞争", 4.5),
    ("new_entrants", "新进入者", "跨界造车者众多", 4.0),
    ("substitutes", "替代品", "传统燃油车仍有市场", 3.0),
    ("buyer_power", "买方力量", "消费者选择多样", 4.0),
    ("supplier_power", "供应商力量", "电池供应商集中", 4.0),
]:
    skill.industry.add_force_driver(force, name, desc, score=score, weight=0.2)

# 快速SWOT
for q, items in {
    "strengths": ["技术积累深厚", "品牌认知度高", "供应链自主可控"],
    "weaknesses": ["盈利能力不足", "海外市场占比低"],
    "opportunities": ["政策补贴延续", "海外市场拓展", "智能化升级"],
    "threats": ["价格战加剧", "原材料成本波动", "技术路线不确定"],
}.items():
    for i, item in enumerate(items):
        skill.strategy.add_swot_item(q, item, importance=5-i)

# 快速价值要素评估
for elem, score in [("质量", 4.0), ("降低成本", 3.5), ("设计/美学", 4.5),
                     ("节省时间", 3.0), ("减少焦虑", 2.5), ("自我实现", 4.0)]:
    skill.consumer.add_value_score(elem, score=score, importance=4.0)

# 输出各模块报告
print(skill.industry.render_markdown())
print(skill.strategy.render_markdown())
print(skill.consumer.render_markdown())
```

### 8.8 AI Agent 调用规则

| 用户意图关键词 | 触发模块 | 调用方法 | 输出格式 |
|----------------|----------|----------|----------|
| 宏观环境/政策/经济/PEST | `skill.macro` | `add_factor()` → `render_markdown()` | PEST报告+EFE评分 |
| 行业竞争/五力/生命周期/KSF | `skill.industry` | `add_force_driver()` → `render_markdown()` | 五力报告+CPM矩阵 |
| SWOT/BCG/GE/价值链/7S/安索夫 | `skill.strategy` | `add_swot_item()` 等 → `render_markdown()` | 战略分析报告 |
| 消费者/价值要素/STP/4P | `skill.consumer` | `add_value_score()` → `render_markdown()` | 价值金字塔+STP报告 |
| 钱包份额/WAO/满意度/忠诚度/ICE | `skill.loyalty` | `add_brand_ranking()` → `render_markdown()` | WAO+忠诚度报告 |
| 品牌/知名度/联想/差异化 | `skill.brand` | `set_awareness()` 等 → `render_markdown()` | 品牌资产报告 |
| 完整报告/全面研究/尽调 | `skill` | 各模块填充 → `generate_full_report()` | 十章完整报告 |
| 框架/方法论/工具 | `skill` | `search_knowledge(keyword)` | 知识库搜索结果 |
| 访谈/问卷/调研 | `skill` | `get_interview_questions(module)` | 访谈问题列表 |

**调用流程规则**:

1. 识别用户意图，匹配上表中的触发模块
2. 如果用户提供了具体数据，直接调用对应方法填充数据
3. 如果用户未提供数据，先通过 `get_interview_questions()` 生成访谈提纲引导用户提供信息
4. 如果用户要求完整研究，按"由外而内"顺序依次执行：宏观→行业→战略→消费者→忠诚度→品牌→报告
5. 所有分析必须在竞争语境中进行，不能孤立评估

### 8.9 测试说明

测试文件位于 `skill01/tests/test_all.py`，包含 10 个独立测试用例：

| 测试用例 | 覆盖范围 |
|----------|----------|
| `test_company_research_skill_init` | 统一入口类初始化、配置验证、属性完整性 |
| `test_macro_analysis` | PESTEL因素添加、EFE评分、关键发现、Markdown/JSON输出 |
| `test_industry_analysis` | 五力模型、生命周期、CPM矩阵、竞争对手、KSF |
| `test_strategy_analysis` | SWOT+BCG+GE+价值链+7S+安索夫全流程 |
| `test_consumer_analysis` | 价值要素评分、STP、营销组合、NPS预测、行业标杆 |
| `test_brand_analysis` | 品牌资产四维评估、竞争品牌、差异化策略 |
| `test_loyalty_analysis` | WAO钱包份额、满意度驱动、客户分层、竞争流失、ICE |
| `test_full_report_generation` | 全模块整合、十章报告生成、诊断发现、战略建议 |
| `test_knowledge_search` | 知识库搜索、主题过滤、内容加载 |
| `test_interview_questions` | 访谈问题完整性、模块覆盖、创新检查清单 |

运行方式：`python3 skill01/tests/test_all.py`

### 8.10 与其他 Skill 的协作

skill01 可以与其他 Skill 协作，形成更完整的研究体系：

**与 JTBD Skill 协作**: 当需要深入理解消费者"为什么购买"时，skill01 的消费者洞察模块提供价值要素金字塔分析，JTBD Skill 提供"待完成工作"分析。两者结合可以从"消费者看重什么"和"消费者想完成什么任务"两个互补视角理解需求。

```python
# skill01 提供价值要素分析
skill01_result = skill.consumer.render_markdown()

# JTBD Skill 提供待完成工作分析
# jtbd_result = jtbd_skill.generate_analysis_report()

# 综合两个视角形成完整消费者洞察
```

**与定量用户研究 Skill 协作**: skill01 提供分析框架和方法论指引，定量研究 Skill 提供数据采集和统计分析能力。skill01 的访谈问题生成功能可以为定量研究提供问卷设计的基础。

**与价值主张设计 Skill 协作**: skill01 的品牌价值分析和消费者价值要素分析，可以为价值主张设计提供输入。品牌差异化策略的输出可以直接作为价值主张画布的参考。

## 九、最佳实践

### 9.1 研究流程

一个完整的企业研究项目应按以下流程推进，确保分析的系统性和逻辑连贯性：

**第一阶段：项目启动与范围界定（1-2天）**

明确研究目标（投资尽调、战略咨询、竞争分析等），确定研究范围和重点模块，识别关键信息来源，制定研究计划和时间表。使用 `skill.validate_config()` 验证配置完整性。

**第二阶段：外部环境扫描（2-3天）**

首先进行宏观环境分析（PESTEL），识别影响企业的关键外部因素和趋势。然后进行行业竞争格局分析（五力模型+行业生命周期），理解行业结构和竞争动态。这一阶段回答"企业所处的外部环境如何"的问题。

```python
skill.macro.add_factor(...)  # PESTEL各维度
skill.industry.set_lifecycle_stage(...)  # 行业生命周期
skill.industry.add_force_driver(...)  # 五力模型
skill.industry.add_ksf(...)  # 关键成功因素
```

**第三阶段：企业内部分析（3-5天）**

进行SWOT分析综合评估企业态势，用BCG/GE矩阵评估业务组合，用价值链分析识别竞争优势来源，用7S模型诊断组织能力。这一阶段回答"企业自身能力如何"的问题。

```python
skill.strategy.add_swot_item(...)  # SWOT
skill.strategy.add_business_unit(...)  # BCG
skill.strategy.add_value_chain_activity(...)  # 价值链
skill.strategy.add_seven_s(...)  # 7S
```

**第四阶段：消费者与品牌研究（3-5天）**

运用价值要素金字塔理解消费者价值感知，进行STP分析确定目标市场和定位，评估营销组合有效性，分析品牌资产和差异化策略。这一阶段回答"消费者如何看待企业"的问题。

```python
skill.consumer.add_value_score(...)  # 价值要素
skill.consumer.add_segment(...)  # STP
skill.brand.set_awareness(...)  # 品牌资产
skill.brand.add_differentiation(...)  # 差异化
```

**第五阶段：客户关系深度分析（2-3天）**

运用WAO钱包分配法则计算钱包份额，用Satisfactor识别满意度驱动因素，用Loyalty Optimizer进行客户分层，用ICE评估客户体验。这一阶段回答"客户关系健康度如何"的问题。

```python
skill.loyalty.add_brand_ranking(...)  # WAO
skill.loyalty.add_satisfaction_driver(...)  # Satisfactor
skill.loyalty.add_loyalty_segment(...)  # Loyalty Optimizer
skill.loyalty.add_ice_assessment(...)  # ICE
```

**第六阶段：综合诊断与报告（2-3天）**

整合各模块分析结果，提炼关键发现，形成综合诊断，制定战略建议，生成完整研究报告。

```python
skill.report.set_executive_summary(...)
skill.report.add_finding(...)
skill.report.add_recommendation(...)
report = skill.generate_full_report()
```

### 9.2 框架选用指南

面对不同的研究问题，应选择合适的分析框架组合：

**宏观层面问题**（"这个行业的未来趋势如何？"）: PESTEL分析 + 行业生命周期。PESTEL扫描外部环境的六个维度，行业生命周期判断行业所处阶段和未来走向。

**行业层面问题**（"这个行业好不好做？"）: 五力模型 + 战略集团分析 + 关键成功因素。五力模型评估行业结构和盈利潜力，战略集团分析识别行业内的竞争格局，KSF确定制胜的关键因素。

**企业层面问题**（"这家公司的战略对不对？"）: SWOT + BCG/GE矩阵 + 价值链 + 7S + 安索夫。SWOT综合评估态势，BCG/GE评估业务组合，价值链识别优势来源，7S诊断组织能力，安索夫指引增长方向。

**消费者层面问题**（"消费者为什么选择/不选择这个品牌？"）: 价值要素金字塔 + STP + 4P/4C。价值要素金字塔解构消费者价值感知，STP确定目标市场和定位，4P/4C评估营销组合。

**客户关系问题**（"客户忠诚度如何提升？"）: WAO钱包分配法则 + Satisfactor + Loyalty Optimizer + ICE。WAO计算钱包份额，Satisfactor识别驱动因素，Loyalty Optimizer分层管理，ICE优化体验。

**品牌问题**（"品牌价值如何提升？"）: 品牌资产模型 + 价值要素与品牌关系 + 差异化策略。品牌资产评估当前状态，价值要素分析消费者期望，差异化策略指引品牌建设方向。

### 9.3 常见错误与避免

**错误1：在真空中评估品牌表现**。许多研究者只关注自身品牌的满意度得分，而忽略了竞争品牌的表现。沃尔玛的案例已经证明，满意度上升并不意味着钱包份额上升。正确做法是始终在竞争语境中进行分析，关注排名而非绝对得分。

**错误2：混淆满意度驱动因素与不满意驱动因素**。满意的驱动因素和不满意的驱动因素往往是不同的。仅仅加强已有优势可能无法减少客户不满。正确做法是分别识别愉悦因素和不满因素，针对性制定改善策略。

**错误3：忽视价值要素的层次结构**。质量是所有价值要素的基础，在质量不达标的情况下，其他要素的优势无法弥补。正确做法是先确保基础层（功能价值）达标，再在情感和生活改变层面建立差异化。

**错误4：过度依赖单一框架**。没有任何一个框架能够完整描述企业的全貌。SWOT分析虽然经典但过于简化，五力模型虽然系统但忽略了合作关系。正确做法是多框架交叉验证，用不同工具从不同角度审视同一问题。

**错误5：框架分析流于形式**。列出SWOT四个象限的条目并不等于完成了战略分析。关键是从SWOT条目中推导出SO/WO/ST/WT组合策略，并转化为可执行的行动计划。正确做法是每一项分析都必须指向可执行的战略建议。

**错误6：忽略态度与行为的差距**。消费者声称重视的因素未必是实际驱动购买行为的因素。正确做法是将态度数据（满意度、推荐意愿）与行为数据（实际购买、钱包份额）结合分析。

**错误7：数据收集不充分就急于分析**。在信息不完整的情况下套用框架，会得出误导性的结论。正确做法是先通过 `get_interview_questions()` 生成访谈提纲，系统收集信息后再进行分析。

### 9.4 检查清单

完成一份企业研究报告前，请逐项检查以下要点：

**完整性检查**:
- [ ] 是否覆盖了六大研究模块（宏观环境、行业竞争、企业战略、消费者洞察、忠诚度、品牌）？
- [ ] 每个模块是否有足够的数据支撑（至少3个以上的分析因素）？
- [ ] 是否包含竞争对手的对比分析？
- [ ] 是否有明确的战略建议（短期+中期+长期）？

**逻辑性检查**:
- [ ] 分析是否按"由外而内"的逻辑顺序推进？
- [ ] 各模块的分析结论是否相互一致、逻辑自洽？
- [ ] 战略建议是否与分析发现直接对应？
- [ ] 是否避免了"在真空中评估"的错误？

**质量检查**:
- [ ] 价值要素分析是否在竞争语境中进行？
- [ ] WAO钱包份额是否正确计算？
- [ ] SWOT是否推导出了组合策略？
- [ ] 满意度驱动因素是否区分了愉悦因素和不满因素？

**可操作性检查**:
- [ ] 每一项战略建议是否有具体的行动计划？
- [ ] 建议是否标注了时间框架和优先级？
- [ ] 是否评估了建议的可行性和预期影响？
- [ ] 是否考虑了实施所需的资源和成本？

## 十、参考资料

### 10.1 核心书籍

《竞争战略》和《竞争优势》（迈克尔·波特）：五力模型、价值链分析、三种基本竞争战略的理论源头。任何行业分析和竞争策略制定都应以此为基础。

《战略管理：概念与案例》（弗雷德·大卫）：IE矩阵、EFE/IFE矩阵、大战略矩阵、CPM竞争态势矩阵等战略工具的系统阐述。

《The Elements of Value》（Bain & Company, HBR 2016）：消费者价值要素金字塔的原始研究，识别出30个价值要素和四个层次，以及价值要素与NPS、收入增长的定量关系。

《The Wallet Allocation Rule》：钱包分配法则的完整理论，证明了排名比满意度更能预测钱包份额，相关性从0.1提升到0.9。

《追求卓越》（汤姆·彼得斯）：麦肯锡7S模型的来源，从战略、结构、制度、风格、人员、技能、共同价值观七个维度诊断组织能力。

《蓝海战略》（金伟灿、勒妮·莫博涅）：超越竞争的战略思维，价值创新和战略画布工具。

《定位》（艾尔·里斯、杰克·特劳特）：市场定位理论的经典著作，STP分析的理论基础。

### 10.2 在线资源

MBA智库百科（wiki.mbalib.com）：中文商业管理知识库，涵盖100+思维模型和分析工具的详细解释和应用案例。

Harvard Business Review（hbr.org）：Elements of Value系列研究的原始发表平台，持续更新的管理学前沿研究。

McKinsey Quarterly（mckinsey.com）：麦肯锡季刊，7S模型、增长战略等框架的实践应用案例。

### 10.3 相关 Skill

| Skill | 协作方式 |
|-------|----------|
| JTBD Knowledge Skill | 消费者需求的互补视角：skill01提供"消费者看重什么"，JTBD提供"消费者想完成什么任务" |
| Quantitative UX Research | skill01提供分析框架，定量研究提供数据采集和统计分析能力 |
| Value Proposition Design | skill01的品牌价值和消费者价值分析为价值主张设计提供输入 |
| Deep Research | 当需要收集企业公开信息时，可调用Deep Research进行信息采集 |
