from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

SKILL_DIR = Path(__file__).resolve().parent.parent
REFERENCES_DIR = SKILL_DIR / "references"

KNOWLEDGE_FILES: Dict[str, str] = {
    "macro_environment": "macro-environment.md",
    "industry_competition": "industry-competition.md",
    "strategy_capability": "strategy-capability.md",
    "consumer_insight": "consumer-insight.md",
    "loyalty_satisfaction": "loyalty-satisfaction.md",
    "brand_value": "brand-value.md",
    "thinking_models": "thinking-models.md",
    "strategy_matrices": "strategy-matrices.md",
    "business_frameworks": "business-frameworks.md",
}

PEST_DIMENSIONS = ["political", "economic", "social", "technological"]
PESTEL_DIMENSIONS = PEST_DIMENSIONS + ["environmental", "legal"]

PEST_LABELS: Dict[str, str] = {
    "political": "政治因素 (Political)",
    "economic": "经济因素 (Economic)",
    "social": "社会文化因素 (Social)",
    "technological": "技术因素 (Technological)",
    "environmental": "环境因素 (Environmental)",
    "legal": "法律因素 (Legal)",
}

FIVE_FORCES = [
    "new_entrants",
    "substitutes",
    "supplier_power",
    "buyer_power",
    "rivalry",
]

FIVE_FORCES_LABELS: Dict[str, str] = {
    "new_entrants": "新进入者威胁",
    "substitutes": "替代品威胁",
    "supplier_power": "供应商议价能力",
    "buyer_power": "买方议价能力",
    "rivalry": "现有竞争者强度",
}

SWOT_QUADRANTS = ["strengths", "weaknesses", "opportunities", "threats"]
SWOT_LABELS: Dict[str, str] = {
    "strengths": "优势 (Strengths)",
    "weaknesses": "劣势 (Weaknesses)",
    "opportunities": "机会 (Opportunities)",
    "threats": "威胁 (Threats)",
}

SWOT_STRATEGIES = {
    "SO": "增长型策略：利用优势抓住机会",
    "WO": "扭转型策略：克服劣势利用机会",
    "ST": "多元化策略：利用优势回避威胁",
    "WT": "防御型策略：减少劣势回避威胁",
}

BCG_QUADRANTS: Dict[str, Dict[str, str]] = {
    "star": {
        "label": "明星业务 ★",
        "growth": "高",
        "share": "高",
        "strategy": "增长战略：大量投资维持增长，未来的现金牛",
        "cash_flow": "适中（大量投入也大量产出）",
    },
    "cash_cow": {
        "label": "现金牛 $",
        "growth": "低",
        "share": "高",
        "strategy": "稳定战略：维持市场地位，产生大量现金流",
        "cash_flow": "高（利润来源）",
    },
    "question_mark": {
        "label": "问题业务 ?",
        "growth": "高",
        "share": "低",
        "strategy": "选择战略：慎重评估是否继续投资",
        "cash_flow": "负（需要大量资金投入）",
    },
    "dog": {
        "label": "瘦狗业务 ×",
        "growth": "低",
        "share": "低",
        "strategy": "收缩/放弃战略：微利或亏损，考虑退出",
        "cash_flow": "适中（不产生也不消耗太多）",
    },
}

GE_MATRIX_ZONES: Dict[str, Dict[str, str]] = {
    "invest_grow": {
        "label": "投资/发展区",
        "cells": "左上三格（高吸引力+强竞争力）",
        "strategy": "优先投资，追求增长和市场领导地位",
    },
    "hold_harvest": {
        "label": "维持/收获区",
        "cells": "对角线三格（中等组合）",
        "strategy": "选择性投资，维持竞争力，收获利润",
    },
    "divest": {
        "label": "收割/放弃区",
        "cells": "右下三格（低吸引力+弱竞争力）",
        "strategy": "减少投资，收割残值或退出",
    },
}

GE_ATTRACTIVENESS_FACTORS = [
    "市场规模",
    "市场增长率",
    "历史毛利率",
    "竞争密集程度",
    "技术要求",
    "能源要求",
    "环境影响",
]

GE_COMPETITIVENESS_FACTORS = [
    "市场份额",
    "份额增长",
    "产品质量",
    "品牌知名度",
    "分销渠道",
    "生产能力",
    "生产效率",
    "单位成本",
    "研发能力",
    "管理人员",
]

VALUE_CHAIN_PRIMARY = [
    "内部后勤（原材料接收、储存、分配）",
    "生产经营（将投入转化为产品）",
    "外部后勤（产品储存和分销）",
    "市场营销（推广和销售）",
    "售后服务",
]

VALUE_CHAIN_SUPPORT = [
    "企业基础设施（管理、财务、法律）",
    "人力资源管理",
    "技术开发",
    "采购",
]

SEVEN_S_ELEMENTS = {
    "hard": {
        "strategy": "战略 (Strategy)",
        "structure": "结构 (Structure)",
        "systems": "制度 (Systems)",
    },
    "soft": {
        "style": "风格 (Style)",
        "staff": "人员 (Staff)",
        "skills": "技能 (Skills)",
        "shared_values": "共同价值观 (Shared Values)",
    },
}

ANSOFF_STRATEGIES: Dict[str, Dict[str, str]] = {
    "market_penetration": {
        "label": "市场渗透",
        "market": "现有",
        "product": "现有",
        "risk": "低",
        "description": "在现有市场增加现有产品的销售",
    },
    "market_development": {
        "label": "市场开发",
        "market": "新",
        "product": "现有",
        "risk": "中",
        "description": "将现有产品推向新市场",
    },
    "product_development": {
        "label": "产品开发",
        "market": "现有",
        "product": "新",
        "risk": "中",
        "description": "为现有市场开发新产品",
    },
    "diversification": {
        "label": "多元化",
        "market": "新",
        "product": "新",
        "risk": "高",
        "description": "以新产品进入新市场",
    },
}

VALUE_PYRAMID_LAYERS: Dict[str, Dict[str, Any]] = {
    "functional": {
        "label": "功能价值（基础层）",
        "level": 1,
        "elements": [
            "节省时间", "减少努力", "简化流程", "避免麻烦",
            "赚钱", "降低成本", "降低风险", "质量",
            "组织整理", "多样性", "整合连接", "感官体验",
            "联结沟通", "信息告知",
        ],
    },
    "emotional": {
        "label": "情感价值",
        "level": 2,
        "elements": [
            "减少焦虑", "健康/保健", "奖励自我", "治愈价值",
            "怀旧感", "趣味/娱乐", "设计/美学", "徽章价值",
            "吸引力", "提供接触渠道",
        ],
    },
    "life_changing": {
        "label": "改变生活价值",
        "level": 3,
        "elements": [
            "提供希望", "自我激励", "自我实现", "传承价值", "归属感",
        ],
    },
    "social_impact": {
        "label": "社会影响价值（顶层）",
        "level": 4,
        "elements": ["自我超越"],
    },
}

ALL_VALUE_ELEMENTS: List[str] = []
for layer in VALUE_PYRAMID_LAYERS.values():
    ALL_VALUE_ELEMENTS.extend(layer["elements"])

INDUSTRY_VALUE_PROFILES: Dict[str, List[str]] = {
    "食品饮料": ["质量", "感官体验", "多样性", "设计/美学", "治愈价值"],
    "消费银行": ["质量", "提供接触渠道", "传承价值", "避免麻烦", "减少焦虑"],
    "智能手机": ["减少努力", "节省时间", "联结沟通", "整合连接", "多样性", "趣味/娱乐"],
    "服装零售": ["质量", "多样性", "避免麻烦", "设计/美学", "节省时间"],
    "电视服务": ["质量", "多样性", "降低成本", "节省时间", "奖励自我"],
    "折扣零售": ["质量", "多样性", "降低成本", "设计/美学", "趣味/娱乐"],
}

LOYALTY_CUSTOMER_SEGMENTS: Dict[str, Dict[str, str]] = {
    "core": {
        "label": "核心客户",
        "ratio": "35%",
        "description": "高价值高忠诚，企业最重要的利润来源",
        "strategy": "维护关系，提升体验，防止流失",
    },
    "high_value_at_risk": {
        "label": "高价值易流失客户",
        "ratio": "20%",
        "description": "价值高但忠诚度不稳定，最需要关注的群体",
        "strategy": "识别流失原因，针对性改善，提升排名",
    },
    "low_value_at_risk": {
        "label": "低价值易流失客户",
        "ratio": "30%",
        "description": "价值低且忠诚度不稳定",
        "strategy": "评估投入产出比，选择性维护",
    },
    "low_value_satisfied": {
        "label": "低价值易满足客户",
        "ratio": "15%",
        "description": "满意度高但消费能力有限",
        "strategy": "维持基本服务，探索提升客单价的机会",
    },
}

ICE_DIMENSIONS = ["接触点", "情境", "感觉", "区段", "地理", "时间"]

ICE_PILLARS = ["整体设计", "品牌差异", "可检测的区别", "期望确定"]

BRAND_LOYALTY_LEVELS = [
    {"level": 1, "label": "价格敏感型转换者", "description": "纯粹基于价格选择，无品牌忠诚"},
    {"level": 2, "label": "习惯性购买者", "description": "出于惯性购买，易被竞争者吸引"},
    {"level": 3, "label": "满意型购买者", "description": "对品牌满意但可能因更好选择而转换"},
    {"level": 4, "label": "情感型忠诚者", "description": "与品牌建立了情感连接"},
    {"level": 5, "label": "承诺型忠诚者", "description": "深度认同品牌价值，主动推荐"},
]

INDUSTRY_LIFECYCLE_STAGES: Dict[str, Dict[str, str]] = {
    "introduction": {
        "label": "导入期",
        "features": "市场规模小、增长缓慢、产品不成熟、竞争者少",
        "strategy": "产品创新和市场教育",
    },
    "growth": {
        "label": "成长期",
        "features": "市场快速增长、新进入者增多、产品逐渐标准化",
        "strategy": "扩大市场份额和建立品牌",
    },
    "maturity": {
        "label": "成熟期",
        "features": "增长放缓、竞争加剧、价格竞争突出",
        "strategy": "效率提升和差异化",
    },
    "decline": {
        "label": "衰退期",
        "features": "市场萎缩、企业退出、价格战频繁",
        "strategy": "收割或退出",
    },
}

RESEARCH_MODULES = [
    "macro_environment",
    "industry_competition",
    "strategy_capability",
    "consumer_insight",
    "loyalty_satisfaction",
    "brand_value",
]

RESEARCH_MODULE_LABELS: Dict[str, str] = {
    "macro_environment": "宏观环境分析",
    "industry_competition": "行业竞争格局",
    "strategy_capability": "企业战略与能力",
    "consumer_insight": "消费者洞察",
    "loyalty_satisfaction": "客户满意度与忠诚度",
    "brand_value": "品牌与价值体系",
}


@dataclass
class AnalysisConfig:
    company_name: str = ""
    industry: str = ""
    modules: List[str] = field(default_factory=lambda: list(RESEARCH_MODULES))
    pest_mode: str = "pestel"
    scoring_scale: int = 5
    output_format: str = "markdown"
    language: str = "zh"
    include_competitors: bool = True
    competitor_names: List[str] = field(default_factory=list)
    time_horizon: str = "3-5年"

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.company_name:
            errors.append("必须指定公司名称 (company_name)")
        if not self.industry:
            errors.append("必须指定所属行业 (industry)")
        valid_modules = set(RESEARCH_MODULES)
        for m in self.modules:
            if m not in valid_modules:
                errors.append(f"无效的研究模块: {m}，可选: {valid_modules}")
        if self.pest_mode not in ("pest", "pestel"):
            errors.append(f"pest_mode 必须为 'pest' 或 'pestel'，当前: {self.pest_mode}")
        if self.scoring_scale not in (5, 10):
            errors.append(f"scoring_scale 必须为 5 或 10，当前: {self.scoring_scale}")
        if self.output_format not in ("markdown", "json"):
            errors.append(f"output_format 必须为 'markdown' 或 'json'，当前: {self.output_format}")
        if self.include_competitors and not self.competitor_names:
            errors.append("启用竞争分析时必须提供竞争对手名称 (competitor_names)")
        return errors
