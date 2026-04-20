"""
Demo: 任务调度器
场景：后端任务队列管理系统，模拟任务的添加、排序、过滤、批量处理。
演示：列表增删改、排序、enumerate、切片、列表推导式、元组解包。
"""

from datetime import datetime

# ---- 任务数据结构：(优先级, 任务名, 预计耗时秒) ----
tasks = [
    (3, "发送邮件通知", 5),
    (1, "数据库备份", 120),
    (2, "生成报表", 45),
    (5, "清理临时文件", 10),
    (1, "处理支付订单", 30),
    (4, "更新用户积分", 8),
    (2, "同步外部数据", 60),
]

print("=" * 55)
print("任务调度器")
print("=" * 55)

# ---- 1. 查看队列状态 ----
print(f"\n当前队列共 {len(tasks)} 个任务")
print(f"最后一个任务：{tasks[-1][1]}")     # 负数索引访问最后一个元素

# ---- 2. 添加紧急任务 ----
tasks.append((1, "修复生产环境 BUG", 0))   # 最高优先级任务
tasks.insert(0, (1, "服务健康检查", 2))    # 插入到队首

# ---- 3. 按优先级排序（优先级数字越小越高）----
tasks.sort(key=lambda t: t[0])
print(f"\n按优先级排序后，队列共 {len(tasks)} 个任务：")
for i, task in enumerate(tasks, start=1):
    priority, name, duration = task          # 元组解包
    bar = "★" * priority
    print(f"  {i:2d}. [{bar:<5}] {name} ({duration}s)")

# ---- 4. 列表推导式：过滤高优先级任务（优先级 <= 2）----
urgent_tasks = [(p, name, d) for p, name, d in tasks if p <= 2]
print(f"\n紧急任务（优先级 ≤ 2）共 {len(urgent_tasks)} 个：")
for _, name, duration in urgent_tasks:       # _ 忽略不需要的值
    print(f"  - {name} ({duration}s)")

# ---- 5. 切片：查看"今日前 3 个任务" ----
today_batch = tasks[:3]
print(f"\n今日前 3 个任务：")
for priority, name, duration in today_batch:
    print(f"  {name}")

# ---- 6. 切片：查看最后 2 个任务（低优先级积压）----
backlog = tasks[-2:]
print(f"\n积压任务（最低优先级）：")
for _, name, _ in backlog:
    print(f"  {name}")

# ---- 7. 统计数据 ----
durations = [d for _, _, d in tasks]        # 提取所有耗时
total_time = sum(durations)
min_time = min(durations)
max_time = max(durations)
avg_time = total_time / len(durations)

print(f"\n任务耗时统计：")
print(f"  总计：{total_time}s")
print(f"  最短：{min_time}s  最长：{max_time}s  平均：{avg_time:.1f}s")

# ---- 8. 移除已完成任务（remove 只删第一个匹配）----
task_names = [name for _, name, _ in tasks]
task_names.remove("服务健康检查")
print(f"\n完成'服务健康检查'后，剩余 {len(task_names)} 个任务")

# ---- 9. 元组不可变演示 ----
point = (10, 20)
x, y = point                                 # 元组解包
print(f"\n坐标解包：x={x}, y={y}")
a, b = 1, 2
a, b = b, a                                  # 变量交换（利用元组解包）
print(f"交换（a=1,b=2 → a={a}, b={b}）")

# ---- 10. 星号解包 ----
first, *middle, last = tasks
print(f"\n第一个任务：{first[1]}")
print(f"中间任务数量：{len(middle)}")
print(f"最后一个任务：{last[1]}")

# ---- 11. 反转切片查看（不修改原列表）----
print(f"\n逆序查看任务（低优先级 → 高优先级）：")
for priority, name, _ in tasks[::-1][:3]:   # 反转后取前3
    print(f"  优先级 {priority}：{name}")
