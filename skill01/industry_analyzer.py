from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .config import (
    FIVE_FORCES, FIVE_FORCES_LABELS, INDUSTRY_LIFECYCLE_STAGES,
)
from .templates import FIVE_FORCES_TEMPLATE
from .utils import (
    calculate_weighted_total, format_score_bar,
    format_table, normalize_weights, score_to_level, validate_score,
    validate_weight, load_knowledge, format_as_json,
)


@dataclass
class ForceDriver:
    force: str
    name: str
    description: str
    score: float = 3.0
    weight: float = 0.2

    def validate(self) -> List[str]:
        errors: List[str] = []
        if self.force not in FIVE_FORCES:
            errors.append(f"无效竞争力量: {self.force}，可选: {FIVE_FORCES}")
        if not 1.0 <= self.score <= 5.0:
            errors.append(f"评分必须在1-5之间，当前: {self.score}")
        return errors


@dataclass
class CompetitorProfile:
    name: str
    market_share: float = 0.0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    strategy: str = ""
    strategic_group: str = ""


@dataclass
class KSF:
    name: str
    weight: float = 0.1
    company_score: float = 3.0
    competitor_scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class IndustryAnalysis:
    company: str
    industry: str
    lifecycle_stage: str = "maturity"
    drivers: List[ForceDriver] = field(default_factory=list)
    competitors: List[CompetitorProfile] = field(default_factory=list)
    ksf_list: List[KSF] = field(default_factory=list)

    def force_score(self, force: str) -> float:
        force_drivers = [d for d in self.drivers if d.force == force]
        if not force_drivers:
            return 0.0
        total_w = sum(d.weight for d in force_drivers)
        if total_w == 0:
            return 0.0
        return sum(d.score * d.weight for d in force_drivers) / total_w

    def overall_attractiveness(self) -> float:
        if not self.drivers:
            return 0.0
        scores = []
        for force in FIVE_FORCES:
            fs = self.force_score(force)
            if fs > 0:
                scores.append(5.0 - fs + 1.0)
        return sum(scores) / len(scores) if scores else 0.0

    def cpm_scores(self) -> Dict[str, float]:
        result: Dict[str, float] = {}
        if not self.ksf_list:
            return result
        normalized = normalize_weights(
            [{"weight": k.weight, "score": k.company_score} for k in self.ksf_list]
        )
        result[self.company] = calculate_weighted_total(normalized)
        all_competitors = set()
        for k in self.ksf_list:
            all_competitors.update(k.competitor_scores.keys())
        for comp in all_competitors:
            comp_factors = normalize_weights(
                [{"weight": k.weight, "score": k.competitor_scores.get(comp, 3.0)}
                 for k in self.ksf_list]
            )
            result[comp] = calculate_weighted_total(comp_factors)
        return result


class IndustryAnalyzer:
    def __init__(self, company: str, industry: str):
        self._analysis = IndustryAnalysis(company=company, industry=industry)

    def set_lifecycle_stage(self, stage: str) -> "IndustryAnalyzer":
        if stage not in INDUSTRY_LIFECYCLE_STAGES:
            raise ValueError(f"无效阶段: {stage}，可选: {list(INDUSTRY_LIFECYCLE_STAGES.keys())}")
        self._analysis.lifecycle_stage = stage
        return self

    def add_force_driver(
        self, force: str, name: str, description: str,
        score: float = 3.0, weight: float = 0.2,
    ) -> "IndustryAnalyzer":
        driver = ForceDriver(
            force=force, name=name, description=description,
            score=validate_score(score), weight=validate_weight(weight),
        )
        errors = driver.validate()
        if errors:
            raise ValueError(f"驱动因素验证失败: {'; '.join(errors)}")
        self._analysis.drivers.append(driver)
        return self

    def add_competitor(
        self, name: str, market_share: float = 0.0,
        strengths: Optional[List[str]] = None,
        weaknesses: Optional[List[str]] = None,
        strategy: str = "", strategic_group: str = "",
    ) -> "IndustryAnalyzer":
        s = strengths if strengths is not None else []
        w = weaknesses if weaknesses is not None else []
        self._analysis.competitors.append(CompetitorProfile(
            name=name, market_share=market_share,
            strengths=s, weaknesses=w,
            strategy=strategy, strategic_group=strategic_group,
        ))
        return self

    def add_ksf(
        self, name: str, weight: float = 0.1,
        company_score: float = 3.0,
        competitor_scores: Optional[Dict[str, float]] = None,
    ) -> "IndustryAnalyzer":
        cs = competitor_scores if competitor_scores is not None else {}
        self._analysis.ksf_list.append(KSF(
            name=name, weight=validate_weight(weight),
            company_score=validate_score(company_score),
            competitor_scores=cs,
        ))
        return self

    def get_attractiveness_assessment(self) -> str:
        score = self._analysis.overall_attractiveness()
        if score >= 4.0:
            return "行业吸引力非常高，盈利潜力大"
        if score >= 3.0:
            return "行业吸引力较高，存在良好盈利机会"
        if score >= 2.5:
            return "行业吸引力中等，竞争较为激烈"
        if score >= 2.0:
            return "行业吸引力较低，盈利空间受限"
        return "行业吸引力很低，竞争极为激烈"

    def get_lifecycle_insights(self) -> List[str]:
        stage = self._analysis.lifecycle_stage
        info = INDUSTRY_LIFECYCLE_STAGES[stage]
        insights = [
            f"行业当前处于{info['label']}",
            f"阶段特征: {info['features']}",
            f"战略重点: {info['strategy']}",
        ]
        return insights

    def render_markdown(self) -> str:
        a = self._analysis
        forces_parts: List[str] = []
        for force in FIVE_FORCES:
            label = FIVE_FORCES_LABELS[force]
            drivers = [d for d in a.drivers if d.force == force]
            if not drivers:
                forces_parts.append(f"### {label}\n\n*暂无评估数据*\n")
                continue
            rows = [[d.name, d.description, f"{d.weight:.2f}",
                     format_score_bar(d.score)] for d in drivers]
            table = format_table(["驱动因素", "描述", "权重", "评分"], rows)
            fs = a.force_score(force)
            threat = "高" if fs >= 4.0 else ("中" if fs >= 2.5 else "低")
            forces_parts.append(
                f"### {label}\n\n{table}\n\n"
                f"**竞争力量强度**: {fs:.2f} — 威胁程度: {threat}\n"
            )
        ksf_section = ""
        if a.ksf_list:
            cpm = a.cpm_scores()
            rows = []
            for k in a.ksf_list:
                row = [k.name, f"{k.weight:.2f}", f"{k.company_score:.1f}"]
                for comp in sorted(set(c for ks in a.ksf_list for c in ks.competitor_scores)):
                    row.append(f"{k.competitor_scores.get(comp, 3.0):.1f}")
                rows.append(row)
            headers = ["关键成功因素", "权重", a.company]
            comp_names = sorted(set(c for ks in a.ksf_list for c in ks.competitor_scores))
            headers.extend(comp_names)
            ksf_section = format_table(headers, rows)
            ksf_section += "\n\n**竞争态势矩阵(CPM)总分**:\n"
            for name, score in sorted(cpm.items(), key=lambda x: -x[1]):
                ksf_section += f"- {name}: {score:.2f}\n"

        lifecycle = INDUSTRY_LIFECYCLE_STAGES[a.lifecycle_stage]
        ksf_section += f"\n### 行业生命周期\n\n当前阶段: **{lifecycle['label']}**\n"
        ksf_section += f"- 特征: {lifecycle['features']}\n"
        ksf_section += f"- 战略重点: {lifecycle['strategy']}\n"

        attractiveness = a.overall_attractiveness()
        return FIVE_FORCES_TEMPLATE.format(
            company=a.company, industry=a.industry,
            forces_section="\n".join(forces_parts),
            total_score=attractiveness, max_score=5,
            attractiveness=self.get_attractiveness_assessment(),
            profitability=score_to_level(attractiveness),
            ksf_section=ksf_section,
        )

    def render_json(self) -> str:
        a = self._analysis
        data = {
            "company": a.company, "industry": a.industry,
            "lifecycle_stage": a.lifecycle_stage,
            "force_scores": {f: a.force_score(f) for f in FIVE_FORCES},
            "overall_attractiveness": a.overall_attractiveness(),
            "assessment": self.get_attractiveness_assessment(),
            "drivers": [
                {"force": d.force, "name": d.name, "description": d.description,
                 "score": d.score, "weight": d.weight}
                for d in a.drivers
            ],
            "competitors": [
                {"name": c.name, "market_share": c.market_share,
                 "strengths": c.strengths, "weaknesses": c.weaknesses,
                 "strategy": c.strategy, "strategic_group": c.strategic_group}
                for c in a.competitors
            ],
            "ksf": [
                {"name": k.name, "weight": k.weight,
                 "company_score": k.company_score,
                 "competitor_scores": k.competitor_scores}
                for k in a.ksf_list
            ],
            "cpm_scores": a.cpm_scores(),
            "lifecycle_insights": self.get_lifecycle_insights(),
        }
        return format_as_json(data)

    def get_knowledge(self) -> str:
        return load_knowledge("industry_competition")
