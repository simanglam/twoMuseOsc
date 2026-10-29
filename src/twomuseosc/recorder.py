import time
import uuid

import numpy as np
from matplotlib import pyplot as plt
from mne import Epochs, EpochsArray, annotations_from_events, find_events
from mne.io import read_raw_fif

from mne_lsl.datasets import sample
from mne_lsl.lsl import resolve_streams, StreamInlet
from mne_lsl.player import PlayerLSL
from mne_lsl.stream import EpochsStream, StreamLSL
from hypyp import analyses

streams = resolve_streams()
print(streams[0])

a = StreamLSL(10, name = streams[0].name, stype = streams[0].stype, source_id = streams[0].source_id).connect(acquisition_delay=0.05, processing_flags="all")

a.start_record("./record1028Simanglam.xdf", overwrite = True)


time.sleep(60 * 10)

a.stop_record()
a.disconnect()
