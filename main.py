import asyncio
import sys
import time
import uuid

from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from mne import Epochs, EpochsArray, annotations_from_events, find_events
from mne.io import read_raw_fif

from mne_lsl.datasets import sample
from mne_lsl.lsl import resolve_streams, StreamInlet
from mne_lsl.player import PlayerLSL
from mne_lsl.stream import EpochsStream, StreamLSL
from hypyp import analyses

from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 5005
client = SimpleUDPClient(ip, port)

from muselsl import stream, list_muses
import subprocess


muses = list_muses()
processes = []
if muses is None or len(muses) < 2:
    print("找不到兩台 Muse 裝置，請確認 Muse 是否已開啟並配對。")
    exit(1)

try:
    for muse in muses:
        process = subprocess.Popen([
            sys.executable,
            "muse_worker.py",
            muse["address"],
        ])
        processes.append(process)
except:
    exit(1)
streams = resolve_streams()
while streams is None or len(streams) < 2:
    time.sleep(1)
    streams = resolve_streams()
    print("等待兩台 Muse 連線中...")

print(streams[0])
print(streams[1])

a = StreamLSL(10, name = streams[0].name, stype = streams[0].stype, source_id = streams[0].source_id).connect(acquisition_delay=0.05, processing_flags="all")
b = StreamLSL(10, name = streams[1].name, stype = streams[1].stype, source_id = streams[1].source_id).connect(acquisition_delay=0.05, processing_flags="all")



import numpy as np
from scipy.interpolate import interp1d


def align_muse_streams(
    muse_a: StreamLSL,
    muse_b: StreamLSL,
    window_sec: float =4.0,
    target_sfreq: float | None = None,
    max_gap_factor: float = 1.5
):
    """
    將兩個 MNE-LSL EEG 串流對齊到共同時間網格。

    Returns
    -------
    data_a_aligned : ndarray, shape (channels_a, samples)
    data_b_aligned : ndarray, shape (channels_b, samples)
    common_ts : ndarray, shape (samples,)
        共同的 LSL 時間戳。
    """

    # 取得兩台裝置最近 window_sec 秒的資料
    data_a, ts_a = muse_a.get_data(winsize=window_sec)
    data_b, ts_b = muse_b.get_data(winsize=window_sec)

    data_a = np.asarray(data_a)
    data_b = np.asarray(data_b)
    ts_a = np.asarray(ts_a)
    
    ts_b = np.asarray(ts_b)

    # print(np.diff(ts_b), np.any(np.diff(ts_b) <= 0))
    if len(ts_a) < 2 or len(ts_b) < 2:
        raise RuntimeError("EEG 樣本不足，請等待更多資料。")

    if data_a.shape[-1] != len(ts_a):
        raise ValueError("Muse A 的資料長度與時間戳不一致。")

    if data_b.shape[-1] != len(ts_b):
        raise ValueError("Muse B 的資料長度與時間戳不一致。")

    # 檢查時間戳必須嚴格遞增
    if np.any(np.diff(ts_a) <= 0) or np.any(np.diff(ts_b) <= 0):
        raise RuntimeError("時間戳不是嚴格遞增，需先檢查串流。")

    fs_a = float(muse_a.info["sfreq"])
    fs_b = float(muse_b.info["sfreq"])

    # 找兩台裝置都有資料的時間範圍
    t_start = max(ts_a[0], ts_b[0])
    t_end = min(ts_a[-1], ts_b[-1])

    if t_end <= t_start:
        raise RuntimeError("兩台 Muse 沒有重疊的時間區間。")

    # 建立共同取樣率
    if target_sfreq is None:
        if not np.isclose(fs_a, fs_b, rtol=0, atol=0.01):
            raise ValueError(
                f"取樣率不同：A={fs_a} Hz、B={fs_b} Hz。"
                "請先處理取樣率差異與抗混疊濾波，再指定 target_sfreq。"
            )
        target_sfreq = fs_a

    # 不允許超過任一裝置的原始取樣率
    if target_sfreq > min(fs_a, fs_b):
        raise ValueError(
            "target_sfreq 不應高於較低的原始取樣率。"
        )

    # 檢查時間戳缺口
    for name, ts, fs in (
        ("Muse A", ts_a, fs_a),
        ("Muse B", ts_b, fs_b),
    ):
        gaps = np.diff(ts)
        if np.any(gaps > max_gap_factor / fs):
            raise RuntimeError(
                f"{name} 有明顯時間戳缺口；"
                "請先處理掉包或中斷，避免跨缺口插值。"
            )

    # 共同時間網格
    n_samples = int(np.floor((t_end - t_start) * target_sfreq)) + 1
    common_ts = t_start + np.arange(n_samples) / target_sfreq

    # 將每個 EEG 通道插值到共同時間點
    def interpolate_data(data, ts):
        f = interp1d(
            ts,
            data,
            axis=-1,
            kind="linear",
            bounds_error=True,
        )
        return f(common_ts)

    aligned_a = interpolate_data(data_a, ts_a)
    aligned_b = interpolate_data(data_b, ts_b)

    return aligned_a, aligned_b, common_ts

time.sleep(12)
try:
    while True:
        align_a, align_b, common_ts = align_muse_streams(a, b, 10.0, a.info['sfreq'])
        freq_band = {'Delta': [1, 4],
                    'Theta': [4, 8],
                    'Alpha': [7.5, 13],
                    'Beta': [13, 30]}
        
        eeg_names_a = ["TP9", "AF7", "AF8", "TP10"]
        eeg_names_b = ["TP9", "AF7", "AF8", "TP10"]

        idx_a = [a.info["ch_names"].index(ch) for ch in eeg_names_a]
        idx_b = [b.info["ch_names"].index(ch) for ch in eeg_names_b]

        align_a_eeg = align_a[idx_a, :]
        align_b_eeg = align_b[idx_b, :]
        
        data = np.stack([align_a_eeg, align_b_eeg], axis=0)
        data = data[:, np.newaxis, :, :]

        coh = analyses.pair_connectivity(data, a.info['sfreq'],  freq_band, mode = "coh")
        
        n_ch = len(a.info['ch_names'])
# print(n_ch)
        Delta, Theta, Alpha, Beta = coh[:, 0:n_ch, n_ch:2*n_ch] # [0:n_channels, n_channels: 2*n_channels]
        client.send_message("/delta", Delta.mean())
        client.send_message("/theta", Theta.mean())
        client.send_message("/alpha", Alpha.mean())
        client.send_message("/beta", Beta.mean())
        time.sleep(0.5)
except KeyboardInterrupt:
    for process in processes:
        process.terminate()
    a.disconnect()
    b.disconnect()
    