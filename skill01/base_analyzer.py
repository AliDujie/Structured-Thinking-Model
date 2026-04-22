"""分析器抽象基类，统一六大模块的公共接口。"""

from abc import ABC, abstractmethod
from .utils import load_knowledge


class BaseAnalyzer(ABC):
    """所有分析模块的基类，定义统一接口契约。"""

    def __init__(self, company: str, industry: str, knowledge_topic: str = ""):
        self._company = company
        self._industry = industry
        self._knowledge_topic = knowledge_topic

    @property
    def company(self) -> str:
        return self._company

    @property
    def industry(self) -> str:
        return self._industry

    @abstractmethod
    def render_markdown(self) -> str:
        """输出 Markdown 格式的分析报告。"""

    @abstractmethod
    def render_json(self) -> str:
        """输出 JSON 格式的分析数据。"""

    def get_knowledge(self) -> str:
        """加载当前模块对应的知识库文档。"""
        if not self._knowledge_topic:
            return ""
        return load_knowledge(self._knowledge_topic)
