from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .config import VALUE_PYRAMID_LAYERS, ALL_VALUE_ELEMENTS, INDUSTRY_VALUE_PROFILES
from .templates import VALUE_PYRAMID_TEMPLATE, STP_TEMPLATE, MARKETING_MIX_TEMPLATE
from .utils import (
    format_list, format_table, format_score_bar, score_to_level,
    validate_score, load_knowledge, format_as_json,
)


@dataclass
class ValueElementScore:
    element: str
    score: float = 3.0
    competitor_scores: Dict[str, float] = field(default_factory=dict)
    importance: float = 3.0

    def is_high_performing(self, threshold: float = 4.0) -> bool:
        return self.score >= threshold

    def competitive_gap(self) -> Dict[str, float]:
        return {c: self.score - s for c, s in self.competitor_scores.items()}


@dataclass
class Segment:
    name: str
    size: str = ""
    growth: str = ""
    characteristics: List[str] = field(default_factory=list)
    needs: List[str] = field(default_factory=list)
    is_target: bool = False


@dataclass
class Positioning:
    target_segment: str = ""
    value_proposition: str = ""
    differentiation: str = ""
    reason_to_believe: str = ""


@dataclass
class MarketingMixItem:
    dimension: str
    assessment: str = ""
    score: float = 3.0
    recommendations: List[str] = field(default_factory=list)


class ConsumerAnalyzer:
    def __init__(self, company: str, industry: str):
        self._company = company
        self._industry = industry
        self._value_scores: List[ValueElementScore] = []
        self._segments: List[Segment] = []
        self._positioning = Positioning()
        self._marketing_mix: List[MarketingMixItem] = []

    def add_value_score(self, element: str, score: float = 3.0,
                        competitor_scores: Optional[Dict[str, float]] = None,
                        importance: float = 3.0) -> "ConsumerAnalyzer":
        if element not in ALL_VALUE_ELEMENTS:
            raise ValueError(f"无效价值要素: {element}")
        cs = competitor_scores if competitor_scores is not None else {}
        self._value_scores.append(ValueElementScore(
            element=element, score=validate_score(score),
            competitor_scores=cs, importance=importance,
        ))
        return self

    def add_segment(self, name: str, size: str = "", growth: str = "",
                    characteristics: Optional[List[str]] = None,
                    needs: Optional[List[str]] = None,
                    is_target: bool = False) -> "ConsumerAnalyzer":
        c = characteristics if characteristics is not None else []
        n = needs if needs is not None else []
        self._segments.append(Segment(
            name=name, size=size, growth=growth,
            characteristics=c, needs=n, is_target=is_target,
        ))
        return self

    def set_positioning(self, target_segment: str, value_proposition: str,
                        differentiation: str = "",
                        reason_to_believe: str = "") -> "ConsumerAnalyzer":
        self._positioning = Positioning(
            target_segment=target_segment, value_proposition=value_proposition,
            differentiation=differentiation, reason_to_believe=reason_to_believe,
        )
        return self

    def add_marketing_mix(self, dimension: str, assessment: str,
                          score: float = 3.0,
                          recommendations: Optional[List[str]] = None) -> "ConsumerAnalyzer":
        r = recommendations if recommendations is not None else []
        self._marketing_mix.append(MarketingMixItem(
            dimension=dimension, assessment=assessment,
            score=validate_score(score), recommendations=r,
        ))
        return self

    def get_high_performing_elements(self, threshold: float = 4.0) -> List[ValueElementScore]:
        return [v for v in self._value_scores if v.is_high_performing(threshold)]

    def get_value_pyramid_summary(self) -> Dict[str, List[ValueElementScore]]:
        result: Dict[str, List[ValueElementScore]] = {}
        for layer_key, layer_info in VALUE_PYRAMID_LAYERS.items():
            elements = layer_info["elements"]
            result[layer_key] = [v for v in self._value_scores if v.element in elements]
        return result

    def get_industry_benchmark(self) -> List[str]:
        return INDUSTRY_VALUE_PROFILES.get(self._industry, [])

    def count_high_elements(self, threshold: float = 4.0) -> int:
        return len(self.get_high_performing_elements(threshold))

    def get_nps_prediction(self) -> str:
        count = self.count_high_elements()
        if count >= 4:
            return "NPS预期较高（4+要素高分，NPS约为仅1个高分要素企业的3倍）"
        if count >= 1:
            return "NPS预期中等（1-3个高分要素）"
        return "NPS预期较低（无高分要素，NPS远低于行业平均）"

    def _render_value_scores(self, layer_key: str) -> str:
        pyramid = self.get_value_pyramid_summary()
        scores = pyramid.get(layer_key, [])
        if not scores:
            return "*暂无评分数据*"
        rows = []
        for v in sorted(scores, key=lambda x: -x.score):
            comp_str = ", ".join(f"{c}: {s:.1f}" for c, s in v.competitor_scores.items())
            rows.append([v.element, format_score_bar(v.score),
                         comp_str if comp_str else "-",
                         "✓" if v.is_high_performing() else ""])
        return format_table(["要素", "评分", "竞争对手", "高分"], rows)

    def render_markdown(self) -> str:
        parts = [f"# 消费者洞察分析 — {self._company}\n"]
        if self._value_scores:
            benchmark = self.get_industry_benchmark()
            bench_str = format_list(benchmark) if benchmark else "*暂无行业标杆数据*"
            high = self.get_high_performing_elements()
            opt: List[str] = []
            if benchmark:
                scored_elements = {v.element for v in self._value_scores}
                missing = [b for b in benchmark if b not in scored_elements]
                low = [v for v in self._value_scores if v.element in benchmark and v.score < 3.5]
                if missing:
                    opt.append(f"行业关键要素中尚未评估: {', '.join(missing)}")
                if low:
                    opt.append(f"行业关键要素中表现不足: {', '.join(v.element for v in low)}")
            if high:
                opt.append(f"高分要素({len(high)}个): {', '.join(v.element for v in high)}")
            opt.append(self.get_nps_prediction())
            parts.append(VALUE_PYRAMID_TEMPLATE.format(
                company=self._company, industry=self._industry,
                social_impact_scores=self._render_value_scores("social_impact"),
                life_changing_scores=self._render_value_scores("life_changing"),
                emotional_scores=self._render_value_scores("emotional"),
                functional_scores=self._render_value_scores("functional"),
                benchmark_comparison=bench_str,
                optimization_suggestions=format_list(opt, numbered=True),
            ))
        if self._segments:
            seg_rows = []
            for s in self._segments:
                seg_rows.append([s.name, s.size, s.growth,
                                 "、".join(s.characteristics[:3]),
                                 "✓" if s.is_target else ""])
            seg_table = format_table(["细分市场", "规模", "增长", "特征", "目标"], seg_rows)
            p = self._positioning
            pos_str = (f"**目标客群**: {p.target_segment}\n\n"
                       f"**价值主张**: {p.value_proposition}\n\n"
                       f"**差异化**: {p.differentiation}\n\n"
                       f"**信任理由**: {p.reason_to_believe}")
            parts.append(STP_TEMPLATE.format(
                company=self._company, segmentation=seg_table,
                targeting=format_list([s.name for s in self._segments if s.is_target]),
                positioning=pos_str,
            ))
        if self._marketing_mix:
            p4 = [m for m in self._marketing_mix if m.dimension in ("产品", "价格", "渠道", "促销")]
            c4 = [m for m in self._marketing_mix if m.dimension in ("消费者需求", "成本", "便利性", "沟通")]
            r4 = [m for m in self._marketing_mix if m.dimension in ("关联", "反应", "关系", "回报")]

            def fmt_mix(items: List[MarketingMixItem]) -> str:
                if not items:
                    return "*暂无数据*"
                rows = [[m.dimension, m.assessment, format_score_bar(m.score),
                         "、".join(m.recommendations[:2])] for m in items]
                return format_table(["维度", "评估", "评分", "建议"], rows)

            parts.append(MARKETING_MIX_TEMPLATE.format(
                company=self._company, four_p=fmt_mix(p4),
                four_c=fmt_mix(c4), four_r=fmt_mix(r4),
            ))
        return "\n\n".join(parts)

    def render_json(self) -> str:
        data = {
            "company": self._company, "industry": self._industry,
            "value_scores": [{"element": v.element, "score": v.score,
                              "competitor_scores": v.competitor_scores,
                              "importance": v.importance,
                              "is_high": v.is_high_performing()}
                             for v in self._value_scores],
            "high_performing_count": self.count_high_elements(),
            "nps_prediction": self.get_nps_prediction(),
            "industry_benchmark": self.get_industry_benchmark(),
            "segments": [{"name": s.name, "size": s.size, "growth": s.growth,
                          "characteristics": s.characteristics, "needs": s.needs,
                          "is_target": s.is_target} for s in self._segments],
            "positioning": {"target": self._positioning.target_segment,
                            "value_proposition": self._positioning.value_proposition,
                            "differentiation": self._positioning.differentiation,
                            "rtb": self._positioning.reason_to_believe},
            "marketing_mix": [{"dimension": m.dimension, "assessment": m.assessment,
                               "score": m.score, "recommendations": m.recommendations}
                              for m in self._marketing_mix],
        }
        return format_as_json(data)

    def get_knowledge(self) -> str:
        return load_knowledge("consumer_insight")
