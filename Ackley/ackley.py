import numpy as np
from evolutive_strategys import EE1
from evolutive_strategys import EE2
from evolutive_strategys import EE2c
from evolutive_strategys import EE3
from evolutive_strategys import EE3c
from evolutive_strategys import EE3xXablau
import evolutive_strategys
import time

POP_SIZE = 30


def comp_EE(x):
    return x.fitness


def lesser_EE(x, y):
    if x.fitness < y.fitness:
        return True
    else:
        return False


def main():
    pop = []
    # for i in range(POP_SIZE):
    #     pop_i = evolve_pop(100)
    #     print_pop(pop_i, str(i), "xablau")
    #     pop_i[0].reset_sigma()
    #     pop.append(pop_i[0])

    # pop.sort(key=comp_EE)
    # print_pop_cromossom(pop, "xit", "xat")
    #
    # print_pop(pop, "xit", "xat")
    # evolve_pop(10000, pop)
    # print_pop(pop, "end", "end")
    pop = evolve_pop(10000)
    print_pop(pop, "end", "end")

def generate_pop():
    pop = []
    for i in range(POP_SIZE):
        pop.append(EE3c(30 * np.random.rand(30) - 15, np.random.rand(30)))
    pop.sort(key=comp_EE)
    return pop


def print_pop_cromossom(pop, message_before="begin", message_after="end"):
    print(message_before + ":\n")

    for i in pop:
        print(i.cromossom)
        # print(i.get_sigma())
        # print(i.get_cromossom())

    print(message_after + ":\n")


def print_pop(pop, message_before, message_after):
    print(message_before + ":\n")

    for i in pop:
        print(i.get_fitness())
        # print(i.get_sigma())
        # print(i.get_cromossom())

    print(message_after + ":\n")


def roulette(pop, parents_size):
    fit_sum = 0
    probs = []
    for j in range(POP_SIZE):
        tmp = 1 / (pop[j].fitness + 0.1)
        fit_sum += tmp
        probs.append(fit_sum)

    for j in range(POP_SIZE):
        probs[j] /= fit_sum

    parents_index_prob = np.random.rand(parents_size)
    parents_index = []
    parents_index_prob.sort()
    idx = 0
    for j in range(len(probs)):
        prob = probs[j]
        while idx < parents_size and prob >= parents_index_prob[idx]:
            parents_index.append(j)
            idx += 1

    return parents_index


def evolve_pop(iterations, pop=generate_pop()):
    evolutive_strategys.time_seed()
    parents_size = 6
    for i in range(iterations):
        parents_index = np.random.randint(POP_SIZE, size=parents_size)
        parents_index.sort()

        offspring = []

        for j in range(parents_size):
            parent1 = pop[parents_index[j]]
            for k in range(j + 1, parents_size):
                parent2 = pop[parents_index[k]]
                offspring.append(parent1.crossover_random(parent2))

        for j in offspring:
            for k in range(1):
                j.iterate()

        offspring.sort(key=comp_EE)

        parents_index = reduce(parents_index)

        offspring_idx = 0
        for parent_idx in range(len(parents_index)):
            if lesser_EE(offspring[offspring_idx], pop[parents_index[parent_idx]]):
                pop[parents_index[parent_idx]] = offspring[offspring_idx]
                offspring_idx += 1

        pop.sort(key=comp_EE)
    return pop


def reduce(parents_index):
    parents_index2 = [parents_index[0]]
    idx = 0
    for parent in parents_index:
        if parents_index2[idx] != parent:
            parents_index2.append(parent)
            idx += 1
    return parents_index2


if __name__ == "__main__":
    main()
