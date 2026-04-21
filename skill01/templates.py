PEST_ANALYSIS_TEMPLATE = """# PEST{el}分析 — {company}

## 分析概要
- **公司**: {company}
- **行业**: {industry}
- **分析日期**: {date}
- **分析模式**: {mode}

{factors_section}

## 综合评估
- **EFE加权总分**: {efe_score:.2f} / {max_score}
- **环境态势判断**: {assessment}

## 关键发现
{key_findings}

## 战略启示
{implications}
"""

FIVE_FORCES_TEMPLATE = """# 波特五力分析 — {company}

## 分析概要
- **公司**: {company}
- **行业**: {industry}

{forces_section}

## 行业吸引力综合评估
- **综合得分**: {total_score:.2f} / {max_score}
- **行业吸引力**: {attractiveness}
- **盈利潜力**: {profitability}

## 关键成功因素
{ksf_section}
"""

SWOT_TEMPLATE = """# SWOT分析 — {company}

## 内部因素
### 优势 (Strengths)
{strengths}

### 劣势 (Weaknesses)
{weaknesses}

## 外部因素
### 机会 (Opportunities)
{opportunities}

### 威胁 (Threats)
{threats}

## SWOT组合策略
### SO策略（增长型）
{so_strategies}

### WO策略（扭转型）
{wo_strategies}

### ST策略（多元化）
{st_strategies}

### WT策略（防御型）
{wt_strategies}
"""

BCG_TEMPLATE = """# 波士顿矩阵分析 — {company}

## 业务组合
{business_units}

## 矩阵定位
```
          高增长率
    ★ 明星  |  ? 问题
   ---------+---------
    $ 现金牛 |  × 瘦狗
          低增长率
    高份额        低份额
```

## 资源配置建议
{recommendations}
"""

GE_TEMPLATE = """# GE矩阵分析 — {company}

## 评估维度

### 行业吸引力因素
{attractiveness_factors}

### 业务竞争力因素
{competitiveness_factors}

## 业务定位
{business_positions}

## 战略建议
{strategies}
"""

VALUE_CHAIN_TEMPLATE = """# 价值链分析 — {company}

## 基本活动
{primary_activities}

## 支持活动
{support_activities}

## 竞争优势来源
{competitive_advantages}

## 改进建议
{improvements}
"""

SEVEN_S_TEMPLATE = """# 7S模型诊断 — {company}

## 硬件要素
{hard_elements}

## 软件要素
{soft_elements}

## 协调性评估
{alignment_assessment}

## 改进优先级
{improvement_priorities}
"""

VALUE_PYRAMID_TEMPLATE = """# 消费者价值要素分析 — {company}

## 行业: {industry}

## 价值要素评分
### 第四层：社会影响价值（顶层）
{social_impact_scores}

### 第三层：改变生活价值
{life_changing_scores}

### 第二层：情感价值
{emotional_scores}

### 第一层：功能价值（基础层）
{functional_scores}

## 与行业标杆对比
{benchmark_comparison}

## 价值要素优化建议
{optimization_suggestions}
"""

WAO_TEMPLATE = """# 钱包分配法则分析 — {company}

## 核心公式
钱包份额 = (1 - 排名/(品牌数量+1)) × (2/品牌数量)

## 品牌排名与钱包份额
{brand_rankings}

## 竞争品牌流失分析
{competitive_loss}

## 提升排名策略
{ranking_strategies}
"""

LOYALTY_TEMPLATE = """# 客户忠诚度分析 — {company}

## 客户分层
{customer_segments}

## 忠诚度驱动因素
{loyalty_drivers}

## 不满意驱动因素
{dissatisfaction_drivers}

## 改善方案
{improvement_plans}
"""

BRAND_TEMPLATE = """# 品牌价值分析 — {company}

## 品牌资产评估
### 品牌知名度
{awareness}

### 品牌联想
{associations}

### 品牌形象
{image}

### 品牌忠诚度
{loyalty}

## 竞争品牌对比
{competitive_comparison}

## 品牌差异化策略
{differentiation}
"""

STP_TEMPLATE = """# STP分析 — {company}

## 市场细分 (Segmentation)
{segmentation}

## 目标市场选择 (Targeting)
{targeting}

## 市场定位 (Positioning)
{positioning}
"""

MARKETING_MIX_TEMPLATE = """# 营销组合分析 — {company}

## 4P分析
{four_p}

## 4C分析（消费者视角）
{four_c}

## 4R分析（关系视角）
{four_r}
"""

ICE_TEMPLATE = """# ICE完美顾客体验分析 — {company}

## 六大构成要素
{dimensions}

## 四大支撑维度
{pillars}

## 体验差距分析
{gap_analysis}

## 差异化体验设计
{experience_design}
"""

FULL_REPORT_TEMPLATE = """# {company} — 企业全维度研究报告

**行业**: {industry}
**研究日期**: {date}
**研究范围**: {scope}

---

## 一、执行摘要
{executive_summary}

## 二、宏观环境分析
{macro_analysis}

## 三、行业竞争格局
{industry_analysis}

## 四、企业概况
{company_overview}

## 五、战略分析
{strategy_analysis}

## 六、消费者洞察
{consumer_insight}

## 七、品牌诊断
{brand_diagnosis}

## 八、客户体验与忠诚度
{loyalty_analysis}

## 九、综合诊断
{comprehensive_diagnosis}

## 十、战略建议
{strategic_recommendations}

---
*本报告基于公开信息和分析框架生成，仅供参考。*
"""

INTERVIEW_QUESTIONS = {
    "macro_environment": [
        "您认为当前政策环境对贵公司业务最大的影响是什么？",
        "未来3-5年，哪些技术趋势会对行业产生颠覆性影响？",
        "消费者行为和社会文化变迁中，哪些变化对贵公司最为关键？",
        "当前经济周期对贵公司的业务有何具体影响？",
        "环保法规和可持续发展要求对贵公司运营有何影响？",
    ],
    "industry_competition": [
        "您认为行业内最强的竞争对手是谁？他们的核心优势是什么？",
        "新进入者对行业的威胁有多大？主要进入壁垒是什么？",
        "是否存在可能替代贵公司产品/服务的替代品？",
        "供应商和客户的议价能力如何？趋势怎样？",
        "行业目前处于生命周期的哪个阶段？未来走向如何？",
    ],
    "strategy_capability": [
        "贵公司最核心的竞争优势是什么？这种优势可持续吗？",
        "贵公司目前的增长战略是什么？效果如何？",
        "组织结构和管理体系是否支撑当前战略的有效执行？",
        "贵公司的业务组合中，哪些是明星业务，哪些需要调整？",
        "价值链中哪些环节是贵公司的优势所在？哪些需要改进？",
    ],
    "consumer_insight": [
        "贵公司的目标消费者是谁？他们最看重什么？",
        "消费者选择贵公司产品/服务的主要原因是什么？",
        "消费者对贵公司品牌的认知与贵公司期望的定位是否一致？",
        "在消费者价值要素中，贵公司在哪些方面表现突出？",
        "消费者的未满足需求有哪些？如何更好地满足？",
    ],
    "loyalty_satisfaction": [
        "贵公司的客户满意度水平如何？与竞争对手相比排名如何？",
        "客户流失的主要原因是什么？流失到了哪些竞争品牌？",
        "贵公司的客户忠诚度计划效果如何？",
        "客户体验中最让客户愉悦和最让客户不满的分别是什么？",
        "贵公司的钱包份额在过去几年的变化趋势如何？",
    ],
    "brand_value": [
        "贵公司品牌的核心价值主张是什么？",
        "品牌知名度和品牌形象在目标市场中处于什么水平？",
        "与主要竞争品牌相比，贵公司品牌的差异化优势是什么？",
        "品牌忠诚度如何？有多少承诺型忠诚者？",
        "品牌在情感价值和功能价值上的表现如何？",
    ],
}

INNOVATION_CHECKLIST = [
    "是否存在消费者的补偿行为（用非理想方式满足需求）？",
    "是否存在异常客户（使用方式与设计意图不同的用户）？",
    "是否存在上游机会（帮助消费者更好地准备使用产品）？",
    "是否存在下游机会（帮助消费者获得更好的使用后体验）？",
    "是否存在流失洞察（离开的客户揭示了什么未满足需求）？",
    "质量是否达到行业基准水平？",
    "是否在四个以上价值要素上获得高分？",
    "数字化体验是否在'节省时间'和'避免麻烦'上表现突出？",
    "是否在情感价值要素上建立了差异化优势？",
    "客户体验是否具有一致性和差异化？",
]
