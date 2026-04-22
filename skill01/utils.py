import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import KNOWLEDGE_FILES, REFERENCES_DIR


def load_knowledge(topic: str) -> str:
    if topic not in KNOWLEDGE_FILES:
        raise ValueError(f"未知知识库主题: {topic}，可选: {list(KNOWLEDGE_FILES.keys())}")
    file_path = REFERENCES_DIR / KNOWLEDGE_FILES[topic]
    if not file_path.exists():
        raise FileNotFoundError(f"知识库文件不存在: {file_path}")
    return file_path.read_text(encoding="utf-8")


def load_all_knowledge() -> Dict[str, str]:
    result: Dict[str, str] = {}
    for topic in KNOWLEDGE_FILES:
        try:
            result[topic] = load_knowledge(topic)
        except FileNotFoundError:
            result[topic] = ""
    return result


def search_knowledge(keyword: str, topics: Optional[List[str]] = None) -> List[Dict[str, str]]:
    if topics is None:
        topics = list(KNOWLEDGE_FILES.keys())
    results: List[Dict[str, str]] = []
    for topic in topics:
        try:
            content = load_knowledge(topic)
        except (ValueError, FileNotFoundError):
            continue
        sections = extract_sections(content)
        for title, body in sections:
            if keyword.lower() in title.lower() or keyword.lower() in body.lower():
                results.append({
                    "topic": topic,
                    "section": title,
                    "content": body.strip(),
                })
    return results


def extract_sections(content: str, level: int = 2) -> List[Tuple[str, str]]:
    pattern = re.compile(rf"^({'#' * level})\s+(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(content))
    sections: List[Tuple[str, str]] = []
    for i, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end]
        sections.append((title, body))
    return sections


def format_as_markdown(title: str, sections: Dict[str, str]) -> str:
    lines = [f"# {title}", ""]
    for heading, body in sections.items():
        lines.append(f"## {heading}")
        lines.append("")
        lines.append(body.strip())
        lines.append("")
    return "\n".join(lines)


def format_as_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def format_list(items: List[str], numbered: bool = False) -> str:
    lines: List[str] = []
    for i, item in enumerate(items, 1):
        prefix = f"{i}." if numbered else "-"
        lines.append(f"{prefix} {item}")
    return "\n".join(lines)


def format_table(headers: List[str], rows: List[List[str]]) -> str:
    lines: List[str] = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        lines.append("| " + " | ".join(str(c) for c in padded) + " |")
    return "\n".join(lines)


def format_score_bar(score: float, max_score: int = 5, bar_length: int = 20) -> str:
    if max_score <= 0:
        return f"[{'░' * bar_length}] {score:.1f}/0"
    clamped = max(0.0, min(float(score), float(max_score)))
    filled = int((clamped / max_score) * bar_length)
    empty = bar_length - filled
    return f"[{'█' * filled}{'░' * empty}] {score:.1f}/{max_score}"


def calculate_weighted_total(factors: List[Dict], weight_key: str = "weight", score_key: str = "score") -> float:
    return sum(f.get(weight_key, 0.0) * f.get(score_key, 0.0) for f in factors)


def normalize_weights(factors: List[Dict], weight_key: str = "weight") -> List[Dict]:
    total = sum(f.get(weight_key, 0.0) for f in factors)
    if total == 0:
        return factors
    for f in factors:
        f[weight_key] = f.get(weight_key, 0.0) / total
    return factors


def score_to_level(score: float, max_score: int = 5) -> str:
    ratio = score / max_score
    if ratio >= 0.8:
        return "非常强"
    if ratio >= 0.6:
        return "较强"
    if ratio >= 0.4:
        return "中等"
    if ratio >= 0.2:
        return "较弱"
    return "非常弱"


def validate_score(score: float, min_val: float = 1.0, max_val: float = 5.0) -> float:
    if score < min_val or score > max_val:
        raise ValueError(f"评分 {score} 超出有效范围 [{min_val}, {max_val}]")
    return score


def validate_weight(weight: float) -> float:
    if weight < 0:
        return 0.0
    if weight > 1.0:
        return 1.0
    return weight


def wallet_share_formula(rank: int, brand_count: int) -> float:
    if brand_count <= 0 or rank <= 0:
        return 0.0
    if rank > brand_count:
        return 0.0
    return (1 - rank / (brand_count + 1)) * (2 / brand_count)
