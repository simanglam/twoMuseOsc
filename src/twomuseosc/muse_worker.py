# muse_worker.py
import sys
from muselsl import stream

if __name__ == "__main__":
    address = sys.argv[1]

    stream(
        address,
        interface="auto",
        backend="auto",
        name=address,
        
    )