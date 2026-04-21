"""skill01 完整测试套件 — 10个测试用例覆盖全部执行能力。"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from skill01 import (
    CompanyResearchSkill,
    MacroAnalyzer,
    IndustryAnalyzer,
    StrategyAnalyzer,
    ConsumerAnalyzer,
    BrandAnalyzer,
    LoyaltyAnalyzer,
    ReportGenerator,
    load_knowledge,
    search_knowledge,
    INTERVIEW_QUESTIONS,
    INNOVATION_CHECKLIST,
)


def test_company_research_skill_init():
    skill = CompanyResearchSkill("测试公司", "零售行业")
    assert skill.config.company_name == "测试公司"
    assert skill.config.industry == "零售行业"
    assert skill.macro is not None
    assert skill.industry is not None
    assert skill.strategy is not None
    assert skill.consumer is not None
    assert skill.loyalty is not None
    assert skill.brand is not None
    assert skill.report is not None
    errors = skill.validate_config()
    assert isinstance(errors, list)
    assert len(errors) == 1
    assert "competitor_names" in errors[0]
    skill.config.include_competitors = False
    errors2 = skill.validate_config()
    assert len(errors2) == 0
    checklist = skill.get_innovation_checklist()
    assert len(checklist) == 10
    print("✅ test_company_research_skill_init passed")


def test_macro_analysis():
    analyzer = MacroAnalyzer("测试公司", "零售行业", mode="pestel")
    analyzer.add_factor(
        "political", "产业政策", "政府对零售行业的支持",
        score=4.0, weight=0.15, trend="上升", impact="高",
    )
    analyzer.add_factor(
        "economic", "GDP增长", "宏观经济增速放缓",
        score=3.0, weight=0.12, trend="下降", impact="中等",
    )
    analyzer.add_factor(
        "social", "消费升级", "消费者品质意识提升",
        score=4.5, weight=0.10, trend="上升", impact="高",
    )
    analyzer.add_factor(
        "technological", "数字化转型", "线上线下融合加速",
        score=4.0, weight=0.13, trend="上升", impact="高",
    )
    analyzer.add_factor(
        "environmental", "环保要求", "绿色包装法规趋严",
        score=2.5, weight=0.08, trend="上升", impact="中等",
    )
    analyzer.add_factor(
        "legal", "数据保护", "个人信息保护法实施",
        score=3.0, weight=0.07, trend="稳定", impact="中等",
    )
    md = analyzer.render_markdown()
    assert "PESTEL分析" in md
    assert "测试公司" in md
    assert "产业政策" in md
    assert "EFE加权总分" in md
    json_out = analyzer.render_json()
    assert '"company": "测试公司"' in json_out
    assert '"efe_score"' in json_out
    findings = analyzer.get_key_findings()
    assert isinstance(findings, list)
    assert len(findings) > 0
    implications = analyzer.get_implications()
    assert isinstance(implications, list)
    assert len(implications) > 0
    knowledge = analyzer.get_knowledge()
    assert "PEST" in knowledge
    print("✅ test_macro_analysis passed")


def test_industry_analysis():
    analyzer = IndustryAnalyzer("测试公司", "零售行业")
    analyzer.set_lifecycle_stage("maturity")
    analyzer.add_force_driver(
        "rivalry", "竞争者数量", "行业内主要竞争者超过10家",
        score=4.0, weight=0.3,
    )
    analyzer.add_force_driver(
        "new_entrants", "资本壁垒", "进入需要大量资本投入",
        score=2.0, weight=0.25,
    )
    analyzer.add_force_driver(
        "substitutes", "电商替代", "线上渠道对实体零售的替代",
        score=4.5, weight=0.2,
    )
    analyzer.add_force_driver(
        "buyer_power", "消费者选择", "消费者转换成本低",
        score=3.5, weight=0.15,
    )
    analyzer.add_force_driver(
        "supplier_power", "供应商集中度", "供应商较为分散",
        score=2.0, weight=0.1,
    )
    analyzer.add_competitor(
        "竞品A", market_share=25.0,
        strengths=["品牌知名度高", "渠道覆盖广"],
        weaknesses=["数字化能力弱"],
        strategy="成本领先",
    )
    analyzer.add_ksf(
        "品牌知名度", weight=0.2, company_score=4.0,
        competitor_scores={"竞品A": 4.5},
    )
    analyzer.add_ksf(
        "供应链效率", weight=0.25, company_score=3.5,
        competitor_scores={"竞品A": 4.0},
    )
    md = analyzer.render_markdown()
    assert "五力分析" in md
    assert "竞争者数量" in md
    assert "成熟期" in md
    json_out = analyzer.render_json()
    assert '"lifecycle_stage": "maturity"' in json_out
    insights = analyzer.get_lifecycle_insights()
    assert "成熟期" in insights[0]
    assessment = analyzer.get_attractiveness_assessment()
    assert isinstance(assessment, str)
    assert len(assessment) > 0
    print("✅ test_industry_analysis passed")


def test_strategy_analysis():
    analyzer = StrategyAnalyzer("测试公司", "零售行业")
    analyzer.add_swot_item("strengths", "品牌知名度高", importance=5)
    analyzer.add_swot_item("strengths", "供应链成熟", importance=4)
    analyzer.add_swot_item("weaknesses", "线上渠道薄弱", importance=4)
    analyzer.add_swot_item("opportunities", "下沉市场扩张", importance=5)
    analyzer.add_swot_item("threats", "电商平台竞争", importance=5)
    analyzer.add_swot_strategy(
        "SO", "利用品牌优势拓展下沉市场",
        actions=["开设社区店", "发展加盟模式"],
    )
    analyzer.add_swot_strategy(
        "WO", "借助下沉市场机会补强线上能力",
        actions=["建设小程序商城", "社区团购"],
    )
    analyzer.add_business_unit("核心零售", market_growth_rate=5.0, relative_market_share=1.5)
    analyzer.add_business_unit("新零售", market_growth_rate=25.0, relative_market_share=0.3)
    analyzer.add_ge_factor("市场规模", weight=0.2, score=4.0, category="attractiveness")
    analyzer.add_ge_factor("市场增长率", weight=0.2, score=3.0, category="attractiveness")
    analyzer.add_ge_factor("市场份额", weight=0.25, score=4.0, category="competitiveness")
    analyzer.add_ge_factor("品牌知名度", weight=0.2, score=4.5, category="competitiveness")
    analyzer.add_value_chain_activity(
        "市场营销", "primary", performance=4.0, competitor_benchmark=3.5,
        description="品牌营销能力强",
    )
    analyzer.add_value_chain_activity(
        "技术开发", "support", performance=2.5, competitor_benchmark=4.0,
        description="数字化技术投入不足",
    )
    analyzer.add_seven_s("strategy", "聚焦高端零售", score=4.0)
    analyzer.add_seven_s("structure", "区域化组织架构", score=3.5)
    analyzer.add_seven_s("shared_values", "客户至上", score=4.5)
    analyzer.set_ansoff_choice("market_development")
    md = analyzer.render_markdown()
    assert "SWOT分析" in md
    assert "波士顿矩阵" in md
    assert "GE矩阵" in md
    assert "价值链分析" in md
    assert "7S模型" in md
    assert "安索夫" in md
    json_out = analyzer.render_json()
    assert '"strengths"' in json_out
    assert '"ansoff_choice": "market_development"' in json_out
    print("✅ test_strategy_analysis passed")


def test_consumer_analysis():
    analyzer = ConsumerAnalyzer("测试公司", "食品饮料")
    analyzer.add_value_score("质量", score=4.5, competitor_scores={"竞品A": 4.0}, importance=5.0)
    analyzer.add_value_score("感官体验", score=4.0, competitor_scores={"竞品A": 3.5}, importance=4.5)
    analyzer.add_value_score("多样性", score=3.5, importance=4.0)
    analyzer.add_value_score("设计/美学", score=4.2, importance=3.5)
    analyzer.add_value_score("减少焦虑", score=3.0, importance=2.5)
    analyzer.add_segment(
        "年轻白领", size="3000万", growth="15%",
        characteristics=["25-35岁", "一二线城市", "注重品质"],
        needs=["健康", "便捷", "高颜值"], is_target=True,
    )
    analyzer.add_segment(
        "家庭主妇", size="5000万", growth="5%",
        characteristics=["30-50岁", "家庭消费决策者"],
        needs=["性价比", "安全"], is_target=False,
    )
    analyzer.set_positioning("年轻白领", "高品质健康生活方式", "天然有机原料", "十年有机认证")
    analyzer.add_marketing_mix("产品", "产品线丰富，品质稳定", score=4.0, recommendations=["推出小包装"])
    analyzer.add_marketing_mix("价格", "中高端定价", score=3.5, recommendations=["推出入门款"])
    high = analyzer.get_high_performing_elements(threshold=4.0)
    assert len(high) >= 2
    nps = analyzer.get_nps_prediction()
    assert "NPS" in nps
    benchmark = analyzer.get_industry_benchmark()
    assert "质量" in benchmark
    md = analyzer.render_markdown()
    assert "消费者洞察" in md or "价值要素" in md
    assert "年轻白领" in md
    json_out = analyzer.render_json()
    assert '"high_performing_count"' in json_out
    print("✅ test_consumer_analysis passed")


def test_brand_analysis():
    analyzer = BrandAnalyzer("测试公司", "零售行业")
    analyzer.set_awareness(top_of_mind=25.0, aided_awareness=75.0, recognition=90.0, assessment="知名度较高")
    analyzer.add_association("高品质", strength=4.5, uniqueness=3.5, favorability=4.0)
    analyzer.add_association("时尚", strength=3.0, uniqueness=4.0, favorability=4.5)
    analyzer.add_image_dimension(
        "产品质量", score=4.5, competitor_scores={"竞品A": 4.0, "竞品B": 3.5},
        description="质量口碑良好",
    )
    analyzer.add_image_dimension(
        "创新能力", score=3.0, competitor_scores={"竞品A": 4.5},
        description="创新投入不足",
    )
    analyzer.set_loyalty(level=3, distribution={1: 10, 2: 25, 3: 35, 4: 20, 5: 10})
    analyzer.add_competitor_brand(
        "竞品A", awareness=30.0, image_score=4.0, loyalty_level=4,
        key_strengths=["创新能力强", "数字化领先"],
        key_weaknesses=["价格偏高"], value_proposition="科技驱动的零售体验",
    )
    analyzer.add_differentiation(
        "客户体验差异化", "打造全渠道无缝购物体验",
        feasibility=4.0, impact=4.5, actions=["统一会员体系", "线上线下价格同步"],
    )
    analyzer.add_differentiation(
        "服务差异化", "提供个性化导购服务",
        feasibility=3.5, impact=3.0, actions=["培训导购团队", "引入AI推荐"],
    )
    md = analyzer.render_markdown()
    assert "品牌价值分析" in md
    assert "25.0%" in md
    assert "竞品A" in md
    assert "客户体验差异化" in md
    json_out = analyzer.render_json()
    assert '"top_of_mind": 25.0' in json_out
    print("✅ test_brand_analysis passed")


def test_loyalty_analysis():
    analyzer = LoyaltyAnalyzer("测试公司", "零售行业")
    analyzer.add_brand_ranking("测试公司", satisfaction_score=4.2, rank=1, brand_count=5)
    analyzer.add_brand_ranking("竞品A", satisfaction_score=4.0, rank=2, brand_count=5)
    analyzer.add_brand_ranking("竞品B", satisfaction_score=3.8, rank=3, brand_count=5)
    ws = analyzer.get_company_wallet_share()
    assert ws > 0
    assert ws < 1.0
    rk = analyzer.get_company_rank()
    assert rk == 1
    analyzer.add_satisfaction_driver("服务响应速度", importance=4.5, performance=3.0, is_dissatisfaction=True)
    analyzer.add_satisfaction_driver("产品质量", importance=5.0, performance=4.5, is_delight=True)
    analyzer.add_satisfaction_driver("价格合理性", importance=4.0, performance=3.5)
    priority = analyzer.get_priority_drivers(top_n=3)
    assert len(priority) == 3
    assert priority[0].name == "服务响应速度"
    analyzer.add_loyalty_segment("core", count=5000, percentage=35.0, strategy="VIP维护计划")
    analyzer.add_loyalty_segment("high_value_at_risk", count=2000, percentage=20.0, strategy="挽留专项")
    analyzer.add_competitive_loss(
        "竞品A", lost_customers=500, lost_revenue=250000.0,
        reasons=["配送速度慢", "促销力度不足"], recovery_cost=50000.0,
    )
    analyzer.add_ice_assessment(
        "接触点", current_score=3.5, target_score=5.0,
        gap_description="线上接触点体验不一致",
        improvement_actions=["统一UI设计", "优化加载速度"],
    )
    md = analyzer.render_markdown()
    assert "钱包分配法则" in md
    assert "测试公司" in md
    assert "服务响应速度" in md
    json_out = analyzer.render_json()
    assert '"company_wallet_share"' in json_out
    assert '"competitive_losses"' in json_out
    print("✅ test_loyalty_analysis passed")


def test_full_report_generation():
    skill = CompanyResearchSkill("测试公司", "零售行业")
    skill.macro.add_factor("political", "产业政策", "支持零售业发展", score=4.0, weight=0.15)
    skill.macro.add_factor("economic", "消费增长", "消费市场持续扩大", score=3.5, weight=0.12)
    skill.industry.set_lifecycle_stage("maturity")
    skill.industry.add_force_driver("rivalry", "竞争强度", "竞争激烈", score=4.0, weight=0.3)
    skill.strategy.add_swot_item("strengths", "品牌知名度高", importance=5)
    skill.strategy.add_swot_item("weaknesses", "数字化能力不足", importance=4)
    skill.consumer.add_value_score("质量", score=4.5, importance=5.0)
    skill.loyalty.add_brand_ranking("测试公司", satisfaction_score=4.2, rank=1, brand_count=3)
    skill.brand.set_awareness(top_of_mind=25.0, aided_awareness=75.0, recognition=90.0)
    skill.report.set_executive_summary("本报告对测试公司进行了全维度研究，发现其品牌优势明显但数字化能力不足。")
    skill.report.set_company_overview("测试公司成立于2000年，是国内领先的零售企业。")
    skill.report.add_finding("战略", "数字化转型滞后", severity="高", evidence="线上营收占比仅5%")
    skill.report.add_finding("品牌", "品牌老化风险", severity="中", evidence="年轻消费者认知度下降")
    skill.report.add_recommendation(
        "加速数字化转型", "投资线上渠道和数字化基础设施",
        timeframe="短期", priority="高",
        actions=["建设自有电商平台", "部署智能供应链系统"],
    )
    skill.report.add_recommendation(
        "品牌年轻化", "重塑品牌形象吸引年轻消费者",
        timeframe="中期", priority="中",
        actions=["联名合作", "社交媒体营销"],
    )
    report = skill.generate_full_report()
    assert "测试公司 — 企业全维度研究报告" in report
    assert "执行摘要" in report
    assert "宏观环境" in report
    assert "战略分析" in report or "SWOT" in report
    assert "消费者洞察" in report or "价值要素" in report
    assert "品牌" in report
    assert "数字化转型滞后" in report
    assert "加速数字化转型" in report
    assert len(report) > 1000
    json_out = skill.report.render_json()
    assert '"company": "测试公司"' in json_out
    print("✅ test_full_report_generation passed")


def test_knowledge_search():
    results = search_knowledge("五力模型")
    assert isinstance(results, list)
    assert len(results) > 0
    found_industry = False
    for r in results:
        assert "topic" in r
        assert "section" in r
        assert "content" in r
        if r["topic"] == "industry_competition":
            found_industry = True
    assert found_industry, "应在industry_competition中找到五力模型相关内容"
    results2 = search_knowledge("SWOT", topics=["strategy_capability"])
    assert len(results2) > 0
    assert all(r["topic"] == "strategy_capability" for r in results2)
    knowledge = load_knowledge("macro_environment")
    assert "PEST" in knowledge
    assert len(knowledge) > 100
    knowledge2 = load_knowledge("consumer_insight")
    assert "价值要素" in knowledge2
    print("✅ test_knowledge_search passed")


def test_interview_questions():
    skill = CompanyResearchSkill("测试公司", "零售行业")
    all_questions = skill.get_interview_questions()
    assert isinstance(all_questions, dict)
    expected_modules = [
        "macro_environment", "industry_competition", "strategy_capability",
        "consumer_insight", "loyalty_satisfaction", "brand_value",
    ]
    for module in expected_modules:
        assert module in all_questions, f"缺少模块: {module}"
        questions = all_questions[module]
        assert isinstance(questions, list)
        assert len(questions) >= 3, f"模块{module}问题数不足"
        for q in questions:
            assert isinstance(q, str)
            assert len(q) > 5
    macro_qs = skill.get_interview_questions("macro_environment")
    assert isinstance(macro_qs, list)
    assert len(macro_qs) >= 3
    empty_qs = skill.get_interview_questions("nonexistent_module")
    assert empty_qs == []
    checklist = skill.get_innovation_checklist()
    assert isinstance(checklist, list)
    assert len(checklist) == 10
    for item in checklist:
        assert isinstance(item, str)
        assert "？" in item
    print("✅ test_interview_questions passed")


def run_all_tests():
    tests = [
        test_company_research_skill_init,
        test_macro_analysis,
        test_industry_analysis,
        test_strategy_analysis,
        test_consumer_analysis,
        test_brand_analysis,
        test_loyalty_analysis,
        test_full_report_generation,
        test_knowledge_search,
        test_interview_questions,
    ]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} FAILED: {e}")
    print(f"\n{'='*50}")
    print(f"测试结果: {passed} 通过, {failed} 失败, 共 {len(tests)} 个")
    print(f"{'='*50}")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
