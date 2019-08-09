"""
global config
"""

import queue

# set queue for watcher
queue_log = queue.Queue(maxsize=20)
# set queue for processing
# processing thread could take a long time, so we need larger buffer
queue_process = queue.Queue(maxsize=200)

