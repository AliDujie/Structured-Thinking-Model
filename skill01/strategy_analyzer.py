from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .base_analyzer import BaseAnalyzer
from .config import (
    SWOT_QUADRANTS, SWOT_LABELS, SWOT_STRATEGIES,
    BCG_QUADRANTS, GE_MATRIX_ZONES, GE_ATTRACTIVENESS_FACTORS,
    GE_COMPETITIVENESS_FACTORS, VALUE_CHAIN_PRIMARY, VALUE_CHAIN_SUPPORT,
    SEVEN_S_ELEMENTS, ANSOFF_STRATEGIES,
)
from .templates import SWOT_TEMPLATE, BCG_TEMPLATE, GE_TEMPLATE, VALUE_CHAIN_TEMPLATE, SEVEN_S_TEMPLATE
from .utils import (
    format_list, format_table, format_score_bar, score_to_level,
    validate_score, validate_weight, format_as_json,
    calculate_weighted_total, normalize_weights,
)


@dataclass
class SWOTItem:
    quadrant: str
    content: str
    importance: int = 3

    def validate(self) -> List[str]:
        errors: List[str] = []
        if self.quadrant not in SWOT_QUADRANTS:
            errors.append(f"无效象限: {self.quadrant}")
        if not 1 <= self.importance <= 5:
            errors.append(f"重要性必须在1-5之间: {self.importance}")
        return errors


@dataclass
class SWOTStrategy:
    strategy_type: str
    description: str
    actions: List[str] = field(default_factory=list)


@dataclass
class BusinessUnit:
    name: str
    market_growth_rate: float = 0.0
    relative_market_share: float = 0.0
    revenue: float = 0.0
    quadrant: str = ""

    def classify(self) -> str:
        high_growth = self.market_growth_rate > 10.0
        high_share = self.relative_market_share > 1.0
        if high_growth and high_share:
            return "star"
        if not high_growth and high_share:
            return "cash_cow"
        if high_growth and not high_share:
            return "question_mark"
        return "dog"


@dataclass
class GEFactor:
    name: str
    weight: float = 0.1
    score: float = 3.0
    category: str = "attractiveness"


@dataclass
class ValueChainActivity:
    name: str
    category: str
    performance: float = 3.0
    competitor_benchmark: float = 3.0
    description: str = ""
    is_advantage: bool = False


@dataclass
class SevenSElement:
    element: str
    assessment: str = ""
    score: float = 3.0
    issues: List[str] = field(default_factory=list)


class StrategyAnalyzer(BaseAnalyzer):
    def __init__(self, company: str, industry: str):
        super().__init__(company, industry, "strategy_capability")
        self._swot_items: List[SWOTItem] = []
        self._swot_strategies: List[SWOTStrategy] = []
        self._business_units: List[BusinessUnit] = []
        self._ge_factors: List[GEFactor] = []
        self._value_chain: List[ValueChainActivity] = []
        self._seven_s: List[SevenSElement] = []
        self._ansoff_choice: str = ""

    def add_swot_item(self, quadrant: str, content: str, importance: int = 3) -> "StrategyAnalyzer":
        item = SWOTItem(quadrant=quadrant, content=content, importance=importance)
        errors = item.validate()
        if errors:
            raise ValueError(f"SWOT项验证失败: {'; '.join(errors)}")
        self._swot_items.append(item)
        return self

    def add_swot_items_batch(self, items: List[Dict]) -> "StrategyAnalyzer":
        for item in items:
            self.add_swot_item(**item)
        return self

    def add_swot_strategy(self, strategy_type: str, description: str,
                          actions: Optional[List[str]] = None) -> "StrategyAnalyzer":
        if strategy_type not in SWOT_STRATEGIES:
            raise ValueError(f"无效策略类型: {strategy_type}，可选: {list(SWOT_STRATEGIES.keys())}")
        a = actions if actions is not None else []
        self._swot_strategies.append(SWOTStrategy(
            strategy_type=strategy_type, description=description, actions=a,
        ))
        return self

    def add_business_unit(self, name: str, market_growth_rate: float,
                          relative_market_share: float, revenue: float = 0.0) -> "StrategyAnalyzer":
        bu = BusinessUnit(name=name, market_growth_rate=market_growth_rate,
                          relative_market_share=relative_market_share, revenue=revenue)
        bu.quadrant = bu.classify()
        self._business_units.append(bu)
        return self

    def add_ge_factor(self, name: str, weight: float, score: float,
                      category: str = "attractiveness") -> "StrategyAnalyzer":
        if category not in ("attractiveness", "competitiveness"):
            raise ValueError(f"category必须为attractiveness或competitiveness")
        self._ge_factors.append(GEFactor(
            name=name, weight=validate_weight(weight),
            score=validate_score(score), category=category,
        ))
        return self

    def add_value_chain_activity(self, name: str, category: str,
                                 performance: float = 3.0,
                                 competitor_benchmark: float = 3.0,
                                 description: str = "") -> "StrategyAnalyzer":
        if category not in ("primary", "support"):
            raise ValueError("category必须为primary或support")
        is_adv = performance > competitor_benchmark
        self._value_chain.append(ValueChainActivity(
            name=name, category=category,
            performance=validate_score(performance),
            competitor_benchmark=validate_score(competitor_benchmark),
            description=description, is_advantage=is_adv,
        ))
        return self

    def add_seven_s(self, element: str, assessment: str,
                    score: float = 3.0,
                    issues: Optional[List[str]] = None) -> "StrategyAnalyzer":
        all_elements = {}
        all_elements.update(SEVEN_S_ELEMENTS["hard"])
        all_elements.update(SEVEN_S_ELEMENTS["soft"])
        if element not in all_elements:
            raise ValueError(f"无效7S要素: {element}，可选: {list(all_elements.keys())}")
        iss = issues if issues is not None else []
        self._seven_s.append(SevenSElement(
            element=element, assessment=assessment,
            score=validate_score(score), issues=iss,
        ))
        return self

    def set_ansoff_choice(self, strategy: str) -> "StrategyAnalyzer":
        if strategy not in ANSOFF_STRATEGIES:
            raise ValueError(f"无效安索夫策略: {strategy}，可选: {list(ANSOFF_STRATEGIES.keys())}")
        self._ansoff_choice = strategy
        return self

    def _render_swot(self) -> str:
        by_q: Dict[str, List[SWOTItem]] = {q: [] for q in SWOT_QUADRANTS}
        for item in self._swot_items:
            by_q[item.quadrant].append(item)

        def fmt(items: List[SWOTItem]) -> str:
            if not items:
                return "*暂无数据*"
            sorted_items = sorted(items, key=lambda x: -x.importance)
            return "\n".join(f"- [{i.importance}/5] {i.content}" for i in sorted_items)

        strategies_by_type: Dict[str, List[SWOTStrategy]] = {}
        for s in self._swot_strategies:
            strategies_by_type.setdefault(s.strategy_type, []).append(s)

        def fmt_strat(st: str) -> str:
            strats = strategies_by_type.get(st, [])
            if not strats:
                return f"*{SWOT_STRATEGIES[st]}*\n\n*待制定*"
            parts = []
            for s in strats:
                parts.append(f"**{s.description}**")
                if s.actions:
                    parts.append(format_list(s.actions))
            return "\n\n".join(parts)

        return SWOT_TEMPLATE.format(
            company=self._company,
            strengths=fmt(by_q["strengths"]),
            weaknesses=fmt(by_q["weaknesses"]),
            opportunities=fmt(by_q["opportunities"]),
            threats=fmt(by_q["threats"]),
            so_strategies=fmt_strat("SO"),
            wo_strategies=fmt_strat("WO"),
            st_strategies=fmt_strat("ST"),
            wt_strategies=fmt_strat("WT"),
        )

    def _render_bcg(self) -> str:
        if not self._business_units:
            return ""
        rows = []
        for bu in self._business_units:
            q_info = BCG_QUADRANTS[bu.quadrant]
            rows.append([bu.name, f"{bu.market_growth_rate:.1f}%",
                         f"{bu.relative_market_share:.2f}",
                         q_info["label"], q_info["strategy"]])
        table = format_table(
            ["业务单元", "市场增长率", "相对市场份额", "象限", "建议策略"], rows
        )
        recs: List[str] = []
        for q_key in ["star", "cash_cow", "question_mark", "dog"]:
            units = [bu for bu in self._business_units if bu.quadrant == q_key]
            if units:
                names = "、".join(u.name for u in units)
                recs.append(f"**{BCG_QUADRANTS[q_key]['label']}** ({names}): {BCG_QUADRANTS[q_key]['strategy']}")
        return BCG_TEMPLATE.format(
            company=self._company,
            business_units=table,
            recommendations="\n\n".join(recs) if recs else "*暂无数据*",
        )

    def _render_ge(self) -> str:
        if not self._ge_factors:
            return ""
        attr_factors = [f for f in self._ge_factors if f.category == "attractiveness"]
        comp_factors = [f for f in self._ge_factors if f.category == "competitiveness"]

        def fmt_factors(factors: List[GEFactor]) -> str:
            if not factors:
                return "*暂无数据*"
            rows = [[f.name, f"{f.weight:.2f}", format_score_bar(f.score)] for f in factors]
            table = format_table(["因素", "权重", "评分"], rows)
            normalized = normalize_weights([{"weight": f.weight, "score": f.score} for f in factors])
            total = calculate_weighted_total(normalized)
            return f"{table}\n\n**加权总分**: {total:.2f}"

        attr_score = 0.0
        if attr_factors:
            n = normalize_weights([{"weight": f.weight, "score": f.score} for f in attr_factors])
            attr_score = calculate_weighted_total(n)
        comp_score = 0.0
        if comp_factors:
            n = normalize_weights([{"weight": f.weight, "score": f.score} for f in comp_factors])
            comp_score = calculate_weighted_total(n)

        if attr_score >= 3.33 and comp_score >= 3.33:
            zone = GE_MATRIX_ZONES["invest_grow"]
        elif attr_score <= 2.33 and comp_score <= 2.33:
            zone = GE_MATRIX_ZONES["divest"]
        else:
            zone = GE_MATRIX_ZONES["hold_harvest"]

        strategies = f"**定位**: {zone['label']} ({zone['cells']})\n\n**战略建议**: {zone['strategy']}"

        return GE_TEMPLATE.format(
            company=self._company,
            attractiveness_factors=fmt_factors(attr_factors),
            competitiveness_factors=fmt_factors(comp_factors),
            business_positions=f"行业吸引力: {attr_score:.2f} | 业务竞争力: {comp_score:.2f}",
            strategies=strategies,
        )

    def render_markdown(self) -> str:
        if (not self._swot_items and not self._business_units and not self._ge_factors
                and not self._value_chain and not self._seven_s):
            return "## 企业战略与能力分析\n\n*尚未录入分析数据。请使用 `add_swot_item()` 等方法添加战略分析数据。*\n"
        parts = [f"# 企业战略与能力分析 — {self._company}\n"]
        if self._swot_items:
            parts.append(self._render_swot())
        if self._business_units:
            parts.append(self._render_bcg())
        if self._ge_factors:
            parts.append(self._render_ge())
        if self._value_chain:
            primary = [a for a in self._value_chain if a.category == "primary"]
            support = [a for a in self._value_chain if a.category == "support"]

            def fmt_vc(activities: List[ValueChainActivity]) -> str:
                if not activities:
                    return "*暂无数据*"
                rows = [[a.name, format_score_bar(a.performance),
                         format_score_bar(a.competitor_benchmark),
                         "✓ 优势" if a.is_advantage else "✗ 劣势",
                         a.description] for a in activities]
                return format_table(["活动", "企业表现", "竞争对手", "对比", "说明"], rows)

            advantages = [a for a in self._value_chain if a.is_advantage]
            improvements = [a for a in self._value_chain if not a.is_advantage]
            parts.append(VALUE_CHAIN_TEMPLATE.format(
                company=self._company,
                primary_activities=fmt_vc(primary),
                support_activities=fmt_vc(support),
                competitive_advantages=format_list([a.name for a in advantages]) if advantages else "*暂无明显优势*",
                improvements=format_list([a.name for a in improvements]) if improvements else "*暂无明显改进点*",
            ))
        if self._seven_s:
            all_el = {}
            all_el.update(SEVEN_S_ELEMENTS["hard"])
            all_el.update(SEVEN_S_ELEMENTS["soft"])
            hard = [s for s in self._seven_s if s.element in SEVEN_S_ELEMENTS["hard"]]
            soft = [s for s in self._seven_s if s.element in SEVEN_S_ELEMENTS["soft"]]

            def fmt_7s(elements: List[SevenSElement]) -> str:
                if not elements:
                    return "*暂无数据*"
                rows = [[all_el.get(e.element, e.element), e.assessment,
                         format_score_bar(e.score),
                         "、".join(e.issues) if e.issues else "无"] for e in elements]
                return format_table(["要素", "评估", "评分", "问题"], rows)

            avg_score = sum(s.score for s in self._seven_s) / len(self._seven_s) if self._seven_s else 0
            alignment = "协调一致" if avg_score >= 3.5 else ("基本协调" if avg_score >= 2.5 else "存在失调")
            low_items = sorted(self._seven_s, key=lambda x: x.score)[:3]
            priorities = format_list([f"{all_el.get(s.element, s.element)} ({s.score:.1f})" for s in low_items])

            parts.append(SEVEN_S_TEMPLATE.format(
                company=self._company,
                hard_elements=fmt_7s(hard),
                soft_elements=fmt_7s(soft),
                alignment_assessment=f"**综合协调性**: {alignment} (平均分: {avg_score:.2f})",
                improvement_priorities=priorities,
            ))
        if self._ansoff_choice:
            info = ANSOFF_STRATEGIES[self._ansoff_choice]
            parts.append(f"\n## 安索夫增长战略选择\n\n**选定策略**: {info['label']}\n"
                         f"- 市场: {info['market']} | 产品: {info['product']} | 风险: {info['risk']}\n"
                         f"- {info['description']}\n")
        return "\n\n".join(parts)

    def render_json(self) -> str:
        data = {
            "company": self._company, "industry": self._industry,
            "swot": {q: [{"content": i.content, "importance": i.importance}
                         for i in self._swot_items if i.quadrant == q]
                     for q in SWOT_QUADRANTS},
            "swot_strategies": [{"type": s.strategy_type, "description": s.description,
                                 "actions": s.actions} for s in self._swot_strategies],
            "bcg": [{"name": bu.name, "growth_rate": bu.market_growth_rate,
                     "relative_share": bu.relative_market_share,
                     "quadrant": bu.quadrant, "revenue": bu.revenue}
                    for bu in self._business_units],
            "ge_factors": [{"name": f.name, "weight": f.weight, "score": f.score,
                            "category": f.category} for f in self._ge_factors],
            "value_chain": [{"name": a.name, "category": a.category,
                             "performance": a.performance,
                             "benchmark": a.competitor_benchmark,
                             "is_advantage": a.is_advantage}
                            for a in self._value_chain],
            "seven_s": [{"element": s.element, "assessment": s.assessment,
                         "score": s.score, "issues": s.issues}
                        for s in self._seven_s],
            "ansoff_choice": self._ansoff_choice,
        }
        return format_as_json(data)
