# -*- coding: utf-8 -*-

import random
import numpy as np
from decimal import *

# 遺伝子集団の大きさ
MAX_GENOM_LIST = 100
# 遺伝子選択数
SELECT_GENOM = 20
# 個体突然変異確率
INDIVIDUAL_MUTATION = 0.1
# 遺伝子突然変異確率
GENOM_MUTATION = 0.1
# 繰り返す世代数
MAX_GENERATION = 10


class Genom:

    genom_list = None
    evaluation = None
    condition_ok = True

    def __init__(self, genom_list, evaluation):
        self.genom_list = genom_list
        self.evaluation = evaluation

    def get_genom(self):
        return self.genom_list

    def get_evaluation(self):
        return self.evaluation

    def set_genom(self, genom_list):
        self.genom_list = genom_list

    def set_evaluation(self, evaluation):
        self.evaluation = evaluation

    def get_condition(self):
        return self.condition_ok

    def set_condition(self):
        return self.condition_ok


def create_genom(length):
    genome_list = []
    for _ in range(length):
        genome_list.append(1000.0 * random.random())
    return Genom(genome_list, 0)


def evaluation(ga, unit):
    genom_total = Decimal(0.0)
    genome_list = ga.get_genom()
    for i in range(len(genome_list)):
        genom_total += Decimal(genome_list[i]) * Decimal(unit[i])
    return genom_total


def select(ga_group, elite_length, a, upper, lower):
    for ga in ga_group:
        genome_list = ga.get_genom()
        for i in range(len(upper)):
            sum = 0.0
            for j in range(len(genome_list)):
                sum += genome_list[j] * a[j][i]
            if sum > upper[j] or sum < lower[j]:
                ga.condition_ok = False
                break

    sort_result = sorted(ga_group, key=lambda u: u.evaluation)
    result = [sort_result.pop(0) for _ in range(elite_length)]
    return result


def crossover(ga_one, ga_second, genon_length):
    genom_list = []
    cross_one = random.randint(0, genon_length)
    cross_second = random.randint(cross_one, genon_length)
    one = ga_one.get_genom()
    second = ga_second.get_genom()
    progeny_one = one[:cross_one] + second[cross_one:cross_second] + one[cross_second:]
    progeny_second = second[:cross_one] + one[cross_one:cross_second] + second[cross_second:]
    genom_list.append(Genom(progeny_one, 0))
    genom_list.append(Genom(progeny_second, 0))
    return genom_list


def next_generation_gene_create(ga_group, ga_elite, ga_progeny):
    next_generation_geno = sorted(ga_group, reverse=True, key=lambda u: u.evaluation)
    for _ in range(0, len(ga_elite) + len(ga_progeny)):
        next_generation_geno.pop(0)
    next_generation_geno.extend(ga_elite)
    next_generation_geno.extend(ga_progeny)
    return next_generation_geno


def mutation(ga_group, individual_mutation, genom_mutation):
    ga_list = []
    for i in ga_group:
        if individual_mutation > (random.randint(0, 100) / Decimal(100)):
            genom_list = []
            for i_ in i.get_genom():
                if genom_mutation > (random.randint(0, 100) / Decimal(100)):
                    genom_list.append(i_ + 5.0)
                else:
                    genom_list.append(i_)
            i.set_genom(genom_list)
            ga_list.append(i)
        else:
            ga_list.append(i)
    return ga_list


def get_info(x_info, max_min):
    a = []
    unit = []
    upper = []
    lower = []
    for item in max_min:
        upper.append(max_min[item]["max"])
        lower.append(max_min[item]["min"])
    a_num = len(upper)
    for item in x_info:
        x_item = x_info[item]
        unit.append(x_item["cost"])
        for i in range(a_num):
            a.append(x_item[str(i+1)])
    a_arr = np.array(a).reshape([-1, a_num]).tolist()
    return a_arr, unit, upper, lower


def run_genetic_algorithm(x_info, max_min):
    genon_length = len(x_info.keys())
    a, unit, upper, lower = get_info(x_info, max_min)

    current_generation_individual_group = []

    for _ in range(MAX_GENOM_LIST):
        current_generation_individual_group.append(create_genom(genon_length))

    for _ in range(1, MAX_GENERATION + 1):
        for i in range(MAX_GENOM_LIST):
            evaluation_result = evaluation(current_generation_individual_group[i], unit)
            current_generation_individual_group[i].set_evaluation(evaluation_result)

        elite_genes = select(current_generation_individual_group, SELECT_GENOM, a, upper, lower)
        progeny_gene = []

        for i in range(0, SELECT_GENOM):
            progeny_gene.extend(crossover(elite_genes[i - 1], elite_genes[i], genon_length))

        next_generation_individual_group = next_generation_gene_create(current_generation_individual_group,
                                                                       elite_genes, progeny_gene)
        next_generation_individual_group = mutation(next_generation_individual_group, INDIVIDUAL_MUTATION,
                                                    GENOM_MUTATION)

        [i.get_evaluation() for i in current_generation_individual_group]
        current_generation_individual_group = next_generation_individual_group

    for i in range(len(elite_genes)):
        if elite_genes[i].get_condition():
            best_unit = elite_genes[i].get_genom()
            cost = elite_genes[i].get_evaluation()
            break
        else:
            best_unit = elite_genes[0].get_genom()
            cost = elite_genes[0].get_evaluation()
    results = {}
    i = 0
    for x_name, _ in x_info.items():
        results[x_name] = round(best_unit[i], 6)
        i += 1
    results['sum_cost'] = round(float(cost), 6)
    return results

