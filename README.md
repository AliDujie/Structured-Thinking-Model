# Structured-Thinking-Model

像咨询公司资深总监一样，系统化地研究一家公司。

一套完整的企业全维度调研工具包，涵盖宏观环境分析、行业竞争格局、企业战略与能力、消费者洞察、客户满意度与忠诚度、品牌价值等六大研究模块，并提供 Python 可执行分析工具与 9 篇方法论知识库。

## 适用场景

- 投资尽职调查：系统评估目标企业的外部环境、竞争地位、内部能力与客户关系
- 战略咨询：为企业制定战略规划提供结构化分析框架与数据支撑
- 竞争分析：从行业结构、关键成功因素、品牌资产等维度评估竞争格局
- 品牌诊断：通过价值要素金字塔、品牌资产模型、差异化策略分析品牌健康度
- 消费者研究：结合价值要素、STP 定位、营销组合评估消费者需求与感知
- 客户忠诚度分析：运用 WAO 钱包分配法则、Satisfactor 模型、ICE 体验框架评估客户关系

## 项目结构

```
Structured-Thinking-Model/
├── SKILL.md                  # Skill 主文件（Agent 读取入口）
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
│   └── business-frameworks.md    # 70 个商业框架索引
└── skill01/                  # Python 可执行工具包
    ├── __init__.py               # 统一入口 CompanyResearchSkill
    ├── config.py                 # 全局配置与模块定义
    ├── macro_analyzer.py         # 宏观环境分析器（PESTEL）
    ├── industry_analyzer.py      # 行业竞争分析器（五力 + CPM）
    ├── strategy_analyzer.py      # 企业战略分析器（SWOT + BCG + GE + 价值链 + 7S）
    ├── consumer_analyzer.py      # 消费者洞察分析器（价值要素 + STP）
    ├── loyalty_analyzer.py       # 客户忠诚度分析器（WAO + Satisfactor + ICE）
    ├── brand_analyzer.py         # 品牌价值分析器（品牌资产 + 差异化）
    ├── report_generator.py       # 综合报告生成器（十章完整报告）
    ├── templates.py              # 访谈问题与创新检查清单
    ├── utils.py                  # 知识库加载与搜索工具
    └── tests/
        └── test_all.py           # 10 个测试用例，覆盖全部模块
```

## 安装

skill01 仅依赖 Python 标准库，Python >= 3.8 即可运行。

```bash
# 克隆仓库
git clone https://github.com/AliDujie/Structured-Thinking-Model.git
cd Structured-Thinking-Model

# 以开发模式安装（推荐）
pip install -e .
```

安装完成后即可在任意位置 `from skill01 import CompanyResearchSkill`。

如果作为 AI Agent Skill 使用，将整个目录复制到你的 skills 目录下即可（如 `~/.agents/skills/`）。

## 快速开始

```python
from skill01 import CompanyResearchSkill

# 初始化
skill = CompanyResearchSkill("星巴克中国", "餐饮连锁")

# 1. 宏观环境分析
skill.macro.add_factor("economic", "消费升级", "中产阶级扩大带动咖啡消费",
                       score=4.5, weight=0.15, trend="上升")
skill.macro.add_factor("social", "咖啡文化", "年轻人咖啡消费习惯形成",
                       score=4.0, weight=0.12, trend="上升")

# 2. 行业竞争分析
skill.industry.set_lifecycle_stage("growth")
skill.industry.add_force_driver("rivalry", "本土品牌崛起",
                                "瑞幸等本土品牌快速扩张", score=4.5, weight=0.3)

# 3. 战略分析
skill.strategy.add_swot_item("strengths", "全球品牌影响力", importance=5)
skill.strategy.add_swot_item("threats", "本土品牌性价比优势", importance=5)

# 4. 消费者洞察
skill.consumer.add_value_score("质量", score=4.5,
                               competitor_scores={"瑞幸": 3.5}, importance=5.0)

# 5. 客户忠诚度
skill.loyalty.add_brand_ranking("星巴克中国", satisfaction_score=4.3,
                                rank=1, brand_count=4)

# 6. 品牌价值
skill.brand.set_awareness(top_of_mind=45.0, aided_awareness=95.0, recognition=98.0)

# 生成完整报告
skill.report.set_executive_summary("星巴克中国在品牌力和体验方面保持领先...")
report = skill.generate_full_report()
print(report)
```

## 八大核心能力

| # | 能力 | 分析器 | 核心框架 |
|---|------|--------|----------|
| 1 | 宏观环境分析 | `MacroAnalyzer` | PEST/PESTEL、EFE 矩阵 |
| 2 | 行业竞争格局 | `IndustryAnalyzer` | 波特五力、CPM 矩阵、行业生命周期 |
| 3 | 企业战略与能力 | `StrategyAnalyzer` | SWOT、BCG、GE、价值链、7S、安索夫 |
| 4 | 消费者洞察 | `ConsumerAnalyzer` | 价值要素金字塔（30 要素）、STP、4P/4C/4R |
| 5 | 客户满意度与忠诚度 | `LoyaltyAnalyzer` | WAO 钱包分配法则、Satisfactor、ICE |
| 6 | 品牌价值分析 | `BrandAnalyzer` | 品牌资产模型、差异化策略 |
| 7 | 综合报告生成 | `ReportGenerator` | 十章完整研究报告 |
| 8 | 知识库检索 | `search_knowledge()` | 9 篇方法论知识库全文检索 |

每个分析器均支持 `render_markdown()` 和 `render_json()` 两种输出格式。

## 研究流程

本工具包遵循"由外而内"的研究逻辑：

```
宏观环境 → 行业竞争 → 企业战略 → 消费者洞察 → 客户忠诚度 → 品牌价值 → 综合报告
 (PESTEL)   (五力+CPM)  (SWOT+BCG)  (价值要素+STP)  (WAO+ICE)   (品牌资产)  (十章报告)
```

五个核心原则贯穿始终：由外而内、竞争视角、消费者导向、数据驱动、行动导向。

## 知识库

references 目录包含 9 篇方法论知识库文档，可通过 Python API 检索：

```python
# 关键词搜索
results = skill.search_knowledge("五力模型")

# 加载特定主题
knowledge = skill.load_knowledge("strategy_capability")

# 生成访谈问题
questions = skill.get_interview_questions("consumer_insight")
```

## 测试

```bash
python3 skill01/tests/test_all.py
```

包含 10 个测试用例，覆盖全部模块：初始化验证、六大分析器、报告生成、知识库搜索、访谈问题生成。

## 与其他 Skill 的协作

| Skill | 协作方式 |
|-------|----------|
| JTBD Knowledge Skill | 互补视角 — 本 Skill 分析"消费者看重什么"，JTBD 分析"消费者想完成什么任务" |
| Quantitative UX Research | 本 Skill 提供分析框架，定量研究提供数据采集和统计分析能力 |
| Value Proposition Design | 品牌价值和消费者价值分析为价值主张设计提供输入 |
| Deep Research | 当需要收集企业公开信息时，可调用 Deep Research 进行信息采集 |

## 理论基础

核心方法论来源于《竞争战略》（波特）、《战略管理》（弗雷德·大卫）、The Elements of Value（Bain & Company, HBR 2016）、The Wallet Allocation Rule、《追求卓越》（彼得斯）、《蓝海战略》、《定位》（里斯 & 特劳特）等经典著作与前沿研究。

## License

MIT
