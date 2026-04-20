"""
Demo: 用户注册信息标准化处理器
场景：用户提交的原始数据格式不规范，需要清洗后存入数据库。
演示：字符串方法、f-string、数字运算、类型转换、None 判断。
"""

# ---- 原始用户数据（模拟表单提交，格式杂乱）----
raw_name = "  alice SMITH  "
raw_email = "  Alice.Smith@Gmail.Com  "
raw_age = "28"
raw_phone = "138-0013-8000"
raw_website = "https://alice.dev"
raw_balance = "1_500.75"
discount_rate = None

# ---- 1. 字符串清洗 ----
name = raw_name.strip().title()          # "Alice Smith"
email = raw_email.strip().lower()        # "alice.smith@gmail.com"
phone = raw_phone.replace("-", "")       # "13800138000"
website = raw_website.removeprefix("https://")  # "alice.dev"（Python 3.9+）

# ---- 2. 类型转换 ----
age = int(raw_age)                       # 28
balance = float(raw_balance.replace("_", ""))  # 1500.75

# ---- 3. 数字运算 ----
MEMBERSHIP_FEE = 99                      # 常量：全大写约定
tax_rate = 0.08
balance_after_fee = balance - MEMBERSHIP_FEE
tax = round(balance_after_fee * tax_rate, 2)
years_to_senior = 60 - age              # 普通减法
account_level = balance // 1_000        # 整除：1（千元为单位的等级）
bonus_points = int(balance) ** 2 % 997  # 幂运算 + 取余（模拟积分计算）

# ---- 4. None 判断 ----
if discount_rate is None:
    discount_rate = 0.0

# ---- 5. f-string 输出（嵌入表达式）----
print("=" * 50)
print("用户信息标准化结果")
print("=" * 50)

print(f"姓名:     {name}")
print(f"邮箱:     {email}")
print(f"手机:     {phone[:3]}-{phone[3:7]}-{phone[7:]}")   # 切片格式化
print(f"网站:     {website}")
print(f"年龄:     {age} 岁（距离高级会员还有 {years_to_senior} 年）")
print(f"余额:     ¥{balance:,.2f}")                         # 千分位 + 2位小数
print(f"会费后:   ¥{balance_after_fee:,.2f}")
print(f"税费:     ¥{tax:,.2f}（税率 {tax_rate:.0%}）")      # 百分比格式
print(f"账户等级: {'白金' if account_level >= 10 else '黄金' if account_level >= 5 else '普通'}")
print(f"积分:     {bonus_points}")
print(f"折扣率:   {discount_rate:.0%}")

# ---- 6. 多行字符串（三引号）----
summary = f"""
--- 用户摘要 ---
{name.upper()} | {email} | 余额 ¥{balance:,.2f}
"""
print(summary)

# ---- 7. 整数任意精度演示 ----
huge_number = 2 ** 64
print(f"2^64 = {huge_number:,}")        # Python 整数不会溢出
