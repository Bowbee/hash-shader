#!/usr/bin/env python2
import subprocess
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

class BlockChainValidator:
    def __init__(self, cmd, name, color):
        self.data = []
        self.cmd = os.path.join(os.path.dirname(__file__), cmd)
        self.name = name
        self.color = color

    def run(self, filename, n):
        data_point = subprocess.check_output([self.cmd, filename, str(n)]).decode("utf-8")
        [b, t] = str(data_point).split()
        self.data.append([int(b), float(t)])

    def plot(self):
        plt.plot(np.array(self.data)[:,0], np.array(self.data)[:,1], c=self.color, label=self.name, linewidth=7.0)


validators = [BlockChainValidator('c/cuda_bitcoin', 'Cuda', 'red'),
              BlockChainValidator('c/cpu_bitcoin', 'CPU', 'blue'),
              BlockChainValidator('vulkan/target/release/blockchain-val', 'rust gpu / Vulkan', 'green')]

# cuda crashes on some numbers for some reason
for blocks in [10, 100, 999, 14999, -1]:
    print blocks
    for comp in validators:
        comp.run(sys.argv[1], blocks)


for comp in validators:
    comp.plot()
plt.ylabel("computatiopn time (ms)");
plt.xlabel("number of blocks verified");
plt.legend()
plt.show()
