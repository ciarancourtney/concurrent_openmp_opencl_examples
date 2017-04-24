#!/usr/bin/env python3

import logging
import subprocess
import platform
import time
import matplotlib.pyplot as plt

import opencl_array_reduce

logging.getLogger().setLevel(logging.INFO)

if not platform.system() == 'Linux':
    # C_BIN = ['bash.exe', '-c', '/mnt/c/workspace/openmp/pure_c_array_reduce']
    # OMP_BIN = ['bash.exe', '-c', '/mnt/c/workspace/openmp/openmp_array_reduce']
    C_BIN = ['pure_c_array_reduce.exe']
    OMP_BIN = ['openmp_array_reduce.exe']
else:
    C_BIN = ['./pure_c_array_reduce']
    OMP_BIN = ['openmp_array_reduce']


def extract_return_stats(output):
    stat_list = [int(s) for s in output.split(' ') if s.isdigit()]
    return stat_list[0], stat_list[1]


def plot_results(*arg):
    logging.info('Plotting Results...')

    legend = []
    for list in arg:
        legend.append(list[0][0])
        x = []
        y = []
        for result in list:
            x.append(result[1])
            y.append(result[2])

        plt.plot(x, y, linewidth=2)

    plt.xlabel('Array Size')
    plt.ylabel('Time (s)')
    plt.legend(legend, loc='upper left')
    plt.show()


class Benchmark(object):

    def __init__(self, start_size, double_count, iterations):
        logging.info('Initializing benchmark...')
        self.start_size = start_size
        self.double_count = double_count
        self.iterations = iterations
        self.range = 100

    def run(self, executable):
        array_size = self.start_size
        results = []
        count = 0
        while count < self.double_count:
            cmd = executable + [str(array_size), str(self.range)]
            x = 0
            time_ms = 0
            while x < self.iterations:
                p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout, stderr = p.communicate()
                time = float(stdout.decode().rstrip())
                x += 1
                time_ms += time

            results.append([executable[-1], array_size, time_ms/self.iterations])
            logging.info('[{}] average runtime for array size {} is {} sec'.format(executable[-1], array_size, time_ms/self.iterations))
            array_size *= 2
            count += 1

        return results

    def run_opencl(self):
        results = []
        power = 20
        while power < 27:  # 2**27 is the largest N possible on my machine
            iteration = 0
            time_s = 0
            array_size = 2 ** power
            while iteration < self.iterations:
                time = opencl_array_reduce.run(power)
                iteration += 1
                time_s += time
            results.append(['opencl', array_size, time_s/self.iterations])
            logging.info('[{}] average runtime for array size {} is {} sec'.format('opencl', array_size, time_s/self.iterations))
            power += 1

        return results

# init benchmark parameters
b = Benchmark(start_size=1000000, double_count=7, iterations=3)

# run each benchmark
pure_c = b.run(C_BIN)
time.sleep(1)
openmp = b.run(OMP_BIN)
time.sleep(1)
opencl = b.run_opencl()
time.sleep(1)

# plot all results in one graph
plot_results(pure_c, openmp, opencl)
