"""
Demo: 专辑信息处理工具
场景：音乐库管理系统，展示函数的各种参数特性、返回值、类型注解、lambda、模块化。
演示：位置/关键字参数、默认参数、*args、**kwargs、返回多值、lambda、类型注解。
"""

from typing import Optional


# ---- 1. 基本函数 + 类型注解 ----
def format_duration(seconds: int) -> str:
    """将秒数格式化为 mm:ss。"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


# ---- 2. 默认参数（正确做法：None 替代可变对象）----
def create_album(
    title: str,
    artist: str,
    year: int,
    genre: str = "Unknown",
    tracks: Optional[list] = None,    # 不用 tracks=[]（可变对象陷阱）
) -> dict:
    """创建专辑信息字典。"""
    if tracks is None:
        tracks = []
    return {
        "title": title,
        "artist": artist,
        "year": year,
        "genre": genre,
        "tracks": tracks,
    }


# ---- 3. *args：任意数量位置参数 ----
def add_tracks(album: dict, *track_names: str) -> dict:
    """批量添加曲目到专辑。*track_names 接收任意数量字符串，类型是元组。"""
    for track in track_names:         # track_names 是元组
        album["tracks"].append({"title": track, "duration": 0})
    return album


# ---- 4. **kwargs：任意数量关键字参数 ----
def update_track_info(album: dict, track_index: int, **kwargs) -> None:
    """更新曲目信息，支持任意字段。**kwargs 得到字典。"""
    if 0 <= track_index < len(album["tracks"]):
        album["tracks"][track_index].update(kwargs)   # kwargs 是字典


# ---- 5. 返回多个值（实际返回元组）----
def analyze_album(album: dict) -> tuple[int, int, int]:
    """返回专辑的曲目数、总时长（秒）、平均时长（秒）。"""
    tracks = album["tracks"]
    if not tracks:
        return 0, 0, 0
    total = sum(t.get("duration", 0) for t in tracks)
    avg = total // len(tracks)
    return len(tracks), total, avg    # 返回元组，调用方解包


# ---- 6. 函数作为参数 + lambda ----
def sort_albums(albums: list[dict], key_func=None, reverse: bool = False) -> list[dict]:
    """对专辑列表排序，key_func 默认按年份。"""
    if key_func is None:
        key_func = lambda a: a["year"]    # 默认：按年份
    return sorted(albums, key=key_func, reverse=reverse)


# ---- 7. 强制关键字参数（* 后的参数）----
def export_album(album: dict, *, format: str = "json", include_tracks: bool = True) -> str:
    """导出专辑信息，format 和 include_tracks 必须用关键字传入。"""
    data = {k: v for k, v in album.items() if k != "tracks" or include_tracks}
    if format == "json":
        import json
        return json.dumps(data, ensure_ascii=False, indent=2)
    elif format == "text":
        lines = [f"{k}: {v}" for k, v in data.items() if k != "tracks"]
        return "\n".join(lines)
    return str(data)


# ---- 主程序 ----
if __name__ == "__main__":
    print("=" * 50)
    print("专辑信息处理工具")
    print("=" * 50)

    # 关键字参数调用（顺序可以乱）
    album1 = create_album(
        artist="Pink Floyd",
        title="The Dark Side of the Moon",
        year=1973,
        genre="Progressive Rock",
    )

    # 位置参数调用
    album2 = create_album("OK Computer", "Radiohead", 1997, "Alternative Rock")

    # *args 批量添加曲目
    add_tracks(album1,
               "Speak to Me", "Breathe", "On the Run",
               "Time", "The Great Gig in the Sky",
               "Money", "Us and Them", "Any Colour You Like",
               "Brain Damage", "Eclipse")

    add_tracks(album2,
               "Airbag", "Paranoid Android", "Subterranean Homesick Alien",
               "Exit Music", "Let Down", "Karma Police",
               "Fitter Happier", "Electioneering", "Climbing Up the Walls",
               "No Surprises", "Lucky", "The Tourist")

    # **kwargs 更新曲目信息
    track_durations = [68, 169, 229, 421, 276, 382, 462, 229, 238, 247]
    for i, duration in enumerate(track_durations):
        update_track_info(album1, i, duration=duration, remastered=True)

    # 返回多值解包
    track_count, total_sec, avg_sec = analyze_album(album1)
    print(f"\n《{album1['title']}》")
    print(f"  艺术家：{album1['artist']}  年份：{album1['year']}")
    print(f"  曲目数：{track_count}")
    print(f"  总时长：{format_duration(total_sec)}")
    print(f"  平均：  {format_duration(avg_sec)}")

    # 曲目列表
    print("  曲目：")
    for i, track in enumerate(album1["tracks"], start=1):
        dur = format_duration(track.get("duration", 0))
        print(f"    {i:2d}. {track['title']} ({dur})")

    # lambda + sort
    albums = [album1, album2,
              create_album("Abbey Road", "The Beatles", 1969, "Rock"),
              create_album("Thriller", "Michael Jackson", 1982, "Pop")]

    print("\n按年份排序（新→旧）：")
    for a in sort_albums(albums, reverse=True):
        print(f"  {a['year']} - {a['title']} / {a['artist']}")

    print("\n按艺术家名首字母排序：")
    for a in sort_albums(albums, key_func=lambda a: a["artist"]):
        print(f"  {a['artist']:25s} - {a['title']}")

    # 强制关键字参数导出
    print("\n导出（text 格式，不含曲目）：")
    text = export_album(album2, format="text", include_tracks=False)
    print(text)
