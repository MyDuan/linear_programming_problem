# -*- coding: utf-8 -*-

import pulp
import time


def linear_programming(x_info, max_min):

    problem = pulp.LpProblem('Cost', pulp.LpMinimize)

    # Objective
    problem += pulp.lpSum(x_value['cost'] * x_value['quantity']
                          for x_name, x_value in x_info.items()), 'Objective'
    # conditions
    for b_name, b_range in max_min.items():
        problem += sum(x_value['quantity'] * x_value[b_name] / 100.0
                       for x_value in x_info.values()) >= b_range['min']
        problem += sum(x_value['quantity'] * x_value[b_name] / 100.0
                       for x_value in x_info.values()) <= b_range['max']
    status = {}

    time_start = time.clock()
    status['status'] = problem.solve()
    time_stop = time.clock()
    status['running_time'] = time_stop - time_start

    return status, x_info
