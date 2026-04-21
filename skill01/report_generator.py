from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional

from .config import RESEARCH_MODULES, RESEARCH_MODULE_LABELS, REPORT_CHAPTERS
from .templates import FULL_REPORT_TEMPLATE
from .utils import format_as_json, load_knowledge, search_knowledge


@dataclass
class ReportSection:
    title: str
    content: str = ""
    sub_sections: Dict[str, str] = field(default_factory=dict)

    def render(self) -> str:
        parts = [self.content] if self.content else []
        for sub_title, sub_content in self.sub_sections.items():
            parts.append(f"### {sub_title}\n\n{sub_content}")
        return "\n\n".join(parts)


@dataclass
class StrategicRecommendation:
    title: str
    description: str
    timeframe: str = "短期"
    priority: str = "高"
    expected_impact: str = ""
    actions: List[str] = field(default_factory=list)

    def render(self) -> str:
        lines = [
            f"**{self.title}** [{self.timeframe} | 优先级: {self.priority}]",
            "", self.description, "",
        ]
        if self.expected_impact:
            lines.append(f"预期效果: {self.expected_impact}")
        if self.actions:
            lines.append("\n行动计划:")
            for i, a in enumerate(self.actions, 1):
                lines.append(f"{i}. {a}")
        return "\n".join(lines)


@dataclass
class DiagnosticFinding:
    category: str
    finding: str
    severity: str = "中"
    evidence: str = ""
    recommendation: str = ""


class ReportGenerator:
    def __init__(self, company: str, industry: str):
        self._company = company
        self._industry = industry
        self._date = date.today().isoformat()
        self._scope = "全维度研究"
        self._sections: Dict[str, ReportSection] = {}
        self._recommendations: List[StrategicRecommendation] = []
        self._findings: List[DiagnosticFinding] = []
        self._executive_summary = ""
        self._company_overview = ""

    def set_scope(self, scope: str) -> "ReportGenerator":
        self._scope = scope
        return self

    def set_executive_summary(self, summary: str) -> "ReportGenerator":
        self._executive_summary = summary
        return self

    def set_company_overview(self, overview: str) -> "ReportGenerator":
        self._company_overview = overview
        return self

    def add_section(self, chapter: str, content: str,
                    sub_sections: Optional[Dict[str, str]] = None) -> "ReportGenerator":
        ss = sub_sections if sub_sections is not None else {}
        self._sections[chapter] = ReportSection(
            title=chapter, content=content, sub_sections=ss,
        )
        return self

    def add_module_output(self, module: str, markdown_output: str) -> "ReportGenerator":
        label = RESEARCH_MODULE_LABELS.get(module, module)
        self._sections[label] = ReportSection(title=label, content=markdown_output)
        return self

    def add_recommendation(self, title: str, description: str,
                           timeframe: str = "短期", priority: str = "高",
                           expected_impact: str = "",
                           actions: Optional[List[str]] = None) -> "ReportGenerator":
        a = actions if actions is not None else []
        self._recommendations.append(StrategicRecommendation(
            title=title, description=description, timeframe=timeframe,
            priority=priority, expected_impact=expected_impact, actions=a,
        ))
        return self

    def add_finding(self, category: str, finding: str,
                    severity: str = "中", evidence: str = "",
                    recommendation: str = "") -> "ReportGenerator":
        self._findings.append(DiagnosticFinding(
            category=category, finding=finding, severity=severity,
            evidence=evidence, recommendation=recommendation,
        ))
        return self

    def _render_diagnosis(self) -> str:
        if not self._findings:
            return "*综合诊断待完成*"
        parts: List[str] = []
        by_severity = {"高": [], "中": [], "低": []}
        for f in self._findings:
            by_severity.get(f.severity, by_severity["中"]).append(f)
        for sev in ["高", "中", "低"]:
            items = by_severity[sev]
            if not items:
                continue
            parts.append(f"### {sev}优先级发现\n")
            for f in items:
                line = f"**[{f.category}]** {f.finding}"
                if f.evidence:
                    line += f"\n- 证据: {f.evidence}"
                if f.recommendation:
                    line += f"\n- 建议: {f.recommendation}"
                parts.append(line)
        return "\n\n".join(parts)

    def _render_recommendations(self) -> str:
        if not self._recommendations:
            return "*战略建议待制定*"
        short = [r for r in self._recommendations if r.timeframe == "短期"]
        mid = [r for r in self._recommendations if r.timeframe == "中期"]
        long = [r for r in self._recommendations if r.timeframe == "长期"]
        parts: List[str] = []
        for label, items in [("短期行动计划", short), ("中期战略方向", mid), ("长期愿景", long)]:
            if items:
                parts.append(f"### {label}\n")
                for r in sorted(items, key=lambda x: {"高": 0, "中": 1, "低": 2}.get(x.priority, 1)):
                    parts.append(r.render())
        return "\n\n".join(parts)

    def add_resource_allocation(self, resource_type: str, area: str,
                                current_pct: float, recommended_pct: float,
                                rationale: str = "") -> "ReportGenerator":
        if not hasattr(self, "_resource_allocations"):
            self._resource_allocations: List[Dict] = []
        valid_types = ("资金", "人才", "时间")
        if resource_type not in valid_types:
            raise ValueError(f"resource_type 必须为 {valid_types} 之一")
        self._resource_allocations.append({
            "type": resource_type, "area": area,
            "current_pct": current_pct, "recommended_pct": recommended_pct,
            "rationale": rationale,
        })
        return self

    def add_failure_scenario(self, scenario: str, probability: str = "中",
                             impact: str = "高", trigger: str = "",
                             mitigation: str = "") -> "ReportGenerator":
        if not hasattr(self, "_failure_scenarios"):
            self._failure_scenarios: List[Dict] = []
        self._failure_scenarios.append({
            "scenario": scenario, "probability": probability,
            "impact": impact, "trigger": trigger, "mitigation": mitigation,
        })
        return self

    def generate_ceo_executive_summary(self) -> str:
        high_findings = [f for f in self._findings if f.severity == "高"]
        mid_findings = [f for f in self._findings if f.severity == "中"]
        high_recs = [r for r in self._recommendations if r.priority == "高"]

        total_factors = len(self._findings) + len(self._recommendations)
        positive = len([f for f in self._findings if f.severity == "低"])
        negative = len(high_findings)
        if total_factors == 0:
            health_score = 50
        else:
            health_score = max(0, min(100, int(
                50 + (positive - negative * 2) / max(total_factors, 1) * 50
            )))

        if health_score >= 70:
            health_label = "良好"
            health_desc = "企业整体战略健康，具备较强竞争力"
        elif health_score >= 40:
            health_label = "需关注"
            health_desc = "企业存在若干需要优先解决的战略问题"
        else:
            health_label = "预警"
            health_desc = "企业面临严峻挑战，需立即采取行动"

        lines = [
            f"## CEO 执行摘要\n",
            f"### 战略健康评分\n",
            f"**综合评分: {health_score}/100 — {health_label}**\n",
            f"{health_desc}\n",
            f"- 高优先级发现: {len(high_findings)} 项",
            f"- 中优先级发现: {len(mid_findings)} 项",
            f"- 高优先级建议: {len(high_recs)} 项\n",
            f"### Top 3 优先事项\n",
        ]

        priorities = sorted(self._recommendations,
                            key=lambda r: ({"高": 0, "中": 1, "低": 2}.get(r.priority, 1),
                                           {"短期": 0, "中期": 1, "长期": 2}.get(r.timeframe, 1)))
        for i, r in enumerate(priorities[:3], 1):
            lines.append(f"**{i}. {r.title}** [{r.timeframe} | {r.priority}优先级]")
            lines.append(f"   {r.description}")
            if r.expected_impact:
                lines.append(f"   预期效果: {r.expected_impact}")
            lines.append("")

        if not priorities:
            lines.append("*尚未制定战略建议，请补充分析数据*\n")

        lines.append("### 主要风险\n")
        if high_findings:
            for f in high_findings[:5]:
                risk_line = f"- **[{f.category}]** {f.finding}"
                if f.evidence:
                    risk_line += f" (证据: {f.evidence})"
                lines.append(risk_line)
        else:
            lines.append("*未识别到高优先级风险*")
        lines.append("")

        lines.append("### 关键决策点\n")
        decisions: List[str] = []
        short_recs = [r for r in self._recommendations if r.timeframe == "短期" and r.priority == "高"]
        for r in short_recs[:3]:
            decisions.append(f"- **是否立即启动「{r.title}」？** — {r.description}")
        if high_findings:
            decisions.append(f"- **是否需要调整当前战略方向？** — 已识别 {len(high_findings)} 项高优先级问题")
        if not decisions:
            decisions.append("- *当前无紧急决策事项*")
        lines.extend(decisions)
        lines.append("")

        return "\n".join(lines)

    def generate_failure_scenarios(self) -> str:
        lines = [
            "## 失败场景分析\n",
            "运用 Pre-Mortem 逆向反思法，假设战略已经失败，逆向推演可能的失败原因和应对措施。\n",
        ]

        scenarios = getattr(self, "_failure_scenarios", [])

        if not scenarios:
            high_findings = [f for f in self._findings if f.severity == "高"]
            for f in high_findings:
                scenarios.append({
                    "scenario": f"因「{f.finding}」导致战略失败",
                    "probability": "中", "impact": "高",
                    "trigger": f.evidence or "详见诊断发现",
                    "mitigation": f.recommendation or "需制定专项应对方案",
                })
            high_recs = [r for r in self._recommendations if r.priority == "高"]
            for r in high_recs:
                scenarios.append({
                    "scenario": f"「{r.title}」执行失败或未达预期",
                    "probability": "低", "impact": "高",
                    "trigger": "执行力不足、资源配置不当或外部环境剧变",
                    "mitigation": "建立阶段性里程碑和退出机制",
                })

        if not scenarios:
            lines.append("*暂无足够数据生成失败场景，请先完成诊断分析*\n")
            return "\n".join(lines)

        lines.append("| 序号 | 失败场景 | 发生概率 | 影响程度 | 触发条件 | 应对措施 |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for i, s in enumerate(scenarios[:8], 1):
            lines.append(
                f"| {i} | {s['scenario']} | {s['probability']} | {s['impact']} "
                f"| {s['trigger']} | {s['mitigation']} |"
            )
        lines.append("")

        high_impact = [s for s in scenarios if s["impact"] == "高"]
        if high_impact:
            lines.append("### 高影响场景应对预案\n")
            for s in high_impact[:3]:
                lines.append(f"**场景**: {s['scenario']}")
                lines.append(f"- 触发条件: {s['trigger']}")
                lines.append(f"- 应对措施: {s['mitigation']}")
                lines.append("")

        return "\n".join(lines)

    def generate_resource_allocation(self) -> str:
        lines = [
            "## 资源分配建议\n",
            "基于战略优先级和诊断发现，提出资金、人才和时间三个维度的资源配置建议。\n",
        ]

        allocations = getattr(self, "_resource_allocations", [])

        if not allocations:
            high_recs = sorted(
                [r for r in self._recommendations if r.priority == "高"],
                key=lambda r: {"短期": 0, "中期": 1, "长期": 2}.get(r.timeframe, 1),
            )
            for r in high_recs[:3]:
                for rtype in ("资金", "人才", "时间"):
                    allocations.append({
                        "type": rtype, "area": r.title,
                        "current_pct": 0.0, "recommended_pct": 0.0,
                        "rationale": f"支撑「{r.title}」战略落地",
                    })

        if not allocations:
            lines.append("*暂无足够数据生成资源分配建议，请先添加战略建议*\n")
            return "\n".join(lines)

        for rtype in ("资金", "人才", "时间"):
            type_items = [a for a in allocations if a["type"] == rtype]
            if not type_items:
                continue
            lines.append(f"### {rtype}配置\n")
            lines.append(f"| 投入领域 | 当前占比 | 建议占比 | 调整理由 |")
            lines.append(f"| --- | --- | --- | --- |")
            for a in type_items:
                cur = f"{a['current_pct']:.0f}%" if a["current_pct"] > 0 else "待评估"
                rec = f"{a['recommended_pct']:.0f}%" if a["recommended_pct"] > 0 else "待评估"
                lines.append(f"| {a['area']} | {cur} | {rec} | {a['rationale']} |")
            lines.append("")

        lines.append("### 资源配置原则\n")
        lines.append("1. 优先保障高优先级短期行动的资源需求")
        lines.append("2. 为中期战略方向预留不低于20%的探索性资源")
        lines.append("3. 人才配置应先于资金配置，关键岗位到位后再追加资金")
        lines.append("4. 建立季度资源复盘机制，根据执行效果动态调整")
        lines.append("")

        return "\n".join(lines)

    def render_markdown(self) -> str:
        def get_section(key: str) -> str:
            if key in self._sections:
                return self._sections[key].render()
            return f"*{key}分析待完成*"

        ceo_parts: List[str] = []
        ceo_parts.append(self.generate_ceo_executive_summary())
        ceo_parts.append(self.generate_failure_scenarios())
        ceo_parts.append(self.generate_resource_allocation())
        ceo_section = "\n".join(ceo_parts)

        return FULL_REPORT_TEMPLATE.format(
            company=self._company, industry=self._industry,
            date=self._date, scope=self._scope,
            executive_summary=self._executive_summary or "*执行摘要待撰写*",
            macro_analysis=get_section("宏观环境分析"),
            industry_analysis=get_section("行业竞争格局"),
            company_overview=self._company_overview or "*企业概况待补充*",
            strategy_analysis=get_section("企业战略与能力"),
            consumer_insight=get_section("消费者洞察"),
            brand_diagnosis=get_section("品牌与价值体系"),
            loyalty_analysis=get_section("客户满意度与忠诚度"),
            comprehensive_diagnosis=self._render_diagnosis(),
            strategic_recommendations=self._render_recommendations(),
            ceo_decision_section=ceo_section,
        )

    def render_json(self) -> str:
        data = {
            "company": self._company, "industry": self._industry,
            "date": self._date, "scope": self._scope,
            "executive_summary": self._executive_summary,
            "sections": {k: v.render() for k, v in self._sections.items()},
            "findings": [
                {"category": f.category, "finding": f.finding,
                 "severity": f.severity, "evidence": f.evidence,
                 "recommendation": f.recommendation}
                for f in self._findings
            ],
            "recommendations": [
                {"title": r.title, "description": r.description,
                 "timeframe": r.timeframe, "priority": r.priority,
                 "expected_impact": r.expected_impact, "actions": r.actions}
                for r in self._recommendations
            ],
        }
        return format_as_json(data)

    def get_knowledge(self, topic: str) -> str:
        return load_knowledge(topic)

    def search(self, keyword: str) -> list:
        return search_knowledge(keyword)
