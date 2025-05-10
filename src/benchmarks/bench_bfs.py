import sys
import os
import time

sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + '/build')
import numpy as np

import bfs_module

g_s = time.time()
effective_time = 0
for epoch in range(1000):
    if epoch == 1: st = time.time()
    field = np.zeros((100, 100), dtype=np.uint8)
    p = np.random.randint(0, 99, 200)
    field[p[:100], p[100:]] = 5
    s = time.time()
    legs = bfs_module.find_path_legs(field, (0, 0), (99, 99))
    effective_time += time.time() - s
print(f"effective_time={effective_time}, total_time={time.time()-g_s}")
