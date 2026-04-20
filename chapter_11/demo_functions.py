"""
被测模块：用户数据处理工具
包含有业务逻辑的函数，供 test_demo.py 进行测试。
"""

from typing import Optional


def normalize_name(name: str) -> str:
    """标准化用户名：去除空白、转换为 Title Case。"""
    if not isinstance(name, str):
        raise TypeError(f"name 必须是字符串，得到 {type(name).__name__}")
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name 不能为空字符串")
    return cleaned.title()


def calculate_discount(price: float, discount_rate: float) -> float:
    """计算折扣后价格。discount_rate 范围 0.0 ~ 1.0。"""
    if price < 0:
        raise ValueError(f"价格不能为负数：{price}")
    if not (0.0 <= discount_rate <= 1.0):
        raise ValueError(f"折扣率必须在 0.0 到 1.0 之间：{discount_rate}")
    return round(price * (1 - discount_rate), 2)


def find_user(users: list[dict], user_id: int) -> Optional[dict]:
    """在用户列表中查找指定 ID 的用户，找不到返回 None。"""
    for user in users:
        if user.get("id") == user_id:
            return user
    return None


def filter_active_users(users: list[dict]) -> list[dict]:
    """过滤出所有 active=True 的用户。"""
    return [u for u in users if u.get("active", False)]


def merge_user_data(base: dict, override: dict) -> dict:
    """合并两个用户数据字典，override 覆盖 base 的值。"""
    return {**base, **override}


def is_palindrome(text: str) -> bool:
    """判断字符串是否是回文（忽略大小写和空格）。"""
    cleaned = text.lower().replace(" ", "").replace(",", "").replace(".", "")
    return cleaned == cleaned[::-1]


def parse_age(raw: str) -> int:
    """将年龄字符串转换为整数，无效输入抛出 ValueError。"""
    try:
        age = int(raw.strip())
    except (ValueError, AttributeError):
        raise ValueError(f"无效的年龄值：{raw!r}")
    if age < 0 or age > 150:
        raise ValueError(f"年龄超出合理范围：{age}")
    return age


def summarize_scores(scores: list[int]) -> dict:
    """统计分数列表的摘要信息。"""
    if not scores:
        raise ValueError("分数列表不能为空")
    return {
        "count": len(scores),
        "min": min(scores),
        "max": max(scores),
        "avg": round(sum(scores) / len(scores), 2),
        "passed": sum(1 for s in scores if s >= 60),
    }
