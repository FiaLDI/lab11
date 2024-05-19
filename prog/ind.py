#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего индивидуального задания лабораторной работы 2.23 
# необходимо реализовать вычисление значений в двух 
# функций в отдельных процессах.

# Вариант 1 и 2

import math
from multiprocessing import Process, Queue

E = 10e-7


# 1 Вариант
def calculate_row_1(target, x, conditional_var):
    def calculate_nextpart(results, x, cur):
        return results[-1] * x * math.log(3) / cur

    i = 0
    local_result = [1]
    while local_result[i] > E:
        local_result.append(calculate_nextpart(local_result, x, i + 1))
        i += 1

    conditional_var.put(sum(local_result))


# 2 Вариант
def calculate_row_2(target, x, conditional_var):
    def calculate_nextpart(results, x):
        return results[-1] * x

    i = 0
    local_result = [1]
    while local_result[i] > E:
        local_result.append(calculate_nextpart(local_result, x))
        i += 1

    conditional_var.put(sum(local_result))


def check_results(target, x1, x2):
    def control_value_1(x):
        return 3**x

    def control_value_2(x):
        return round(1 / (1 - x), 4)

    print(
        f'Различие найденной суммы с контрольным значением {control_value_1(x1) - target.get("sum_row_1")}'
    )
    print(
        f'Различие найденной суммы с контрольным значением {control_value_2(x2) - target.get("sum_row_2")}'
    )
    print(f"Результат {target}")


def main():
    conditional_var = Queue()

    part_of_rows = {"sum_row_1": 0, "sum_row_2": 0}

    p1 = Process(target=calculate_row_1, args=(part_of_rows, 1, conditional_var))
    p2 = Process(target=calculate_row_2, args=(part_of_rows, 0.7, conditional_var))
    p3 = Process(target=check_results, args=(part_of_rows, 1, 0.7))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    part_of_rows["sum_row_1"] = conditional_var.get()
    part_of_rows["sum_row_2"] = conditional_var.get()
    
    p3.start()
    
    

if __name__ == "__main__":
    main()
