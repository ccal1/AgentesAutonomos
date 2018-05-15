import numpy as np
from evolutive_strategys import EE1
from evolutive_strategys import EE2
from evolutive_strategys import EE2c
from evolutive_strategys import EE3
from evolutive_strategys import EE3c
from evolutive_strategys import EE3xXablau
import matplotlib.pyplot as plt
import evolutive_strategys
import time

#Constants
POP_SIZE = 30
N = 5
ITERATIONS = 10000

def comp_EE(x):
    return x.fitness


def lesser_EE(x, y):
    if x.fitness < y.fitness:
        return True
    else:
        return False


def main():
    number_it_list = []
    means = []
    bests = []
    for i in range(N):
        #for i in range(POP_SIZE):
        #    pop_i = evolve_pop(100)
        #    print_pop(pop_i[0], str(i), "xablau")
        #    pop_i[0][0].reset_sigma()
        #    pop_i[0].append(pop_i[0][0])

        #pop_i[0].sort(key=comp_EE)
        #print_pop_cromossom(pop_i[0], "xit", "xat")
        #print_pop(pop_i[0], "xit", "xat")
        #evolve_pop(10000, pop_i[0])
        #print_pop(pop_i[0], "end", "end")
        pop, number_it, stds, bests_i = evolve_pop(ITERATIONS)
        number_it_list.append(number_it)
        means.append(stds)
        bests.append(bests_i)
        print(len(stds))
        print_pop(pop, "end", "end")
    #printing Number Iterations till converge
    number_it_list = np.array(number_it_list)
    number_it_mean = np.mean(number_it_list)
    print("mean of iterations to converge" + str(number_it_mean))
    #plotting Means by iteration
    plot_iterations_dots(means, "EE3c", "Average")
    plot_iterations_dots(bests, "EE3c", "Bests")
    plot_both(means,bests, "EE2c", "Average and Best")


def plot_iterations(means, algorithm, title):
    values = []
    medias = []
    desvios = []
    for i in range(0,ITERATIONS):
        for j in range(0,N):
            values.append(means[j][i])
        values = np.array(values)
        medias.append(np.mean(values))
        desvios.append(np.std(values))
        values = []
    x = np.arange(0, len(medias))
    fig, ax = plt.subplots()
    ax.errorbar(x, medias, yerr=desvios)
    ax.set_ylabel(title+'(+ standard deviation)')
    ax.set_xlabel('Iterations(Max = 10000)')
    ax.set_title('Population ' +title+' through ' + str(N) + ' iterations with ' + algorithm)
    plt.show()

def plot_iterations_dots(means, algorithm, title):
    values = []
    medias = []
    desvios = []
    for i in range(0,ITERATIONS):
        for j in range(0,N):
            values.append(means[j][i])
        values = np.array(values)
        medias.append(np.mean(values))
        desvios.append(np.std(values))
        values = []
    x = np.arange(0, len(medias))
    fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(x, medias)
    ax[0].set_ylabel('Average')
    ax[0].set_title('Polulation ' + title + ' through 30' + ' iterations with ' + algorithm)
    ax[1].plot(x, desvios)
    ax[1].set_ylabel('Standard Deviation')
    ax[1].set_xlabel('Iterations')
    plt.show()

def plot_both(means, best, algorithm, title):
    values = []
    medias = []
    bests = []
    melhores = []
    for i in range(0,ITERATIONS):
        for j in range(0,N):
            values.append(means[j][i])
            bests.append(best[j][i])
        bests = np.array(bests)
        values = np.array(values)
        medias.append(np.mean(values))
        melhores.append(np.mean(bests))
        values = []
        bests = []
    x = np.arange(0, len(medias))
    fig, ax = plt.subplots()
    ax.plot(x, medias)
    ax.set_ylabel('Average and best(red)')
    ax.set_title('Polulation ' + title + ' through 30' + ' iterations with ' + algorithm)
    ax.plot(x, melhores, 'r')

    plt.show()

def generate_pop():
    pop = []
    for i in range(POP_SIZE):
        pop.append(EE3c(30 * np.random.rand(30) - 15, np.random.random(30)))
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
        print(i.fitness)
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
    number_it = -1
    means = []
    bests = []
    for i in range(iterations):
        parents_index = np.random.randint(POP_SIZE, size=parents_size)
        parents_index.sort()

        offspring = []

        if POP_SIZE == 1:
            pop[0].iterate()
        else:
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
        mean_fitness = calculate_mean_fitness(pop)
        means.append(mean_fitness)
        bests.append(pop[0].fitness)
        if (pop[0].fitness < 0.1 and number_it == -1):
            number_it = i
    if number_it == -1:
        number_it = ITERATIONS
    return pop, number_it, means, bests


def reduce(parents_index):
    parents_index2 = [parents_index[0]]
    idx = 0
    for parent in parents_index:
        if parents_index2[idx] != parent:
            parents_index2.append(parent)
            idx += 1
    return parents_index2

def calculate_mean(lis):
    mean = 0
    amount = len(lis)
    for i in lis:
        mean += i
    return mean/amount

def calculate_std_dev(lis):
    mean = calculate_mean_fitness(lis)
    amount = len(lis)
    std_dev = 0
    for i in pop:
        std_dev += (i - mean)**2
    std_dev /= amount
    std_dev = np.sqrt(std_dev)
    return std_dev

def calculate_mean_fitness(pop):
    fit_mean = 0
    amount = len(pop)
    for i in pop:
        fit_mean += i.fitness
    return fit_mean/amount

def calculate_std_deviation_fitness(pop):
    fit_mean = calculate_mean_fitness(pop)
    amount = len(pop)
    std_dev = 0
    for i in pop:
        std_dev += (i.fitness - fit_mean)**2
    std_dev /= amount
    std_dev = np.sqrt(std_dev)
    return std_dev

if __name__ == "__main__":
    main()