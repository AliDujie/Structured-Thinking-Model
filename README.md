# Structured-Thinking-Model

一套结构化思维工具集，帮你在面对复杂商业问题时，快速找到合适的分析框架，构建清晰的研究思路。

不同于传统的"方法论手册"，这个 Skill 把经典的咨询分析框架封装成了可执行的 Python 工具和可检索的知识库。你不需要记住每个框架的细节——只需要描述你面对的问题，它会帮你匹配合适的结构化思维工具，引导你完成从问题拆解到分析输出的全过程。

## 它能解决什么问题

当你遇到以下这类问题时，这套工具可以帮上忙：

- **"这个行业值不值得进入？"** → 调用 PESTEL 扫描宏观环境，用五力模型评估行业结构，用生命周期判断发展阶段
- **"我们的战略方向对不对？"** → 用 SWOT 梳理态势，BCG/GE 矩阵审视业务组合，价值链定位优势来源，7S 诊断组织协调性
- **"消费者到底看重什么？"** → 用价值要素金字塔（30 个要素、四个层次）解构消费者价值感知，STP 锁定目标市场
- **"客户为什么在流失？"** → 用 WAO 钱包分配法则计算真实份额，Satisfactor 识别驱动因素，ICE 评估体验差距
- **"品牌该往哪个方向走？"** → 品牌资产四维评估，竞争品牌对比，差异化策略优先级排序
- **"需要一份完整的企业调研报告"** → 按"由外而内"的逻辑，串联以上所有工具，生成十章完整报告

核心理念很简单：**问题决定工具，而不是工具决定问题。**

## 工具全景

### 五层分析工具体系

```
┌─────────────────────────────────────────────────────┐
│  第五层：决策与思维工具                                │
│  六顶思考帽 · KT决策法 · 5W2H · 平衡计分卡 · PDCA     │
├─────────────────────────────────────────────────────┤
│  第四层：客户忠诚度工具                                │
│  WAO钱包分配法则 · Satisfactor · Loyalty Optimizer     │
│  ICE完美顾客体验 · Rewards Optimizer                   │
├─────────────────────────────────────────────────────┤
│  第三层：消费者与品牌工具                               │
│  价值要素金字塔(30要素) · STP · 4P/4C/4R · 品牌资产     │
├─────────────────────────────────────────────────────┤
│  第二层：企业战略工具                                   │
│  SWOT · BCG · GE矩阵 · 价值链 · 核心竞争力 · 安索夫 · 7S │
├─────────────────────────────────────────────────────┤
│  第一层：宏观与行业工具                                 │
│  PEST/PESTEL · 波特五力 · 行业生命周期 · 战略集团        │
└─────────────────────────────────────────────────────┘
```

### 问题 → 工具速查

| 你的问题 | 推荐工具 | 对应模块 |
|----------|----------|----------|
| 外部环境和趋势怎么样？ | PESTEL + EFE 矩阵 | `MacroAnalyzer` |
| 行业好不好做？竞争激不激烈？ | 五力模型 + CPM + 行业生命周期 | `IndustryAnalyzer` |
| 企业自身能力和战略选择？ | SWOT + BCG + GE + 价值链 + 7S + 安索夫 | `StrategyAnalyzer` |
| 消费者真正看重什么？ | 价值要素金字塔 + STP + 4P/4C/4R | `ConsumerAnalyzer` |
| 客户满意度和钱包份额？ | WAO + Satisfactor + ICE | `LoyaltyAnalyzer` |
| 品牌价值和差异化方向？ | 品牌资产模型 + 差异化策略 | `BrandAnalyzer` |
| 需要完整研究报告？ | 全模块串联 | `generate_full_report()` |
| 想查某个框架的方法论？ | 知识库检索 | `search_knowledge()` |

## 项目结构

```
Structured-Thinking-Model/
├── SKILL.md                  # Skill 主文件（AI Agent 读取入口）
├── pyproject.toml            # Python 包配置
├── requirements.txt          # 依赖说明（仅标准库）
├── references/               # 方法论知识库（9 篇）
│   ├── macro-environment.md      # PEST/PESTEL 分析框架
│   ├── industry-competition.md   # 五力模型、战略集团、行业生命周期
│   ├── strategy-capability.md    # SWOT、BCG、GE、价值链、7S、安索夫
│   ├── consumer-insight.md       # 价值要素金字塔、STP、4P/4C/4R
│   ├── loyalty-satisfaction.md   # WAO、Satisfactor、Loyalty Optimizer、ICE
│   ├── brand-value.md            # 品牌资产模型、差异化策略
│   ├── thinking-models.md        # 六顶思考帽、KT 决策法、平衡计分卡等
│   ├── strategy-matrices.md      # IE 矩阵、定向政策矩阵、大战略矩阵
│   ├── business-frameworks.md    # 49 个商业框架速查索引
│   ├── api-reference.md          # Python API 完整参考文档
│   └── best-practices.md         # 研究流程、框架选用、常见错误
└── skill01/                  # Python 可执行工具包
    ├── __init__.py               # 统一入口 CompanyResearchSkill
    ├── base_analyzer.py          # 分析器抽象基类
    ├── config.py                 # 全局配置与模块定义
    ├── macro_analyzer.py         # 宏观环境分析器
    ├── industry_analyzer.py      # 行业竞争分析器
    ├── strategy_analyzer.py      # 企业战略分析器
    ├── consumer_analyzer.py      # 消费者洞察分析器
    ├── loyalty_analyzer.py       # 客户忠诚度分析器
    ├── brand_analyzer.py         # 品牌价值分析器
    ├── report_generator.py       # 综合报告生成器
    ├── templates.py              # 访谈问题与创新检查清单
    ├── utils.py                  # 知识库加载与搜索工具
    └── tests/
        └── test_all.py           # 16 个测试用例
```

## 安装

skill01 仅使用 Python 标准库，Python >= 3.8 即可运行，无需安装第三方依赖。

```bash
git clone https://github.com/AliDujie/Structured-Thinking-Model.git
cd Structured-Thinking-Model
pip install -e .
```

作为 AI Agent Skill 使用时，将整个目录复制到 skills 目录下即可（如 `~/.agents/skills/`）。

## 使用示例

### 示例 1：回答一个具体问题

"咖啡行业的竞争结构怎么样？值不值得进入？"——只需要调用行业分析模块：

```python
from skill01 import CompanyResearchSkill

skill = CompanyResearchSkill("新品牌", "咖啡连锁")

# 用五力模型拆解行业竞争结构
skill.industry.set_lifecycle_stage("growth")
skill.industry.add_force_driver("rivalry", "本土品牌崛起", "瑞幸等快速扩张", score=4.5, weight=0.3)
skill.industry.add_force_driver("new_entrants", "进入门槛低", "精品咖啡店遍地开花", score=3.5, weight=0.2)
skill.industry.add_force_driver("substitutes", "替代品多", "茶饮、便利店咖啡", score=3.0, weight=0.2)

# 关键成功因素对比
skill.industry.add_ksf("品牌溢价", weight=0.25,
    company_score=2.0, competitor_scores={"星巴克": 5.0, "瑞幸": 2.5})
skill.industry.add_ksf("门店密度", weight=0.20,
    company_score=1.0, competitor_scores={"星巴克": 4.0, "瑞幸": 5.0})

print(skill.industry.render_markdown())
```

### 示例 2：串联多个工具做完整研究

当问题更复杂时，可以按需组合多个工具：

```python
skill = CompanyResearchSkill("星巴克中国", "餐饮连锁")

# 宏观环境 → 行业竞争 → 战略 → 消费者 → 忠诚度 → 品牌
skill.macro.add_factor("economic", "消费升级", "中产阶级扩大", score=4.5, weight=0.15, trend="上升")
skill.industry.add_force_driver("rivalry", "竞争加剧", "本土品牌崛起", score=4.5, weight=0.3)
skill.strategy.add_swot_item("strengths", "全球品牌影响力", importance=5)
skill.consumer.add_value_score("质量", score=4.5, competitor_scores={"瑞幸": 3.5}, importance=5.0)
skill.loyalty.add_brand_ranking("星巴克中国", satisfaction_score=4.3, rank=1, brand_count=4)
skill.brand.set_awareness(top_of_mind=45.0, aided_awareness=95.0, recognition=98.0)

# 一键生成完整报告
skill.report.set_executive_summary("星巴克中国在品牌力和体验方面保持领先...")
print(skill.generate_full_report())
```

### 示例 3：不知道该用什么框架？查知识库

```python
# 关键词搜索，找到相关的分析框架和方法论
results = skill.search_knowledge("客户流失")
for r in results:
    print(f"[{r['topic']}] {r['section']}: {r['content'][:80]}...")

# 加载完整的方法论知识
knowledge = skill.load_knowledge("loyalty_satisfaction")

# 获取某个模块的标准访谈问题，快速启动调研
questions = skill.get_interview_questions("consumer_insight")
```

## 知识库

references 目录下的 11 篇文档构成了方法论知识库，覆盖 49 个商业分析框架。它们既是 AI Agent 的参考资料，也可以作为独立的方法论速查手册使用。

| 主题 | 文件 | 涵盖框架 |
|------|------|----------|
| 宏观环境 | `macro-environment.md` | PEST/PESTEL、EFE 矩阵 |
| 行业竞争 | `industry-competition.md` | 五力模型、战略集团、行业生命周期、CPM |
| 企业战略 | `strategy-capability.md` | SWOT、BCG、GE、价值链、7S、安索夫、核心竞争力 |
| 消费者洞察 | `consumer-insight.md` | 价值要素金字塔、STP、4P/4C/4R |
| 客户忠诚度 | `loyalty-satisfaction.md` | WAO、Satisfactor、Loyalty Optimizer、ICE |
| 品牌价值 | `brand-value.md` | 品牌资产模型、差异化策略 |
| 思维决策 | `thinking-models.md` | 六顶思考帽、KT 决策法、平衡计分卡、杜邦分析、PDCA |
| 战略矩阵 | `strategy-matrices.md` | IE 矩阵、定向政策矩阵、大战略矩阵 |
| 框架索引 | `business-frameworks.md` | 49 个商业框架速查索引 |
| API 参考 | `api-reference.md` | Python API 完整方法签名与参数说明 |
| 最佳实践 | `best-practices.md` | 研究流程、框架选用指南、常见错误、检查清单 |

## 测试

```bash
python3 skill01/tests/test_all.py
```

10 个测试用例覆盖全部模块：初始化验证、六大分析器、报告生成、知识库搜索、访谈问题生成。

## 与其他 Skill 的协作

这套工具提供的是"结构化思考的框架"，可以和其他专注于特定领域的 Skill 组合使用：

| Skill | 怎么配合 |
|-------|----------|
| JTBD Knowledge Skill | 本工具分析"消费者看重什么"，JTBD 分析"消费者想完成什么任务"，两个视角互补 |
| Quantitative UX Research | 本工具提供分析框架和研究设计，定量研究提供数据采集和统计验证 |
| Value Proposition Design | 本工具的消费者洞察和品牌分析，为价值主张设计提供输入 |
| Deep Research | 当需要收集公开信息时，用 Deep Research 采集数据，再用本工具做结构化分析 |

## 理论基础

工具集的方法论来源于经典著作和前沿研究：《竞争战略》与《竞争优势》（波特）、《战略管理：概念与案例》（弗雷德·大卫）、The Elements of Value（Bain & Company, HBR 2016）、The Wallet Allocation Rule、《追求卓越》（彼得斯）、《蓝海战略》（金伟灿）、《定位》（里斯 & 特劳特）。

## License

MIT
