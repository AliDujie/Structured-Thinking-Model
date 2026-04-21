from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

from .config import (
    PEST_DIMENSIONS, PESTEL_DIMENSIONS, PEST_LABELS, SCORING_SCALE,
)
from .templates import PEST_ANALYSIS_TEMPLATE
from .utils import (
    calculate_weighted_total, format_list, format_score_bar,
    format_table, normalize_weights, score_to_level, validate_score,
    validate_weight, load_knowledge, format_as_json,
)


@dataclass
class PESTFactor:
    dimension: str
    name: str
    description: str
    score: float = 3.0
    weight: float = 0.1
    trend: str = "稳定"
    impact: str = "中等"

    def validate(self) -> List[str]:
        errors: List[str] = []
        dims = PESTEL_DIMENSIONS
        if self.dimension not in dims:
            errors.append(f"无效维度: {self.dimension}，可选: {dims}")
        if not 1.0 <= self.score <= 5.0:
            errors.append(f"评分必须在1-5之间，当前: {self.score}")
        if not 0.0 <= self.weight <= 1.0:
            errors.append(f"权重必须在0-1之间，当前: {self.weight}")
        if self.trend not in ("上升", "稳定", "下降"):
            errors.append(f"趋势必须为 上升/稳定/下降，当前: {self.trend}")
        return errors


@dataclass
class PESTAnalysis:
    company: str
    industry: str
    mode: str = "pestel"
    factors: List[PESTFactor] = field(default_factory=list)

    def factors_by_dimension(self) -> Dict[str, List[PESTFactor]]:
        result: Dict[str, List[PESTFactor]] = {}
        dims = PESTEL_DIMENSIONS if self.mode == "pestel" else PEST_DIMENSIONS
        for d in dims:
            result[d] = [f for f in self.factors if f.dimension == d]
        return result

    def dimension_score(self, dimension: str) -> float:
        dim_factors = [f for f in self.factors if f.dimension == dimension]
        if not dim_factors:
            return 0.0
        return sum(f.score * f.weight for f in dim_factors) / sum(f.weight for f in dim_factors)

    def efe_score(self) -> float:
        if not self.factors:
            return 0.0
        normalized = normalize_weights(
            [{"weight": f.weight, "score": f.score} for f in self.factors]
        )
        return calculate_weighted_total(normalized)

    def assessment(self) -> str:
        score = self.efe_score()
        if score >= 4.0:
            return "外部环境非常有利，存在大量战略机会"
        if score >= 3.0:
            return "外部环境总体有利，机会大于威胁"
        if score >= 2.5:
            return "外部环境中性，机会与威胁并存"
        if score >= 2.0:
            return "外部环境不利，威胁大于机会"
        return "外部环境非常不利，面临严峻挑战"


class MacroAnalyzer:
    def __init__(self, company: str, industry: str, mode: str = "pestel"):
        self._analysis = PESTAnalysis(company=company, industry=industry, mode=mode)

    def add_factor(
        self, dimension: str, name: str, description: str,
        score: float = 3.0, weight: float = 0.1,
        trend: str = "稳定", impact: str = "中等",
    ) -> "MacroAnalyzer":
        factor = PESTFactor(
            dimension=dimension, name=name, description=description,
            score=validate_score(score), weight=validate_weight(weight),
            trend=trend, impact=impact,
        )
        errors = factor.validate()
        if errors:
            raise ValueError(f"因素验证失败: {'; '.join(errors)}")
        self._analysis.factors.append(factor)
        return self

    def add_factors_batch(self, factors: List[Dict]) -> "MacroAnalyzer":
        for f in factors:
            self.add_factor(**f)
        return self

    def get_key_findings(self) -> List[str]:
        findings: List[str] = []
        by_dim = self._analysis.factors_by_dimension()
        for dim, factors in by_dim.items():
            if not factors:
                continue
            high_impact = [f for f in factors if f.score >= 4.0]
            low_impact = [f for f in factors if f.score <= 2.0]
            rising = [f for f in factors if f.trend == "上升"]
            if high_impact:
                names = "、".join(f.name for f in high_impact)
                findings.append(f"{PEST_LABELS[dim]}中，{names}表现有利，构成战略机会")
            if low_impact:
                names = "、".join(f.name for f in low_impact)
                findings.append(f"{PEST_LABELS[dim]}中，{names}表现不利，构成潜在威胁")
            if rising:
                names = "、".join(f.name for f in rising)
                findings.append(f"{PEST_LABELS[dim]}中，{names}呈上升趋势，需持续关注")
        return findings

    def get_implications(self) -> List[str]:
        implications: List[str] = []
        score = self._analysis.efe_score()
        if score >= 3.0:
            implications.append("外部环境总体有利，建议采取积极进取的增长战略")
        else:
            implications.append("外部环境存在较多挑战，建议采取审慎防御的战略姿态")
        by_dim = self._analysis.factors_by_dimension()
        for dim, factors in by_dim.items():
            if not factors:
                continue
            dim_score = self._analysis.dimension_score(dim)
            if dim_score >= 4.0:
                implications.append(f"{PEST_LABELS[dim]}环境非常有利，可作为战略发力点")
            elif dim_score <= 2.0:
                implications.append(f"{PEST_LABELS[dim]}环境不利，需制定风险应对预案")
        return implications

    def render_markdown(self) -> str:
        a = self._analysis
        sections: List[str] = []
        by_dim = a.factors_by_dimension()
        for dim, factors in by_dim.items():
            if not factors:
                continue
            label = PEST_LABELS[dim]
            rows = []
            for f in factors:
                rows.append([f.name, f.description, f"{f.weight:.2f}",
                             format_score_bar(f.score), f.trend, f.impact])
            table = format_table(
                ["因素", "描述", "权重", "评分", "趋势", "影响程度"], rows
            )
            dim_score = a.dimension_score(dim)
            sections.append(f"### {label}\n\n{table}\n\n"
                            f"**维度综合评分**: {dim_score:.2f} — {score_to_level(dim_score)}\n")
        el = "EL" if a.mode == "pestel" else ""
        return PEST_ANALYSIS_TEMPLATE.format(
            el=el, company=a.company, industry=a.industry,
            date=date.today().isoformat(), mode=a.mode.upper(),
            factors_section="\n".join(sections),
            efe_score=a.efe_score(), max_score=5,
            assessment=a.assessment(),
            key_findings=format_list(self.get_key_findings(), numbered=True),
            implications=format_list(self.get_implications(), numbered=True),
        )

    def render_json(self) -> str:
        a = self._analysis
        data = {
            "company": a.company,
            "industry": a.industry,
            "mode": a.mode,
            "date": date.today().isoformat(),
            "factors": [
                {
                    "dimension": f.dimension, "name": f.name,
                    "description": f.description, "score": f.score,
                    "weight": f.weight, "trend": f.trend, "impact": f.impact,
                }
                for f in a.factors
            ],
            "dimension_scores": {
                d: a.dimension_score(d) for d in a.factors_by_dimension()
            },
            "efe_score": a.efe_score(),
            "assessment": a.assessment(),
            "key_findings": self.get_key_findings(),
            "implications": self.get_implications(),
        }
        return format_as_json(data)

    def get_knowledge(self) -> str:
        return load_knowledge("macro_environment")
