
import numpy as np

def compare_timeline(a, b, window_sec=10):
    _, ta = a.get_data(winsize=window_sec)
    _, tb = b.get_data(winsize=window_sec)

    if len(ta) < 10 or len(tb) < 10:
        print("資料不足")
        return

    # 兩台裝置在各自時間戳上的時間範圍
    start = max(ta[0], tb[0])
    end = min(ta[-1], tb[-1])

    print(f"共同時間範圍: {end - start:.3f} s")
    print(f"Muse A 範圍: {ta[0]:.3f}–{ta[-1]:.3f}")
    print(f"Muse B 範圍: {tb[0]:.3f}–{tb[-1]:.3f}")

    if end <= start:
        print("沒有共同時間範圍，請檢查時間戳是否處於相同時鐘基準")
        return

    print(f"共同範圍起點差: {abs(ta[0] - tb[0]) * 1000:.2f} ms")
    print(f"共同範圍終點差: {abs(ta[-1] - tb[-1]) * 1000:.2f} ms")

compare_timeline(a, b)
