# API 参考文档

本文档是 skill01 Python 工具包的完整 API 参考。统一入口类 `CompanyResearchSkill` 封装了全部分析能力。

## CompanyResearchSkill 统一入口类

```python
from skill01 import CompanyResearchSkill
skill = CompanyResearchSkill("目标公司", "所属行业")
```

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

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `search_knowledge(keyword, topics)` | `List[Dict]` | 搜索知识库 |
| `load_knowledge(topic)` | `str` | 加载指定主题知识 |
| `load_all_knowledge()` | `Dict[str, str]` | 加载全部知识库 |
| `get_interview_questions(module)` | `List[str]` 或 `Dict` | 获取访谈问题 |
| `get_innovation_checklist()` | `List[str]` | 获取创新检查清单 |
| `generate_full_report()` | `str` | 生成完整研究报告 |
| `validate_config()` | `List[str]` | 验证配置，返回错误列表 |

## MacroAnalyzer — 宏观环境分析

分析企业所处的政治、经济、社会、技术、环境、法律等宏观因素，评估外部环境的机会与威胁。

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `add_factor()` | `dimension`(str), `name`(str), `description`(str), `score`(float,1-5), `weight`(float,0-1), `trend`(str), `impact`(str) | `MacroAnalyzer` | 添加PEST因素 |
| `add_factors_batch()` | `factors`(List[Dict]) | `MacroAnalyzer` | 批量添加因素 |
| `get_key_findings()` | 无 | `List[str]` | 获取关键发现 |
| `get_implications()` | 无 | `List[str]` | 获取战略启示 |
| `render_markdown()` | 无 | `str` | 输出Markdown报告 |
| `render_json()` | 无 | `str` | 输出JSON数据 |

- **dimension**: `political`, `economic`, `social`, `technological`, `environmental`, `legal`
- **trend**: `上升`, `稳定`, `下降`

```python
skill.macro.add_factor("political", "产业政策", "政府支持力度加大", score=4.0, weight=0.15, trend="上升")
skill.macro.add_factor("economic", "GDP增长", "经济增速放缓", score=3.0, weight=0.12, trend="下降")
print(skill.macro.render_markdown())
```

## IndustryAnalyzer — 行业竞争格局分析

分析行业竞争结构、竞争强度、关键成功因素、行业生命周期阶段，评估行业吸引力。

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `set_lifecycle_stage()` | `stage`(str) | `IndustryAnalyzer` | 设置行业生命周期阶段 |
| `add_force_driver()` | `force`(str), `name`(str), `description`(str), `score`(float), `weight`(float) | `IndustryAnalyzer` | 添加五力驱动因素 |
| `add_competitor()` | `name`(str), `market_share`(float), `strengths`(List), `weaknesses`(List), `strategy`(str) | `IndustryAnalyzer` | 添加竞争对手 |
| `add_ksf()` | `name`(str), `weight`(float), `company_score`(float), `competitor_scores`(Dict) | `IndustryAnalyzer` | 添加关键成功因素 |
| `render_markdown()` / `render_json()` | 无 | `str` | 输出报告 |

- **force**: `new_entrants`, `substitutes`, `supplier_power`, `buyer_power`, `rivalry`
- **stage**: `introduction`, `growth`, `maturity`, `decline`

```python
skill.industry.set_lifecycle_stage("maturity")
skill.industry.add_force_driver("rivalry", "竞争者数量", "行业内超过10家主要企业", score=4.0, weight=0.3)
skill.industry.add_ksf("品牌知名度", weight=0.2, company_score=4.0, competitor_scores={"竞品A": 4.5})
print(skill.industry.render_markdown())
```

## StrategyAnalyzer — 企业战略与能力分析

评估企业战略选择、业务组合健康度、内部能力、组织协调性、增长方向。

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

```python
skill.strategy.add_swot_item("strengths", "品牌知名度高", importance=5)
skill.strategy.add_swot_strategy("SO", "利用品牌优势拓展下沉市场", actions=["开设社区店", "发展加盟"])
skill.strategy.add_business_unit("核心零售", market_growth_rate=5.0, relative_market_share=1.5)
print(skill.strategy.render_markdown())
```

## ConsumerAnalyzer — 消费者洞察分析

理解消费者价值感知结构、市场细分与定位、营销组合评估，识别高价值要素和NPS预测。

| 方法 | 关键参数 | 说明 |
|------|----------|------|
| `add_value_score()` | `element`(30个价值要素之一), `score`(1-5), `competitor_scores`(Dict), `importance`(float) | 添加价值要素评分 |
| `add_segment()` | `name`, `size`, `growth`, `characteristics`(List), `needs`(List), `is_target`(bool) | 添加市场细分 |
| `set_positioning()` | `target_segment`, `value_proposition`, `differentiation`, `reason_to_believe` | 设置市场定位 |
| `add_marketing_mix()` | `dimension`(产品/价格/渠道/促销/消费者需求/成本/便利性/沟通/关联/反应/关系/回报), `assessment`, `score`, `recommendations`(List) | 添加营销组合评估 |
| `get_nps_prediction()` | 无 | NPS预测 |
| `render_markdown()` / `render_json()` | 无 | 输出报告 |

30个价值要素按金字塔层次分布：功能价值（节省时间、减少努力、简化流程、避免麻烦、赚钱、降低成本、降低风险、质量、组织整理、多样性、整合连接、感官体验、联结沟通、信息告知），情感价值（减少焦虑、健康/保健、奖励自我、治愈价值、怀旧感、趣味/娱乐、设计/美学、徽章价值、吸引力、提供接触渠道），改变生活价值（提供希望、自我激励、自我实现、传承价值、归属感），社会影响价值（自我超越）。

```python
skill.consumer.add_value_score("质量", score=4.5, competitor_scores={"竞品A": 4.0}, importance=5.0)
skill.consumer.add_segment("年轻白领", size="3000万", growth="15%", is_target=True)
skill.consumer.set_positioning("年轻白领", "高品质健康生活", "天然有机原料")
print(skill.consumer.render_markdown())
```

## LoyaltyAnalyzer — 客户满意度与忠诚度分析

分析客户钱包份额（WAO法则）、满意度驱动因素（Satisfactor）、忠诚度分层（Loyalty Optimizer）、客户体验（ICE）、竞争流失分析。

| 方法 | 关键参数 | 说明 |
|------|----------|------|
| `add_brand_ranking()` | `brand`, `satisfaction_score`, `rank`, `brand_count` | 添加品牌排名（自动计算WAO钱包份额） |
| `add_satisfaction_driver()` | `name`, `importance`, `performance`, `is_delight`, `is_dissatisfaction` | 添加满意度驱动因素 |
| `add_loyalty_segment()` | `segment_type`(core/high_value_at_risk/low_value_at_risk/low_value_satisfied), `count`, `percentage`, `strategy` | 添加客户分层 |
| `add_competitive_loss()` | `competitor`, `lost_customers`, `lost_revenue`, `reasons`(List), `recovery_cost` | 添加竞争流失 |
| `add_ice_assessment()` | `dimension`(接触点/情境/感觉/区段/地理/时间), `current_score`, `target_score`, `gap_description`, `improvement_actions` | 添加ICE评估 |
| `get_company_wallet_share()` | 无 | 获取企业钱包份额 |
| `render_markdown()` / `render_json()` | 无 | 输出报告 |

WAO核心公式: `钱包份额 = (1 - 排名/(品牌数量+1)) × (2/品牌数量)`

```python
skill.loyalty.add_brand_ranking("目标公司", satisfaction_score=4.2, rank=1, brand_count=5)
skill.loyalty.add_satisfaction_driver("服务响应速度", importance=4.5, performance=3.0, is_dissatisfaction=True)
print(skill.loyalty.render_markdown())
```

## BrandAnalyzer — 品牌价值分析

评估品牌资产（知名度、联想、形象、忠诚度）、竞争品牌对比、差异化策略优先级排序。

| 方法 | 关键参数 | 说明 |
|------|----------|------|
| `set_awareness()` | `top_of_mind`, `aided_awareness`, `recognition`, `assessment` | 设置品牌知名度 |
| `add_association()` | `attribute`, `strength`(1-5), `uniqueness`(1-5), `favorability`(1-5) | 添加品牌联想 |
| `add_image_dimension()` | `dimension`, `score`, `competitor_scores`(Dict), `description` | 添加品牌形象维度 |
| `set_loyalty()` | `level`(1-5), `distribution`(Dict[int,float]) | 设置忠诚度层级 |
| `add_competitor_brand()` | `name`, `awareness`, `image_score`, `loyalty_level`, `key_strengths`, `key_weaknesses` | 添加竞争品牌 |
| `add_differentiation()` | `strategy_type`(产品/服务/品牌形象/客户体验差异化), `description`, `feasibility`, `impact`, `actions` | 添加差异化策略 |
| `render_markdown()` / `render_json()` | 无 | 输出报告 |

品牌忠诚度五层级: 1-价格敏感型转换者、2-习惯性购买者、3-满意型购买者、4-情感型忠诚者、5-承诺型忠诚者

```python
skill.brand.set_awareness(top_of_mind=25.0, aided_awareness=75.0, recognition=90.0)
skill.brand.add_association("高品质", strength=4.5, uniqueness=3.5, favorability=4.0)
skill.brand.add_differentiation("客户体验差异化", "全渠道无缝体验", feasibility=4.0, impact=4.5)
print(skill.brand.render_markdown())
```

## ReportGenerator — 综合报告生成

将各模块分析结果整合为十章完整研究报告。

| 方法 | 说明 |
|------|------|
| `set_executive_summary(summary)` | 设置执行摘要 |
| `set_company_overview(overview)` | 设置企业概况 |
| `add_section(chapter, content, sub_sections)` | 添加报告章节 |
| `add_finding(category, finding, severity, evidence, recommendation)` | 添加诊断发现 |
| `add_recommendation(title, description, timeframe, priority, actions)` | 添加战略建议 |
| `render_markdown()` / `render_json()` | 输出报告 |

通过 `skill.generate_full_report()` 可一键整合所有模块输出生成完整报告。

## 知识库检索

```python
# 关键词搜索
results = skill.search_knowledge("五力模型")
for r in results:
    print(f"[{r['topic']}] {r['section']}: {r['content'][:100]}...")

# 加载特定主题
knowledge = skill.load_knowledge("strategy_capability")

# 加载全部
all_knowledge = skill.load_all_knowledge()
```

可搜索的知识库主题: `macro_environment`, `industry_competition`, `strategy_capability`, `consumer_insight`, `loyalty_satisfaction`, `brand_value`, `thinking_models`, `strategy_matrices`, `business_frameworks`

## 访谈问题生成

```python
all_questions = skill.get_interview_questions()
macro_questions = skill.get_interview_questions("macro_environment")
checklist = skill.get_innovation_checklist()
```

覆盖六大模块：宏观环境、行业竞争、企业战略、消费者洞察、客户忠诚度、品牌价值，每个模块5个标准问题。

## 相关文档

- [strategy-capability.md](strategy-capability.md) — SWOT、BCG、价值链等战略分析框架的方法论详解
- [consumer-insight.md](consumer-insight.md) — 价值要素金字塔、STP 理论基础
- [loyalty-satisfaction.md](loyalty-satisfaction.md) — WAO 公式推导和 ICE 体验框架详解
- [best-practices.md](best-practices.md) — 研究流程、框架选用指南、常见错误
