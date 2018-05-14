import numpy as np
import time
import datetime

from ackleyfunc import ackleyFunc


def time_seed():
    np.random.seed(datetime.datetime.now().microsecond)


class EE1:
    def __init__(self, cromossom=30 * np.random.random(30) - 15, sigma=np.random.random(), improvement_count=0,
                 it_number=1):
        self.cromossom = cromossom
        self.sigma = sigma
        self.fitness = ackleyFunc(self.cromossom)
        self.eps = 1e-12
        self.improvement_count = improvement_count
        self.it_number = it_number
        self.sigma_parameter = 0.95

    def calc_sigma(self):
        new_sigma = self.sigma
        if self.it_number % 5 == 0:
            sum_succ = self.improvement_count
            if sum_succ > 1:
                new_sigma /= self.sigma_parameter
            elif sum_succ < 1:
                new_sigma *= self.sigma_parameter
        return new_sigma

    def replace_with(self, child):
        self.cromossom = child.cromossom
        self.sigma = child.sigma
        self.fitness = child.fitness

    def calc_mutation(self):
        new_sigma = self.calc_sigma()
        cromossom_temp = self.cromossom + new_sigma * np.random.randn(30)

        return EE1(cromossom_temp, new_sigma, self.improvement_count, self.it_number)

    def iterate(self):
        child = self.calc_mutation()
        if child.fitness <= self.fitness:
            self.replace_with(child)
            self.improvement_count += 1

        if self.it_number % 5 == 0:
            self.improvement_count = 0

        self.sigma = self.calc_sigma()
        # if self.it_number %100 ==0:
        #     self.sigma = np.random.random()

        self.it_number += 1


class EE2:
    def __init__(self, cromossom=30 * np.random.random(30) - 15, sigma=np.random.random(), it_number=1):
        self.cromossom = cromossom
        self.sigma = sigma
        self.fitness = ackleyFunc(self.cromossom)
        self.threshold = 0.5
        self.eps = 1e-12
        self.it_number = it_number

    def set_cromossom(self, cromossom):
        self.cromossom = cromossom

    def set_sigma(self, sigma):
        self.sigma = sigma

    def set_fitness(self):
        self.fitness = ackleyFunc(self.cromossom)

    def get_fitness(self):
        return self.fitness

    def get_cromossom(self):
        return self.cromossom

    def calc_sigma(self):
        tal = 1 / np.sqrt(30)
        newSigma = self.sigma * np.exp(tal * np.random.randn())

        if self.threshold > newSigma:
            newSigma = self.threshold

        return newSigma

    def calc_mutation(self):
        newSigma = self.calc_sigma()
        cromossomTemp = self.cromossom + newSigma * np.random.randn(30)

        newMember = EE2()
        newMember.set_cromossom(cromossomTemp)
        newMember.set_sigma(newSigma)
        newMember.set_fitness()

        return newMember

    def replace_with(self, child):
        self.cromossom = child.cromossom
        self.sigma = child.sigma
        self.fitness = child.fitness

    def iterate(self):
        child = self.calc_mutation()
        if child.fitness <= self.fitness:
            self.replace_with(child)
        else:
            self.sigma = child.sigma

        self.it_number += 1

        # if self.it_number %100 ==0:
        #     self.sigma = np.random.random()


class EE2c:
    def __init__(self, cromossom=30 * np.random.random(30) - 15, sigma=np.random.random(), it_number=1):
        self.cromossom = cromossom
        self.sigma = sigma
        self.fitness = ackleyFunc(self.cromossom)
        self.threshold = 0.5
        self.eps = 1e-12
        self.it_number = it_number

    def set_cromossom(self, cromossom):
        self.cromossom = cromossom

    def set_sigma(self, sigma):
        self.sigma = sigma

    def set_fitness(self):
        self.fitness = ackleyFunc(self.cromossom)

    def get_fitness(self):
        return self.fitness

    def get_cromossom(self):
        return self.cromossom

    def get_sigma(self):
        return self.sigma

    def calc_sigma(self):
        tal = 1 / np.sqrt(30)
        newSigma = self.sigma * np.exp(tal * np.random.randn())

        if self.threshold > newSigma:
            newSigma = self.threshold

        return newSigma

    def calc_mutation(self):
        newSigma = self.calc_sigma()
        cromossomTemp = self.cromossom + newSigma * np.random.randn(30)

        newMember = EE2c()
        newMember.set_cromossom(cromossomTemp)
        newMember.set_sigma(newSigma)
        newMember.set_fitness()

        return newMember

    def replace_with(self, child):
        self.cromossom = child.cromossom
        self.sigma = child.sigma
        self.fitness = child.fitness

    def iterate(self):
        child = self.calc_mutation()
        if child.fitness <= self.fitness:
            self.replace_with(child)
        else:
            self.sigma = child.sigma

        self.it_number += 1

    def crossover_complete(self, other):
        alpha = 0.5
        return EE2c(alpha * self.cromossom + (1 - alpha) * other.cromossom, self.sigma, self.it_number)

    def crossover_random(self, other):
        prob = np.random.random(30)
        new_cromossom = np.zeros(30)
        for i in range(prob.size):
            if (prob[i] > 0.5):
                new_cromossom[i] = self.cromossom[i]
            else:
                new_cromossom[i] = other.cromossom[i]

        return EE2c(new_cromossom, self.sigma, self.it_number)


class EE3:
    def __init__(self, cromossom=30 * np.random.random(30) - 15, sigma=np.random.random(30), it_number=1):
        self.cromossom = cromossom
        self.sigma = sigma
        self.fitness = ackleyFunc(self.cromossom)
        self.eps = 1e-12
        self.it_number = it_number
        self.sigma_parameter = 0.95
        self.t = 1.0 / np.sqrt(2 * 30)
        self.tl = 1.0 / np.sqrt(np.sqrt(2 * 30))
        self.threshold = 0.5

    def calc_sigma(self):
        new_sigma = self.sigma * np.exp(self.t * np.random.randn(30) + self.tl * np.random.randn(30))
        return np.maximum(new_sigma, self.threshold + np.zeros(30))

    def replace_with(self, child):
        self.cromossom = child.cromossom
        self.sigma = child.sigma
        self.fitness = child.fitness

    def calc_mutation(self):
        new_sigma = self.calc_sigma()
        cromossom_temp = self.cromossom + new_sigma * np.random.randn(30)

        return EE3(cromossom_temp, new_sigma, self.it_number)

    def iterate(self):
        child = self.calc_mutation()
        if child.fitness <= self.fitness:
            self.replace_with(child)
        else:
            self.sigma = child.sigma
        # if self.it_number %100 ==0:
        #     self.sigma = np.random.random()
        
        self.it_number += 1


class EE3c:
    def __init__(self, cromossom=30 * np.random.random(30) - 15, sigma=np.random.random(30), it_number=1):
        self.cromossom = cromossom
        self.sigma = sigma
        self.fitness = ackleyFunc(self.cromossom)
        self.eps = 1e-12
        self.it_number = it_number
        self.sigma_parameter = 0.95
        self.t = 0.05 / np.sqrt(2 * 30)
        self.tl = 0.05 / np.sqrt(np.sqrt(2 * 30))
        self.threshold = 1

    def set_cromossom(self, cromossom):
        self.cromossom = cromossom

    def set_sigma(self, sigma):
        self.sigma = sigma

    def set_fitness(self):
        self.fitness = ackleyFunc(self.cromossom)

    def get_fitness(self):
        return self.fitness

    def get_cromossom(self):
        return self.cromossom

    def get_sigma(self):
        return self.sigma

    def reset_sigma(self):
        self.sigma = np.random.random(30)

    def calc_sigma(self):
        new_sigma = self.sigma * np.exp(self.t * np.random.randn() * np.random.randn() + self.tl * np.random.randn())
        return np.maximum(new_sigma, self.threshold + np.zeros(30))

    def replace_with(self, child):
        self.cromossom = child.cromossom
        self.sigma = child.sigma
        self.fitness = child.fitness

    def calc_mutation(self):
        new_sigma = self.calc_sigma()
        cromossom_temp = self.cromossom + new_sigma * np.random.randn()

        return EE3c(cromossom_temp, new_sigma, self.it_number)

    def iterate(self):
        child = self.calc_mutation()
        
        self.replace_with(child)

        self.it_number += 1
        if (not (self.it_number % 10)):
            self.threshold /= 2.0

    def crossover_complete(self, other):
        alpha = 0.5
        return EE3c(alpha * self.cromossom + (1 - alpha) * other.cromossom, self.sigma, self.it_number)

    def crossover_random(self, other):
        prob = np.random.randint(2, size=30)
        prob_no = 1 - prob

        new_cromossom = self.cromossom * prob + other.cromossom * prob_no

        prob = np.random.randint(2, size=30)
        prob_no = 1 - prob
        new_sigma = self.sigma * prob + other.sigma * prob_no

        return EE3c(new_cromossom, new_sigma, self.it_number)



class EE3xXablau:
    def __init__(self, cromossom=30 * np.random.random(30) - 15, sigma=np.random.random(30), it_number=1):
        self.cromossom = cromossom
        self.sigma = sigma
        self.fitness = ackleyFunc(self.cromossom)
        self.eps = 1e-12
        self.it_number = it_number
        self.sigma_parameter = 0.95
        self.t = 0.05 / np.sqrt(2 * 30)
        self.tl = 0.05 / np.sqrt(np.sqrt(2 * 30))
        self.threshold = 1

    def reset_sigma(self):
        self.sigma = np.random.random(30)

    def calc_sigma(self):
        new_sigma = self.sigma * np.exp(self.t * np.random.randn(30) + self.tl * np.random.randn())
        return np.maximum(new_sigma, self.threshold + np.zeros(30))

    def replace_with(self, child):
        self.cromossom = child.cromossom
        self.sigma = child.sigma
        self.fitness = child.fitness


    def mutate_index(self, i):
        sigma = self.sigma[i] * np.exp(self.t * np.random.randn() + self.tl * np.random.randn())
        sigma = np.maximum(sigma, self.threshold)
        cromossom = self.cromossom
        cromossom[i] = self.cromossom[i] + np.random.randn()*sigma
        if ackleyFunc(cromossom) <= self.fitness:
            self.cromossom[i] = cromossom[i]
            self.sigma[i] = sigma


    def iterate(self):
        for i in range(30):
            self.mutate_index(i)

        self.it_number += 1
        if (not (self.it_number % 10)):
            self.threshold /= 1.5

    def crossover_complete(self, other):
        alpha = 0.5
        return EE3c(alpha * self.cromossom + (1 - alpha) * other.cromossom, self.sigma, self.it_number)

    def crossover_random(self, other):
        prob = np.random.randint(2, size=30)
        prob_no = 1 - prob

        new_cromossom = self.cromossom * prob + other.cromossom * prob_no

        prob = np.random.randint(2, size=30)
        prob_no = 1 - prob
        new_sigma = self.sigma * prob + other.sigma * prob_no

        return EE3c(new_cromossom, new_sigma, self.it_number)
