"""企业全维度调研工具包 — 像咨询公司资深总监一样研究一家公司。"""

from .config import AnalysisConfig, RESEARCH_MODULES, RESEARCH_MODULE_LABELS
from .utils import load_knowledge, load_all_knowledge, search_knowledge
from .macro_analyzer import MacroAnalyzer, PESTFactor, PESTAnalysis
from .industry_analyzer import IndustryAnalyzer, ForceDriver, CompetitorProfile, KSF
from .strategy_analyzer import (
    StrategyAnalyzer, SWOTItem, SWOTStrategy, BusinessUnit,
    GEFactor, ValueChainActivity, SevenSElement,
)
from .consumer_analyzer import (
    ConsumerAnalyzer, ValueElementScore, Segment, Positioning, MarketingMixItem,
)
from .loyalty_analyzer import (
    LoyaltyAnalyzer, BrandRanking, SatisfactionDriver,
    LoyaltySegment, CompetitiveLoss, ICEAssessment,
)
from .brand_analyzer import (
    BrandAnalyzer, BrandAwareness, BrandAssociation,
    BrandImageDimension, CompetitorBrand, DifferentiationStrategy,
)
from .report_generator import (
    ReportGenerator, ReportSection, StrategicRecommendation, DiagnosticFinding,
)
from .templates import INTERVIEW_QUESTIONS, INNOVATION_CHECKLIST


class CompanyResearchSkill:
    """统一入口类，封装全部研究执行能力。"""

    def __init__(self, company: str, industry: str):
        self._company = company
        self._industry = industry
        self._config = AnalysisConfig(company_name=company, industry=industry)
        self._macro = MacroAnalyzer(company, industry)
        self._industry_a = IndustryAnalyzer(company, industry)
        self._strategy = StrategyAnalyzer(company, industry)
        self._consumer = ConsumerAnalyzer(company, industry)
        self._loyalty = LoyaltyAnalyzer(company, industry)
        self._brand = BrandAnalyzer(company, industry)
        self._report = ReportGenerator(company, industry)

    @property
    def config(self) -> AnalysisConfig:
        return self._config

    @property
    def macro(self) -> MacroAnalyzer:
        return self._macro

    @property
    def industry(self) -> IndustryAnalyzer:
        return self._industry_a

    @property
    def strategy(self) -> StrategyAnalyzer:
        return self._strategy

    @property
    def consumer(self) -> ConsumerAnalyzer:
        return self._consumer

    @property
    def loyalty(self) -> LoyaltyAnalyzer:
        return self._loyalty

    @property
    def brand(self) -> BrandAnalyzer:
        return self._brand

    @property
    def report(self) -> ReportGenerator:
        return self._report

    def search_knowledge(self, keyword: str, topics=None):
        return search_knowledge(keyword, topics)

    def load_knowledge(self, topic: str) -> str:
        return load_knowledge(topic)

    def load_all_knowledge(self):
        return load_all_knowledge()

    def get_interview_questions(self, module: str = ""):
        if module:
            return INTERVIEW_QUESTIONS.get(module, [])
        return INTERVIEW_QUESTIONS

    def get_innovation_checklist(self):
        return INNOVATION_CHECKLIST

    def generate_full_report(self) -> str:
        modules = {
            "宏观环境分析": self._macro,
            "行业竞争格局": self._industry_a,
            "企业战略与能力": self._strategy,
            "消费者洞察": self._consumer,
            "客户满意度与忠诚度": self._loyalty,
            "品牌与价值体系": self._brand,
        }
        for label, analyzer in modules.items():
            output = analyzer.render_markdown()
            if output.strip():
                self._report.add_section(label, output)
        return self._report.render_markdown()

    def validate_config(self):
        return self._config.validate()


__all__ = [
    "CompanyResearchSkill",
    "AnalysisConfig",
    "MacroAnalyzer", "PESTFactor", "PESTAnalysis",
    "IndustryAnalyzer", "ForceDriver", "CompetitorProfile", "KSF",
    "StrategyAnalyzer", "SWOTItem", "SWOTStrategy", "BusinessUnit",
    "GEFactor", "ValueChainActivity", "SevenSElement",
    "ConsumerAnalyzer", "ValueElementScore", "Segment",
    "Positioning", "MarketingMixItem",
    "LoyaltyAnalyzer", "BrandRanking", "SatisfactionDriver",
    "LoyaltySegment", "CompetitiveLoss", "ICEAssessment",
    "BrandAnalyzer", "BrandAwareness", "BrandAssociation",
    "BrandImageDimension", "CompetitorBrand", "DifferentiationStrategy",
    "ReportGenerator", "ReportSection", "StrategicRecommendation",
    "DiagnosticFinding",
    "load_knowledge", "load_all_knowledge", "search_knowledge",
    "INTERVIEW_QUESTIONS", "INNOVATION_CHECKLIST",
    "RESEARCH_MODULES", "RESEARCH_MODULE_LABELS",
]
