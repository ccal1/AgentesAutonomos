import numpy as np
from collections import deque


def ackleyFunc(cromossom):
    value = 0
    c1 = 20
    c2 = 0.2
    c3 = 2 * np.pi

    cromossomTemp = cromossom
    root_mean_square = np.sqrt((cromossomTemp * cromossomTemp).mean())

    value = -c1 * np.exp(-c2 * root_mean_square)

    cosine_mean = np.cos(cromossomTemp * c3).mean()

    value = value - np.exp(cosine_mean) + c1 + np.exp(1)

    return value


class EE1:
    def __init__(self, cromossom=30 * np.random.rand(30) - 15, sigma=np.random.rand(), improvement_count=0,
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
        #     self.sigma = np.random.rand()

        self.it_number += 1


class EE2:

    def __init__(self, cromossom=30 * np.random.rand(30) - 15, sigma=np.random.rand(), it_number=1):
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
        tal = 1/np.sqrt(30)
        newSigma = self.sigma * np.exp(tal*np.random.randn())
        
        if self.threshold > newSigma:
            newSigma = self.threshold

        return newSigma

    def calc_mutation(self):
        newSigma = self.calc_sigma()
        cromossomTemp = self.cromossom + newSigma*np.random.randn(30)

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
        #     self.sigma = np.random.rand()



class EE3:
    def __init__(self, cromossom=30 * np.random.rand(30) - 15, sigma=np.random.rand(30), it_number=1):
        self.cromossom = cromossom
        self.sigma = sigma
        self.fitness = ackleyFunc(self.cromossom)
        self.eps = 1e-12
        self.it_number = it_number
        self.sigma_parameter = 0.95
        self.t = 1.0/np.sqrt(2*30)
        self.tl = 1.0/np.sqrt(np.sqrt(2*30))
        self.threshold = 0.5

    def calc_sigma(self):
        new_sigma = self.sigma * np.exp(self.t * np.random.randn(30) + self.tl*np.random.randn(30))
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
        #     self.sigma = np.random.rand()

        self.it_number += 1


def main():
    pop = EE2()
    print("Fitness_Inicial: %lf\n" % pop.fitness)
    # print "Cromossomo_Inicial: "
    print(pop.cromossom)
    print("\n")

    for i in range(10000):
        pop.iterate()
        print("\n\niteration:" + str(pop.it_number))
        print("fitness: " + str(pop.fitness))
        print("sigma: " + str(pop.sigma))


if __name__ == "__main__":
    main()