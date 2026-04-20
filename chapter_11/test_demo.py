"""
pytest 测试文件
覆盖：正常用例、边界值、异常、参数化、fixture、mock。
运行：pytest chapter_11/test_demo.py -v
"""

import pytest
from unittest.mock import patch, MagicMock

from demo_functions import (
    normalize_name,
    calculate_discount,
    find_user,
    filter_active_users,
    merge_user_data,
    is_palindrome,
    parse_age,
    summarize_scores,
)


# ==================== Fixture ====================

@pytest.fixture
def sample_users():
    """测试用用户列表，每个测试函数调用前重新创建。"""
    return [
        {"id": 1, "name": "Alice", "role": "admin",  "active": True},
        {"id": 2, "name": "Bob",   "role": "editor", "active": True},
        {"id": 3, "name": "Carol", "role": "viewer", "active": False},
        {"id": 4, "name": "Dave",  "role": "editor", "active": False},
    ]


@pytest.fixture
def base_user():
    return {"id": 1, "name": "Alice", "role": "viewer", "active": True}


# ==================== normalize_name ====================

class TestNormalizeName:

    def test_basic(self):
        assert normalize_name("alice") == "Alice"

    def test_strips_whitespace(self):
        assert normalize_name("  bob  ") == "Bob"

    def test_title_case_multiword(self):
        assert normalize_name("john doe") == "John Doe"

    def test_already_normalized(self):
        assert normalize_name("Alice Smith") == "Alice Smith"

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError, match="不能为空"):
            normalize_name("")

    def test_raises_on_whitespace_only(self):
        with pytest.raises(ValueError):
            normalize_name("   ")

    def test_raises_on_non_string(self):
        with pytest.raises(TypeError, match="必须是字符串"):
            normalize_name(123)

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            normalize_name(None)


# ==================== calculate_discount ====================

@pytest.mark.parametrize("price,rate,expected", [
    (100.0, 0.0,  100.0),    # 无折扣
    (100.0, 1.0,    0.0),    # 全额折扣
    (100.0, 0.2,   80.0),    # 八折
    (99.9,  0.1,   89.91),   # 精度测试
    (0.0,   0.5,    0.0),    # 零价格
])
def test_calculate_discount(price, rate, expected):
    assert calculate_discount(price, rate) == expected


def test_calculate_discount_negative_price():
    with pytest.raises(ValueError, match="不能为负数"):
        calculate_discount(-10.0, 0.5)


def test_calculate_discount_invalid_rate_high():
    with pytest.raises(ValueError, match="折扣率"):
        calculate_discount(100.0, 1.5)


def test_calculate_discount_invalid_rate_low():
    with pytest.raises(ValueError):
        calculate_discount(100.0, -0.1)


# ==================== find_user ====================

def test_find_user_found(sample_users):
    user = find_user(sample_users, user_id=1)
    assert user is not None
    assert user["name"] == "Alice"


def test_find_user_not_found(sample_users):
    result = find_user(sample_users, user_id=999)
    assert result is None


def test_find_user_empty_list():
    result = find_user([], user_id=1)
    assert result is None


# ==================== filter_active_users ====================

def test_filter_active_users_returns_only_active(sample_users):
    active = filter_active_users(sample_users)
    assert len(active) == 2
    assert all(u["active"] for u in active)


def test_filter_active_users_names(sample_users):
    active = filter_active_users(sample_users)
    names = {u["name"] for u in active}
    assert names == {"Alice", "Bob"}


def test_filter_active_users_empty():
    assert filter_active_users([]) == []


def test_filter_active_users_all_inactive():
    users = [{"id": 1, "active": False}, {"id": 2, "active": False}]
    assert filter_active_users(users) == []


# ==================== merge_user_data ====================

def test_merge_user_data_override(base_user):
    result = merge_user_data(base_user, {"role": "admin", "department": "eng"})
    assert result["role"] == "admin"           # 被覆盖
    assert result["name"] == "Alice"           # 保留
    assert result["department"] == "eng"       # 新增


def test_merge_user_data_does_not_modify_base(base_user):
    original_role = base_user["role"]
    merge_user_data(base_user, {"role": "admin"})
    assert base_user["role"] == original_role  # 原字典不受影响


def test_merge_user_data_empty_override(base_user):
    result = merge_user_data(base_user, {})
    assert result == base_user


# ==================== is_palindrome ====================

@pytest.mark.parametrize("text,expected", [
    ("racecar",                           True),
    ("hello",                             False),
    ("A man a plan a canal Panama",        True),
    ("",                                  True),
    ("Was it a car or a cat I saw",       True),
    ("No lemon, no melon",                True),
    ("Python",                            False),
])
def test_is_palindrome(text, expected):
    assert is_palindrome(text) == expected


# ==================== parse_age ====================

@pytest.mark.parametrize("raw,expected", [
    ("25", 25),
    (" 30 ", 30),
    ("0", 0),
    ("150", 150),
])
def test_parse_age_valid(raw, expected):
    assert parse_age(raw) == expected


@pytest.mark.parametrize("raw", ["abc", "", "  ", "12.5", None])
def test_parse_age_invalid_format(raw):
    with pytest.raises((ValueError, AttributeError)):
        parse_age(raw)


@pytest.mark.parametrize("raw", ["-1", "151", "999"])
def test_parse_age_out_of_range(raw):
    with pytest.raises(ValueError, match="超出合理范围"):
        parse_age(raw)


# ==================== summarize_scores ====================

def test_summarize_scores_basic():
    result = summarize_scores([80, 90, 70, 60, 50])
    assert result["count"] == 5
    assert result["min"] == 50
    assert result["max"] == 90
    assert result["avg"] == 70.0
    assert result["passed"] == 4    # >= 60 的有 4 个


def test_summarize_scores_all_fail():
    result = summarize_scores([10, 20, 30])
    assert result["passed"] == 0


def test_summarize_scores_single():
    result = summarize_scores([75])
    assert result["count"] == 1
    assert result["avg"] == 75.0


def test_summarize_scores_empty():
    with pytest.raises(ValueError, match="不能为空"):
        summarize_scores([])


# ==================== Mock 示例 ====================

def get_remote_config(url: str, http_client=None) -> dict:
    """
    从远程 URL 获取配置。
    http_client 是可注入的 HTTP 客户端（依赖注入便于测试）。
    """
    if http_client is None:
        try:
            import requests
            http_client = requests
        except ImportError:
            raise RuntimeError("requests 未安装，请 pip install requests")
    response = http_client.get(url, timeout=5)
    return response.json()


def test_get_remote_config_success():
    """通过依赖注入传入 mock 客户端，无需安装 requests。"""
    mock_client = MagicMock()
    mock_client.get.return_value.json.return_value = {"version": "1.0", "debug": False}

    result = get_remote_config("http://config.example.com/api", http_client=mock_client)

    assert result["version"] == "1.0"
    assert result["debug"] is False
    mock_client.get.assert_called_once_with("http://config.example.com/api", timeout=5)


def test_get_remote_config_network_error():
    """网络异常时抛出 ConnectionError。"""
    mock_client = MagicMock()
    mock_client.get.side_effect = ConnectionError("网络不可达")

    with pytest.raises(ConnectionError):
        get_remote_config("http://config.example.com/api", http_client=mock_client)
