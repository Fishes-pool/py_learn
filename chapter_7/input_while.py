"""
Demo: 命令行 Todo 应用
场景：通过 while True 驱动主循环，演示 input()、循环控制、列表动态修改。
注意：可直接运行（交互模式）。若需无交互演示，将 DEMO_MODE 改为 True。
"""

DEMO_MODE = True   # True: 自动执行预设命令序列；False: 真实交互

# ---- 数据结构 ----
todos = []         # 未完成任务
done = []          # 已完成任务


def show_todos():
    """显示当前任务列表。"""
    if not todos:                       # 真值测试空列表
        print("  （暂无待办任务）")
        return
    for i, task in enumerate(todos, start=1):
        print(f"  {i}. {task}")


def show_help():
    print("  命令：add <任务>  done <编号>  list  undo  clear  quit")


# ---- 预设命令（仅 DEMO_MODE 使用）----
demo_commands = [
    "add 完成项目文档",
    "add 修复登录 BUG",
    "add 更新依赖版本",
    "add 代码 review",
    "list",
    "done 2",
    "done 1",
    "list",
    "undo",
    "list",
    "clear",
    "quit",
]
demo_index = 0


def get_input(prompt: str) -> str:
    """根据模式返回用户输入或预设命令。"""
    global demo_index
    if DEMO_MODE and demo_index < len(demo_commands):
        cmd = demo_commands[demo_index]
        demo_index += 1
        print(f"{prompt}{cmd}")         # 模拟用户输入显示
        return cmd
    return input(prompt)


# ---- 主循环 ----
print("=" * 45)
print("命令行 Todo 应用")
print("=" * 45)
show_help()
print()

while True:                            # while True + break 模式（替代 do-while）
    raw = get_input(">>> ").strip()

    if not raw:                        # 真值测试：空字符串为 falsy
        continue

    # 解析命令和参数
    parts = raw.split(maxsplit=1)      # 最多分割一次
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    if cmd == "add":
        if not arg:
            print("请输入任务名称，例如：add 买咖啡")
            continue
        todos.append(arg.strip())
        print(f"  已添加：「{arg.strip()}」（共 {len(todos)} 个任务）")

    elif cmd == "done":
        if not arg.isdigit():
            print("请输入有效的任务编号，例如：done 1")
            continue
        index = int(arg) - 1           # 转换为 0-based 索引
        if not (0 <= index < len(todos)):   # 链式比较
            print(f"  编号 {arg} 超出范围（当前 {len(todos)} 个任务）")
            continue
        task = todos.pop(index)         # pop 返回被删除的元素
        done.append(task)
        print(f"  完成：「{task}」（还剩 {len(todos)} 个任务）")

    elif cmd == "list":
        print(f"\n待办任务（{len(todos)} 个）：")
        show_todos()
        if done:
            print(f"已完成（{len(done)} 个）：")
            for task in done:
                print(f"  ✓ {task}")
        print()

    elif cmd == "undo":
        if not done:
            print("没有可撤销的任务")
            continue
        task = done.pop()               # 从已完成取出最后一个
        todos.insert(0, task)           # 插入到待办队首
        print(f"  已撤销：「{task}」移回待办")

    elif cmd == "clear":
        count = len(todos)
        todos.clear()                   # 清空列表
        print(f"  已清空 {count} 个待办任务")

    elif cmd in ("quit", "exit", "q"):  # in 检测多个匹配值
        print(f"\n再见！本次完成 {len(done)} 个任务。")
        break                           # 退出 while True 循环

    else:
        print(f"  未知命令：{cmd!r}")
        show_help()

# ---- while 消耗列表演示 ----
print("\n处理已完成任务（while 消耗列表）：")
archive = done[:]                       # 复制列表
while archive:                          # 列表为空时自动结束
    task = archive.pop(0)
    print(f"  归档：{task}")

print("所有任务已归档。")
