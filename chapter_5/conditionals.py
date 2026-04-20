"""
Demo: RBAC 权限控制系统
场景：根据用户角色、账号状态、资源类型判断访问权限。
演示：if-elif-else、in/not in、and/or/not、三元表达式、is None、真值测试。
"""

# ---- 用户和资源数据 ----
users = [
    {"id": 1, "name": "Alice", "role": "admin",  "active": True,  "login_count": 150},
    {"id": 2, "name": "Bob",   "role": "editor", "active": True,  "login_count": 30},
    {"id": 3, "name": "Carol", "role": "viewer", "active": False, "login_count": 5},
    {"id": 4, "name": "Dave",  "role": "editor", "active": True,  "login_count": 0},
    {"id": 5, "name": "Eve",   "role": "unknown","active": True,  "login_count": 1},
]

resources = [
    {"name": "系统配置",   "type": "private", "required_role": "admin"},
    {"name": "用户数据",   "type": "private", "required_role": "editor"},
    {"name": "公开文档",   "type": "public",  "required_role": None},
    {"name": "财务报表",   "type": "private", "required_role": "admin"},
]

ROLE_LEVELS = {"admin": 3, "editor": 2, "viewer": 1}


def check_permission(user: dict, resource: dict) -> str:
    """检查用户是否有权限访问资源，返回判断结果说明。"""
    name = user["name"]
    role = user["role"]
    active = user["active"]
    login_count = user["login_count"]
    required_role = resource["required_role"]
    resource_name = resource["name"]
    resource_type = resource["type"]

    # 1. 账号状态检查（短路：inactive 直接拒绝）
    if not active:
        return f"❌ {name} → {resource_name}：账号已停用"

    # 2. 角色有效性检查（in 成员检测）
    if role not in ROLE_LEVELS:
        return f"❌ {name} → {resource_name}：未知角色 '{role}'"

    # 3. 公开资源（required_role 为 None）
    if required_role is None:          # None 判断用 is
        status = "活跃" if login_count > 0 else "新用户"   # 三元表达式
        return f"✅ {name}（{status}）→ {resource_name}：公开资源，直接允许"

    # 4. 私有资源：角色等级检查
    user_level = ROLE_LEVELS[role]
    required_level = ROLE_LEVELS.get(required_role, 0)

    if user_level >= required_level:
        # 链式比较：检查登录次数是否在合理范围
        trust_level = "可信" if 1 <= login_count <= 1000 else "异常"
        return f"✅ {name}（{trust_level}）→ {resource_name}：角色 {role} 满足要求"
    else:
        return f"⛔ {name} → {resource_name}：需要 {required_role} 权限，当前为 {role}"


def get_user_summary(user: dict) -> str:
    """生成用户状态摘要。"""
    role = user["role"]
    active = user["active"]
    login_count = user["login_count"]

    # elif 多分支
    if role == "admin":
        role_label = "管理员"
    elif role == "editor":
        role_label = "编辑"
    elif role == "viewer":
        role_label = "访客"
    else:
        role_label = "未知角色"

    # 布尔运算：and / or / not
    is_trusted = active and login_count >= 10
    needs_review = not active or login_count == 0

    # 真值测试：login_count 为 0 时是 falsy
    activity = f"{login_count} 次登录" if login_count else "从未登录"

    flags = []
    if is_trusted:
        flags.append("受信")
    if needs_review:
        flags.append("待审核")
    flag_str = f"[{', '.join(flags)}]" if flags else ""   # 真值测试空列表

    return f"{user['name']} ({role_label}) - {activity} {flag_str}"


# ---- 主程序 ----
print("=" * 60)
print("RBAC 权限控制系统")
print("=" * 60)

# 用户摘要
print("\n用户列表：")
for user in users:
    print(f"  {get_user_summary(user)}")

# 权限矩阵
print("\n权限检查矩阵：")
print("-" * 60)
for user in users:
    for resource in resources:
        result = check_permission(user, resource)
        print(f"  {result}")
    print()

# 过滤：活跃的 admin 或 editor 用户
print("有效操作用户（活跃的 admin/editor）：")
operators = [
    u["name"] for u in users
    if u["active"] and u["role"] in ("admin", "editor")  # in 检测元组
]
print(f"  {operators if operators else '无'}")  # 真值测试空列表
