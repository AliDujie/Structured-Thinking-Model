from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .config import LOYALTY_CUSTOMER_SEGMENTS, ICE_DIMENSIONS, ICE_PILLARS, ICE_DATA_METHODS
from .templates import WAO_TEMPLATE, LOYALTY_TEMPLATE, ICE_TEMPLATE
from .utils import (
    format_list, format_table, format_score_bar, validate_score,
    wallet_share_formula, load_knowledge, format_as_json,
)


@dataclass
class BrandRanking:
    brand: str
    satisfaction_score: float = 3.0
    rank: int = 1
    brand_count: int = 3
    wallet_share: float = 0.0

    def calculate_wallet_share(self) -> float:
        self.wallet_share = wallet_share_formula(self.rank, self.brand_count)
        return self.wallet_share


@dataclass
class SatisfactionDriver:
    name: str
    importance: float = 3.0
    performance: float = 3.0
    is_delight: bool = False
    is_dissatisfaction: bool = False

    def gap(self) -> float:
        return self.performance - self.importance

    def priority_score(self) -> float:
        return self.importance * (5.0 - self.performance)


@dataclass
class LoyaltySegment:
    segment_type: str
    count: int = 0
    percentage: float = 0.0
    characteristics: List[str] = field(default_factory=list)
    strategy: str = ""


@dataclass
class CompetitiveLoss:
    competitor: str
    lost_customers: int = 0
    lost_revenue: float = 0.0
    reasons: List[str] = field(default_factory=list)
    recovery_cost: float = 0.0


@dataclass
class ICEAssessment:
    dimension: str
    current_score: float = 3.0
    target_score: float = 5.0
    gap_description: str = ""
    improvement_actions: List[str] = field(default_factory=list)


class LoyaltyAnalyzer:
    def __init__(self, company: str, industry: str):
        self._company = company
        self._industry = industry
        self._brand_rankings: List[BrandRanking] = []
        self._satisfaction_drivers: List[SatisfactionDriver] = []
        self._loyalty_segments: List[LoyaltySegment] = []
        self._competitive_losses: List[CompetitiveLoss] = []
        self._ice_assessments: List[ICEAssessment] = []

    def add_brand_ranking(self, brand: str, satisfaction_score: float,
                          rank: int, brand_count: int) -> "LoyaltyAnalyzer":
        br = BrandRanking(brand=brand, satisfaction_score=validate_score(satisfaction_score),
                          rank=rank, brand_count=brand_count)
        br.calculate_wallet_share()
        self._brand_rankings.append(br)
        return self

    def add_satisfaction_driver(self, name: str, importance: float = 3.0,
                                performance: float = 3.0,
                                is_delight: bool = False,
                                is_dissatisfaction: bool = False) -> "LoyaltyAnalyzer":
        self._satisfaction_drivers.append(SatisfactionDriver(
            name=name, importance=validate_score(importance),
            performance=validate_score(performance),
            is_delight=is_delight, is_dissatisfaction=is_dissatisfaction,
        ))
        return self

    def add_loyalty_segment(self, segment_type: str, count: int = 0,
                            percentage: float = 0.0,
                            characteristics: Optional[List[str]] = None,
                            strategy: str = "") -> "LoyaltyAnalyzer":
        if segment_type not in LOYALTY_CUSTOMER_SEGMENTS:
            raise ValueError(f"无效客户分层: {segment_type}")
        c = characteristics if characteristics is not None else []
        self._loyalty_segments.append(LoyaltySegment(
            segment_type=segment_type, count=count, percentage=percentage,
            characteristics=c, strategy=strategy,
        ))
        return self

    def add_competitive_loss(self, competitor: str, lost_customers: int = 0,
                             lost_revenue: float = 0.0,
                             reasons: Optional[List[str]] = None,
                             recovery_cost: float = 0.0) -> "LoyaltyAnalyzer":
        r = reasons if reasons is not None else []
        self._competitive_losses.append(CompetitiveLoss(
            competitor=competitor, lost_customers=lost_customers,
            lost_revenue=lost_revenue, reasons=r, recovery_cost=recovery_cost,
        ))
        return self

    def add_ice_assessment(self, dimension: str, current_score: float = 3.0,
                           target_score: float = 5.0, gap_description: str = "",
                           improvement_actions: Optional[List[str]] = None) -> "LoyaltyAnalyzer":
        if dimension not in ICE_DIMENSIONS:
            raise ValueError(f"无效ICE维度: {dimension}，可选: {ICE_DIMENSIONS}")
        a = improvement_actions if improvement_actions is not None else []
        self._ice_assessments.append(ICEAssessment(
            dimension=dimension, current_score=validate_score(current_score),
            target_score=validate_score(target_score),
            gap_description=gap_description, improvement_actions=a,
        ))
        return self

    def get_company_wallet_share(self) -> float:
        for br in self._brand_rankings:
            if br.brand == self._company:
                return br.wallet_share
        return 0.0

    def get_company_rank(self) -> int:
        for br in self._brand_rankings:
            if br.brand == self._company:
                return br.rank
        return 0

    def get_priority_drivers(self, top_n: int = 5) -> List[SatisfactionDriver]:
        sorted_drivers = sorted(self._satisfaction_drivers, key=lambda d: -d.priority_score())
        return sorted_drivers[:top_n]

    def render_markdown(self) -> str:
        parts = [f"# 客户满意度与忠诚度分析 — {self._company}\n"]
        if self._brand_rankings:
            rows = []
            for br in sorted(self._brand_rankings, key=lambda x: x.rank):
                rows.append([br.brand, f"{br.satisfaction_score:.1f}",
                             str(br.rank), str(br.brand_count),
                             f"{br.wallet_share:.1%}"])
            table = format_table(["品牌", "满意度", "排名", "品牌数", "钱包份额"], rows)
            ws = self.get_company_wallet_share()
            rk = self.get_company_rank()
            ranking_strats: List[str] = []
            if self._competitive_losses:
                for cl in sorted(self._competitive_losses, key=lambda x: -x.lost_revenue):
                    reasons_str = "、".join(cl.reasons[:3]) if cl.reasons else "未知"
                    ranking_strats.append(
                        f"流失到{cl.competitor}: {cl.lost_customers}人, "
                        f"营收损失{cl.lost_revenue:.0f}, 原因: {reasons_str}"
                    )
            parts.append(WAO_TEMPLATE.format(
                company=self._company,
                brand_rankings=table,
                competitive_loss=format_list(ranking_strats) if ranking_strats else "*暂无流失数据*",
                ranking_strategies=(
                    f"当前排名第{rk}，钱包份额{ws:.1%}。"
                    f"{'需提升排名以增加钱包份额。' if rk > 1 else '保持领先地位。'}"
                ),
            ))
        if self._satisfaction_drivers:
            delight = [d for d in self._satisfaction_drivers if d.is_delight]
            dissatisfaction = [d for d in self._satisfaction_drivers if d.is_dissatisfaction]
            priority = self.get_priority_drivers()
            seg_rows = []
            for ls in self._loyalty_segments:
                info = LOYALTY_CUSTOMER_SEGMENTS.get(ls.segment_type, {})
                seg_rows.append([info.get("label", ls.segment_type),
                                 f"{ls.percentage:.0f}%", str(ls.count),
                                 ls.strategy or info.get("strategy", "")])
            parts.append(LOYALTY_TEMPLATE.format(
                company=self._company,
                customer_segments=format_table(
                    ["客户类型", "占比", "数量", "策略"], seg_rows
                ) if seg_rows else "*暂无分层数据*",
                loyalty_drivers=format_list(
                    [f"{d.name} (重要性{d.importance:.1f}, 表现{d.performance:.1f})" for d in delight]
                ) if delight else "*暂无愉悦因素数据*",
                dissatisfaction_drivers=format_list(
                    [f"{d.name} (重要性{d.importance:.1f}, 表现{d.performance:.1f})" for d in dissatisfaction]
                ) if dissatisfaction else "*暂无不满因素数据*",
                improvement_plans=format_list(
                    [f"优先改善: {d.name} (优先级分{d.priority_score():.1f})" for d in priority]
                ),
            ))
        if self._ice_assessments:
            ice_rows = [[a.dimension, format_score_bar(a.current_score),
                         format_score_bar(a.target_score),
                         a.gap_description] for a in self._ice_assessments]
            exp_design: List[str] = []
            for a in self._ice_assessments:
                if a.improvement_actions:
                    exp_design.append(f"**{a.dimension}**: " + "、".join(a.improvement_actions))
            parts.append(ICE_TEMPLATE.format(
                company=self._company,
                dimensions=format_table(["维度", "当前", "目标", "差距"], ice_rows),
                pillars=format_list(ICE_PILLARS),
                gap_analysis=format_list(
                    [f"{a.dimension}: {a.gap_description}" for a in self._ice_assessments if a.gap_description]
                ) if any(a.gap_description for a in self._ice_assessments) else "*暂无差距数据*",
                experience_design="\n\n".join(exp_design) if exp_design else "*暂无设计建议*",
            ))
        return "\n\n".join(parts)

    def render_json(self) -> str:
        data = {
            "company": self._company, "industry": self._industry,
            "wao": {
                "brand_rankings": [
                    {"brand": br.brand, "satisfaction": br.satisfaction_score,
                     "rank": br.rank, "brand_count": br.brand_count,
                     "wallet_share": br.wallet_share}
                    for br in self._brand_rankings
                ],
                "company_wallet_share": self.get_company_wallet_share(),
                "company_rank": self.get_company_rank(),
            },
            "satisfaction_drivers": [
                {"name": d.name, "importance": d.importance,
                 "performance": d.performance, "gap": d.gap(),
                 "priority_score": d.priority_score(),
                 "is_delight": d.is_delight,
                 "is_dissatisfaction": d.is_dissatisfaction}
                for d in self._satisfaction_drivers
            ],
            "loyalty_segments": [
                {"type": ls.segment_type, "count": ls.count,
                 "percentage": ls.percentage, "strategy": ls.strategy}
                for ls in self._loyalty_segments
            ],
            "competitive_losses": [
                {"competitor": cl.competitor, "lost_customers": cl.lost_customers,
                 "lost_revenue": cl.lost_revenue, "reasons": cl.reasons,
                 "recovery_cost": cl.recovery_cost}
                for cl in self._competitive_losses
            ],
            "ice": [
                {"dimension": a.dimension, "current": a.current_score,
                 "target": a.target_score, "gap": a.gap_description,
                 "actions": a.improvement_actions}
                for a in self._ice_assessments
            ],
        }
        return format_as_json(data)

    def get_knowledge(self) -> str:
        return load_knowledge("loyalty_satisfaction")
