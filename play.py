
import time
import uuid
import pyxdf
import numpy as np
from matplotlib import pyplot as plt
from mne import Epochs, EpochsArray, annotations_from_events, find_events
from mne.io import read_raw_fif

from mne_lsl.datasets import sample
from mne_lsl.lsl import resolve_streams, StreamInlet
from mne_lsl.player import PlayerLSL
from mne_lsl.stream import EpochsStream, StreamLSL
from hypyp import analyses
import mne
streams, header  = pyxdf.load_xdf("./record1028Simanglam.xdf")
# 2. 找到你的 EEG 訊號流 (此處假設 streams[0] 是 EEG，請依實際格式調整)
eeg_stream = streams[0]
data = eeg_stream["time_series"].T  # 轉置符合 MNE (n_channels, n_times) 的格式
sfreq = float(eeg_stream["info"]["nominal_srate"][0])
ch_count = int(eeg_stream["info"]["channel_count"][0])

# 3. 建立 MNE Info 與 RawArray 物件
ch_names = [f"EEG_{i}" for i in range(ch_count)]
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types="eeg")
raw = mne.io.RawArray(data, info)
a = PlayerLSL(raw)
a.start()

time.sleep(100)