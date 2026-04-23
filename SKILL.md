---
name: structured-thinking-model
description: 结构化商业分析工具集。提供 PESTEL、五力模型、SWOT、BCG、GE 矩阵、价值要素金字塔、WAO 钱包分配法则等 20+ 个分析框架的可执行 Python 实现，支持宏观环境、行业竞争、企业战略、消费者洞察、客户忠诚度、品牌价值六大模块的量化分析与报告生成，并自动附加CEO执行摘要、失败场景分析与资源分配建议。附带 11 篇方法论知识库（含 49 个商业框架速查）和访谈提纲生成能力。适用于战略咨询、竞争分析、投资尽调、品牌诊断、消费者研究等场景。
---

# 结构化思维工具集

一套结构化的商业分析工具，帮助你面对复杂问题时快速匹配合适的分析框架，完成从问题拆解到量化输出的全过程。

核心理念：**问题决定工具，而不是工具决定问题。**

## 触发条件

| 用户意图关键词 | 调用模块 | 核心方法 | 输出 |
|----------------|----------|----------|------|
| 宏观环境/政策/经济/PEST | `skill.macro` | `add_factor()` → `render_markdown()` | PEST报告 + EFE评分 |
| 行业竞争/五力/生命周期/KSF | `skill.industry` | `add_force_driver()` → `render_markdown()` | 五力报告 + CPM矩阵 |
| SWOT/BCG/GE/价值链/7S/安索夫 | `skill.strategy` | `add_swot_item()` 等 → `render_markdown()` | 战略分析报告 |
| 消费者/价值要素/STP/4P | `skill.consumer` | `add_value_score()` → `render_markdown()` | 价值金字塔 + STP |
| 钱包份额/WAO/满意度/忠诚度/ICE | `skill.loyalty` | `add_brand_ranking()` → `render_markdown()` | WAO + 忠诚度报告 |
| 品牌/知名度/联想/差异化 | `skill.brand` | `set_awareness()` 等 → `render_markdown()` | 品牌资产报告 |
| 完整报告/全面研究/尽调 | `skill` | 各模块填充 → `generate_full_report()` | 十章完整报告 |
| 框架/方法论/工具 | `skill` | `search_knowledge(keyword)` | 知识库搜索结果 |
| 访谈/问卷/调研 | `skill` | `get_interview_questions(module)` | 访谈问题列表 |
| CEO 摘要、执行摘要、战略健康 | `skill.report` | `generate_ceo_executive_summary()` | CEO 执行摘要 + 战略健康评分 |
| 失败场景、Pre-Mortem、风险分析 | `skill.report` | `generate_failure_scenarios()` | 失败场景表 + 应对预案 |
| 资源分配、预算、人力配置 | `skill.report` | `generate_resource_allocation()` | 资金/人才/时间三维分配 |

**不适用场景**: 纯概念解释（如"什么是五力模型"）无需启动分析流程，直接用 `search_knowledge()` 检索知识库即可；非商业分析类问题不在本工具覆盖范围内。

## 调用流程

1. 识别用户意图，匹配上表中的触发模块
2. 如果用户提供了具体数据，直接调用对应方法填充数据
3. 如果用户未提供数据，先通过 `get_interview_questions()` 生成访谈提纲引导用户提供信息
4. 如果用户要求完整研究，按"由外而内"顺序依次执行：宏观 → 行业 → 战略 → 消费者 → 忠诚度 → 品牌 → 报告
5. 所有分析必须在竞争语境中进行，不能孤立评估

## 分析模块

所有模块通过统一入口类 `CompanyResearchSkill` 访问，支持 `render_markdown()` 和 `render_json()` 两种输出格式。完整 API 详见 [api-reference.md](references/api-reference.md)。

```python
from skill01 import CompanyResearchSkill
skill = CompanyResearchSkill("目标公司", "所属行业")
```

### 宏观环境分析（MacroAnalyzer）

分析企业所处的政治、经济、社会、技术、环境、法律等宏观因素。输出 PESTEL 报告和 EFE 加权评分。

```python
skill.macro.add_factor("economic", "消费升级", "中产阶级扩大", score=4.5, weight=0.15, trend="上升")
skill.macro.add_factor("technological", "AI技术", "人工智能加速渗透", score=4.0, weight=0.13, trend="上升")
print(skill.macro.render_markdown())
```

### 行业竞争格局（IndustryAnalyzer）

分析行业竞争结构（五力模型）、关键成功因素（CPM矩阵）、行业生命周期。

```python
skill.industry.set_lifecycle_stage("growth")
skill.industry.add_force_driver("rivalry", "本土品牌崛起", "竞争加剧", score=4.5, weight=0.3)
skill.industry.add_ksf("品牌溢价", weight=0.25, company_score=5.0, competitor_scores={"竞品A": 2.5})
print(skill.industry.render_markdown())
```

### 企业战略与能力（StrategyAnalyzer）

SWOT 态势分析、BCG 业务组合、GE 矩阵、价值链、7S 组织诊断、安索夫增长方向。

```python
skill.strategy.add_swot_item("strengths", "全球品牌影响力", importance=5)
skill.strategy.add_swot_item("threats", "本土品牌性价比优势", importance=5)
skill.strategy.add_business_unit("核心业务", market_growth_rate=15.0, relative_market_share=1.5)
print(skill.strategy.render_markdown())
```

### 消费者洞察（ConsumerAnalyzer）

价值要素金字塔（30 个要素、四个层次）、STP 市场细分与定位、4P/4C/4R 营销组合评估、NPS 预测。

```python
skill.consumer.add_value_score("质量", score=4.5, competitor_scores={"竞品A": 3.5}, importance=5.0)
skill.consumer.add_segment("年轻白领", size="3000万", growth="15%", is_target=True)
skill.consumer.set_positioning("年轻白领", "高品质生活方式", "天然健康")
print(skill.consumer.render_markdown())
```

### 客户满意度与忠诚度（LoyaltyAnalyzer）

WAO 钱包分配法则、Satisfactor 满意度驱动、Loyalty Optimizer 客户分层、ICE 体验评估。

核心洞察：满意度与钱包份额相关性仅 0.1，排名与钱包份额相关性高达 0.9。

```python
skill.loyalty.add_brand_ranking("目标公司", satisfaction_score=4.2, rank=1, brand_count=5)
skill.loyalty.add_satisfaction_driver("服务响应速度", importance=4.5, performance=3.0, is_dissatisfaction=True)
print(f"钱包份额: {skill.loyalty.get_company_wallet_share():.1%}")
print(skill.loyalty.render_markdown())
```

### 品牌价值（BrandAnalyzer）

品牌资产四维评估（知名度、联想、形象、忠诚度）、竞争品牌对比、差异化策略优先级排序。

```python
skill.brand.set_awareness(top_of_mind=25.0, aided_awareness=75.0, recognition=90.0)
skill.brand.add_association("高品质", strength=4.5, uniqueness=3.5, favorability=4.0)
skill.brand.add_differentiation("客户体验差异化", "全渠道无缝体验", feasibility=4.0, impact=4.5)
print(skill.brand.render_markdown())
```

### 综合报告生成

一键整合所有模块输出，生成十章完整研究报告。

```python
skill.report.set_executive_summary("目标公司在品牌力方面保持领先，但面临...")
skill.report.add_finding("竞争", "本土品牌在价格和便捷性上形成显著优势", severity="高")
skill.report.add_recommendation("差异化体验升级", "强化体验差距", timeframe="短期", priority="高")
print(skill.generate_full_report())
```

> **注意**: `generate_full_report()` 自动包含 CEO 执行摘要、失败场景分析和资源分配建议，无需额外调用。

### 知识库检索与访谈提纲

```python
# 搜索分析框架的方法论
results = skill.search_knowledge("五力模型")

# 加载完整知识文档
knowledge = skill.load_knowledge("strategy_capability")

# 生成访谈问题（引导用户提供分析所需信息）
questions = skill.get_interview_questions("consumer_insight")
```

## 知识库索引

references 目录下的 11 篇文档构成方法论知识库，覆盖 49 个商业分析框架：

| 主题 | 文件 | 涵盖框架 |
|------|------|----------|
| 宏观环境 | [macro-environment.md](references/macro-environment.md) | PEST/PESTEL、EFE 矩阵 |
| 行业竞争 | [industry-competition.md](references/industry-competition.md) | 五力模型、战略集团、行业生命周期、CPM |
| 企业战略 | [strategy-capability.md](references/strategy-capability.md) | SWOT、BCG、GE、价值链、7S、安索夫、蓝海战略 |
| 消费者洞察 | [consumer-insight.md](references/consumer-insight.md) | 价值要素金字塔、STP、4P/4C/4R、客户旅程地图 |
| 客户忠诚度 | [loyalty-satisfaction.md](references/loyalty-satisfaction.md) | WAO、Satisfactor、Loyalty Optimizer、ICE、CLV |
| 品牌价值 | [brand-value.md](references/brand-value.md) | 品牌资产模型、差异化策略、品牌定位方法论 |
| 思维决策 | [thinking-models.md](references/thinking-models.md) | 六顶思考帽、KT 决策法、平衡计分卡、PDCA |
| 战略矩阵 | [strategy-matrices.md](references/strategy-matrices.md) | IE 矩阵、定向政策矩阵、大战略矩阵 |
| 框架速查 | [business-frameworks.md](references/business-frameworks.md) | 49 个商业框架索引（含商业模式画布、精益画布、OKR 等） |
| API 参考 | [api-reference.md](references/api-reference.md) | 完整的 Python API 方法签名与参数说明 |
| 最佳实践 | [best-practices.md](references/best-practices.md) | 研究流程、框架选用指南、常见错误、检查清单 |

## CEO 决策视角

完整报告（`generate_full_report()`）自动包含以下 CEO 决策模块，无需额外调用：

**CEO 执行摘要** — 基于所有模块的诊断发现和战略建议，自动计算战略健康评分(0-100)，输出 Top 3 优先事项、主要风险和关键决策点。评分标准：≥70 良好 / 40-69 需关注 / <40 预警。

**失败场景分析** — 运用 Pre-Mortem 逆向反思法，假设战略已失败，从高优先级发现和建议中推演可能的失败场景（概率/影响/触发条件/应对措施），为高影响场景提供专项预案。

**资源分配建议** — 基于战略优先级，按资金、人才、时间三个维度提出配置建议。遵循四项原则：优先保障短期行动、预留 20% 探索资源、人才先于资金、季度复盘动态调整。

**自动行为**: `generate_full_report()` 自动包含以上三个 CEO 决策模块。也可单独调用：

```python
# 单独调用 CEO 方法
ceo_summary = skill.report.generate_ceo_executive_summary()
failure_analysis = skill.report.generate_failure_scenarios()
resource_plan = skill.report.generate_resource_allocation()

# 自定义失败场景
skill.report.add_failure_scenario("竞品先发优势", probability="高", impact="高", 
    trigger="竞品发布类似产品", mitigation="差异化策略+快速迭代")
```

**默认行为**: 任何涉及完整分析或战略评估的任务，都应使用 `generate_full_report()` 以确保包含 CEO 决策视角。

## 核心原则

运用这套工具时，需遵循以下原则：

1. **由外而内**: 先理解宏观环境与行业格局，再深入企业内部
2. **竞争视角**: 一切分析必须置于竞争语境中，孤立评价毫无意义
3. **消费者导向**: 最终价值由消费者定义，所有分析回归消费者需求
4. **数据驱动**: 定性洞察必须有定量验证，避免主观臆断
5. **行动导向**: 每一项分析必须指向可执行的战略建议

## 与其他 Skill 的协作

本工具提供"结构化思考的框架"，可与其他领域 Skill 组合使用：

- **JTBD Knowledge Skill**: 互补视角——本工具分析"消费者看重什么"，JTBD 分析"消费者想完成什么任务"
- **Quantitative UX Research**: 本工具提供分析框架和研究设计，定量研究提供数据采集和统计验证
- **Value Proposition Design**: 消费者洞察和品牌分析的输出可直接作为价值主张设计的输入
- **Deep Research**: 当需要收集公开信息时，用 Deep Research 采集数据，再用本工具做结构化分析

### AI Agent 调用规则

| # | 规则 | 说明 |
|---|------|------|
| 1 | **统一入口** | 始终通过 `CompanyResearchSkill` 类调用 |
| 2 | **由外而内** | 分析顺序：宏观→行业→战略→消费者→忠诚度→品牌→报告 |
| 3 | **竞争视角** | 一切分析在竞争语境中进行，不孤立评估 |
| 4 | **知识优先** | 理论问题先调用 `search_knowledge()` 查询 |
| 5 | **CEO 决策自动包含** | 使用 `generate_full_report()` 即自动包含 CEO 执行摘要 + 失败场景 + 资源分配 |
| 6 | **完整交付** | 综合分析任务使用 `generate_full_report()`，确保十章完整报告含 CEO 决策 |

## 理论基础

方法论来源：《竞争战略》与《竞争优势》（波特）、《战略管理：概念与案例》（弗雷德·大卫）、The Elements of Value（Bain & Company, HBR 2016）、The Wallet Allocation Rule、《追求卓越》（彼得斯）、《蓝海战略》（金伟灿）、《定位》（里斯 & 特劳特）。
