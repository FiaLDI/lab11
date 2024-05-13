#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего индивидуального задания лабораторной работы 2.23
# необходимо реализовать
# вычисление значений в двух функций в отдельных процессах.

import math
from multiprocessing import Process, Queue
from threading import Barrier, Thread

E = 10e-7
br = Barrier(4)
results = [1]
local_results = Queue()


def calculate_sum(x):
    return 3**x


def calculate_part(x, cur, result_queue):
    local_result = [1]

    def my_log(local_result):
        local_result[0] *= math.pow(math.log(3), cur)
        br.wait()

    def my_pow(local_result):
        local_result[0] *= x**cur
        br.wait()

    def my_fact(local_result):
        local_result[0] /= math.factorial(cur)
        br.wait()

    Thread(target=my_log, args=(local_result,)).start()
    Thread(target=my_pow, args=(local_result,)).start()
    Thread(target=my_fact, args=(local_result,)).start()

    br.wait()
    result_queue.put(local_result[0])


def main():
    x = 3
    i = 0

    while not (round(sum(results), 5) == calculate_sum(x)):
        Process(target=calculate_part, args=(x, i + 1, local_results)).start()
        results.append(local_results.get())
        i += 1

    print(results)
    print(f"x = {x}")
    print(round(sum(results), 5))
    print(round(sum(results), 5) == calculate_sum(x))


if __name__ == "__main__":
    main()
