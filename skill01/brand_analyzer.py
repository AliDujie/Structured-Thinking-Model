from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .config import BRAND_LOYALTY_LEVELS
from .templates import BRAND_TEMPLATE
from .utils import (
    format_list, format_table, format_score_bar, validate_score,
    load_knowledge, format_as_json,
)


@dataclass
class BrandAwareness:
    top_of_mind: float = 0.0
    aided_awareness: float = 0.0
    recognition: float = 0.0
    assessment: str = ""


@dataclass
class BrandAssociation:
    attribute: str
    strength: float = 3.0
    uniqueness: float = 3.0
    favorability: float = 3.0

    def overall(self) -> float:
        return (self.strength + self.uniqueness + self.favorability) / 3.0


@dataclass
class BrandImageDimension:
    dimension: str
    score: float = 3.0
    competitor_scores: Dict[str, float] = field(default_factory=dict)
    description: str = ""


@dataclass
class CompetitorBrand:
    name: str
    awareness: float = 0.0
    image_score: float = 3.0
    loyalty_level: int = 1
    key_strengths: List[str] = field(default_factory=list)
    key_weaknesses: List[str] = field(default_factory=list)
    value_proposition: str = ""


@dataclass
class DifferentiationStrategy:
    strategy_type: str
    description: str
    feasibility: float = 3.0
    impact: float = 3.0
    actions: List[str] = field(default_factory=list)

    def priority_score(self) -> float:
        return self.feasibility * self.impact


class BrandAnalyzer:
    def __init__(self, company: str, industry: str):
        self._company = company
        self._industry = industry
        self._awareness = BrandAwareness()
        self._associations: List[BrandAssociation] = []
        self._image_dims: List[BrandImageDimension] = []
        self._loyalty_level: int = 1
        self._loyalty_distribution: Dict[int, float] = {}
        self._competitors: List[CompetitorBrand] = []
        self._differentiations: List[DifferentiationStrategy] = []

    def set_awareness(self, top_of_mind: float = 0.0,
                      aided_awareness: float = 0.0,
                      recognition: float = 0.0,
                      assessment: str = "") -> "BrandAnalyzer":
        self._awareness = BrandAwareness(
            top_of_mind=top_of_mind, aided_awareness=aided_awareness,
            recognition=recognition, assessment=assessment,
        )
        return self

    def add_association(self, attribute: str, strength: float = 3.0,
                        uniqueness: float = 3.0,
                        favorability: float = 3.0) -> "BrandAnalyzer":
        self._associations.append(BrandAssociation(
            attribute=attribute, strength=validate_score(strength),
            uniqueness=validate_score(uniqueness),
            favorability=validate_score(favorability),
        ))
        return self

    def add_image_dimension(self, dimension: str, score: float = 3.0,
                            competitor_scores: Optional[Dict[str, float]] = None,
                            description: str = "") -> "BrandAnalyzer":
        cs = competitor_scores if competitor_scores is not None else {}
        self._image_dims.append(BrandImageDimension(
            dimension=dimension, score=validate_score(score),
            competitor_scores=cs, description=description,
        ))
        return self

    def set_loyalty(self, level: int,
                    distribution: Optional[Dict[int, float]] = None) -> "BrandAnalyzer":
        if not 1 <= level <= 5:
            raise ValueError(f"忠诚度层级必须在1-5之间: {level}")
        self._loyalty_level = level
        self._loyalty_distribution = distribution if distribution is not None else {}
        return self

    def add_competitor_brand(self, name: str, awareness: float = 0.0,
                             image_score: float = 3.0, loyalty_level: int = 1,
                             key_strengths: Optional[List[str]] = None,
                             key_weaknesses: Optional[List[str]] = None,
                             value_proposition: str = "") -> "BrandAnalyzer":
        s = key_strengths if key_strengths is not None else []
        w = key_weaknesses if key_weaknesses is not None else []
        self._competitors.append(CompetitorBrand(
            name=name, awareness=awareness, image_score=validate_score(image_score),
            loyalty_level=loyalty_level, key_strengths=s,
            key_weaknesses=w, value_proposition=value_proposition,
        ))
        return self

    def add_differentiation(self, strategy_type: str, description: str,
                            feasibility: float = 3.0, impact: float = 3.0,
                            actions: Optional[List[str]] = None) -> "BrandAnalyzer":
        valid_types = ("产品差异化", "服务差异化", "品牌形象差异化", "客户体验差异化")
        if strategy_type not in valid_types:
            raise ValueError(f"无效差异化类型: {strategy_type}，可选: {valid_types}")
        a = actions if actions is not None else []
        self._differentiations.append(DifferentiationStrategy(
            strategy_type=strategy_type, description=description,
            feasibility=validate_score(feasibility),
            impact=validate_score(impact), actions=a,
        ))
        return self

    def _get_loyalty_label(self, level: int) -> str:
        for item in BRAND_LOYALTY_LEVELS:
            if item["level"] == level:
                return item["label"]
        return "未知"

    def render_markdown(self) -> str:
        aw = self._awareness
        awareness_str = (
            f"- 无提示知名度 (Top of Mind): {aw.top_of_mind:.1f}%\n"
            f"- 提示后知名度: {aw.aided_awareness:.1f}%\n"
            f"- 品牌识别度: {aw.recognition:.1f}%\n"
            f"- 评估: {aw.assessment}"
        )
        assoc_str = "*暂无数据*"
        if self._associations:
            rows = [[a.attribute, format_score_bar(a.strength),
                     format_score_bar(a.uniqueness),
                     format_score_bar(a.favorability),
                     f"{a.overall():.1f}"]
                    for a in sorted(self._associations, key=lambda x: -x.overall())]
            assoc_str = format_table(["属性", "强度", "独特性", "好感度", "综合"], rows)
        image_str = "*暂无数据*"
        if self._image_dims:
            rows = []
            for d in self._image_dims:
                comp_str = ", ".join(f"{c}: {s:.1f}" for c, s in d.competitor_scores.items())
                rows.append([d.dimension, format_score_bar(d.score),
                             comp_str if comp_str else "-", d.description])
            image_str = format_table(["维度", "评分", "竞争对手", "说明"], rows)
        loyalty_label = self._get_loyalty_label(self._loyalty_level)
        loyalty_str = f"**当前忠诚度层级**: {self._loyalty_level}/5 — {loyalty_label}\n\n"
        if self._loyalty_distribution:
            for level, pct in sorted(self._loyalty_distribution.items()):
                label = self._get_loyalty_label(level)
                loyalty_str += f"- Level {level} ({label}): {pct:.1f}%\n"
        comp_str = "*暂无竞争品牌数据*"
        if self._competitors:
            rows = []
            for c in self._competitors:
                rows.append([c.name, f"{c.awareness:.1f}%",
                             format_score_bar(c.image_score),
                             self._get_loyalty_label(c.loyalty_level),
                             "、".join(c.key_strengths[:2]) if c.key_strengths else "-"])
            comp_str = format_table(["品牌", "知名度", "形象", "忠诚度", "核心优势"], rows)
        diff_str = "*暂无差异化策略*"
        if self._differentiations:
            parts: List[str] = []
            for d in sorted(self._differentiations, key=lambda x: -x.priority_score()):
                part = (f"**{d.strategy_type}** (优先级: {d.priority_score():.1f})\n\n"
                        f"{d.description}\n")
                if d.actions:
                    part += "\n" + format_list(d.actions)
                parts.append(part)
            diff_str = "\n\n".join(parts)
        return BRAND_TEMPLATE.format(
            company=self._company, awareness=awareness_str,
            associations=assoc_str, image=image_str,
            loyalty=loyalty_str, competitive_comparison=comp_str,
            differentiation=diff_str,
        )

    def render_json(self) -> str:
        data = {
            "company": self._company, "industry": self._industry,
            "awareness": {"top_of_mind": self._awareness.top_of_mind,
                          "aided": self._awareness.aided_awareness,
                          "recognition": self._awareness.recognition},
            "associations": [{"attribute": a.attribute, "strength": a.strength,
                              "uniqueness": a.uniqueness, "favorability": a.favorability,
                              "overall": a.overall()} for a in self._associations],
            "image": [{"dimension": d.dimension, "score": d.score,
                       "competitor_scores": d.competitor_scores}
                      for d in self._image_dims],
            "loyalty": {"level": self._loyalty_level,
                        "label": self._get_loyalty_label(self._loyalty_level),
                        "distribution": self._loyalty_distribution},
            "competitors": [{"name": c.name, "awareness": c.awareness,
                             "image_score": c.image_score,
                             "loyalty_level": c.loyalty_level,
                             "strengths": c.key_strengths,
                             "weaknesses": c.key_weaknesses}
                            for c in self._competitors],
            "differentiation": [{"type": d.strategy_type, "description": d.description,
                                 "feasibility": d.feasibility, "impact": d.impact,
                                 "priority": d.priority_score(), "actions": d.actions}
                                for d in self._differentiations],
        }
        return format_as_json(data)

    def get_knowledge(self) -> str:
        return load_knowledge("brand_value")
