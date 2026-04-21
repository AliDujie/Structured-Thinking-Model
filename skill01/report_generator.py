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

    def render_markdown(self) -> str:
        def get_section(key: str) -> str:
            if key in self._sections:
                return self._sections[key].render()
            return f"*{key}分析待完成*"

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
