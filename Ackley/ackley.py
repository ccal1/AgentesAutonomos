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

class EE2c:
	
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

	def get_sigma(self):
		return self.sigma

	def calc_sigma(self):
		tal = 1/np.sqrt(30)
		newSigma = self.sigma * np.exp(tal*np.random.randn())
        
		if self.threshold > newSigma:
			newSigma = self.threshold

		return newSigma

	def calc_mutation(self):
		newSigma = self.calc_sigma()
		cromossomTemp = self.cromossom + newSigma*np.random.randn(30)
		
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
		return EE2c(alpha*self.cromossom + (1-alpha)*other.cromossom, self.sigma, self.it_number)

	def crossover_random(self, other):
		prob = np.random.rand(30)
		new_cromossom = np.zeros(30)
		for i in range(prob.size):
 			if (prob[i] > 0.5):
				new_cromossom[i] = self.cromossom[i]
			else:
				new_cromossom[i] = other.cromossom[i]

		return EE2c(new_cromossom, self.sigma, self.it_number)


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

class EE3c:
	def __init__(self, cromossom=30 * np.random.rand(30) - 15, sigma=np.random.rand(30), it_number=1):
		self.cromossom = cromossom
		self.sigma = sigma
		self.fitness = ackleyFunc(self.cromossom)
		self.eps = 1e-12
		self.it_number = it_number
		self.sigma_parameter = 0.95
		self.t = 0.05/np.sqrt(2*30)
		self.tl = 0.05/np.sqrt(np.sqrt(2*30))
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

		return EE3c(cromossom_temp, new_sigma, self.it_number)

	def iterate(self):
		child = self.calc_mutation()
		if child.fitness <= self.fitness:
			self.replace_with(child)
		else:
			self.sigma = child.sigma
		# if self.it_number %100 ==0:
		#     self.sigma = np.random.rand()

		self.it_number += 1
		if (not(self.it_number % 1000)):
			self.threshold /= 10

	def crossover_complete(self, other):
		alpha = 0.5
		return EE3c(alpha*self.cromossom + (1-alpha)*other.cromossom, self.sigma, self.it_number)

	def crossover_random(self, other):
		prob = np.random.randint(2, size = 30)
		prob_no = 1 - prob
		new_cromossom = np.ones(30)
		new_sigma = np.ones(30)
		
		new_cromossom = new_cromossom*prob + new_cromossom*prob_no
		
		prob = np.random.randint(2, size = 30)
		prob_no = 1 - prob
		new_sigma = new_sigma*prob + new_sigma*prob_no

		return EE3c(new_cromossom, new_sigma, self.it_number)

def comp_EE(x):
	return x.get_fitness()

def lesser_EE(x,y):
	if (x.get_fitness() < y.get_fitness()):
		return True
	else:
		return False

def main():
	pop = []
	for i in range(30):
		pop.append(EE3c(30 * np.random.rand(30) - 15,np.random.rand(30)))

	pop.sort(key=comp_EE)
	print "Populacao Inicial:\n"

	for i in pop:
		print "Individuo:\n" 
		print(i.get_fitness())
		#print(i.get_sigma())
		#print(i.get_cromossom())

	print "Acabou Populacao Inicial\n"

	for i in range(100000):
		parents_index = np.random.randint(30,size = 60)
		offspring = []

		k = 0
		l = 0
		for j in range(30):
			offspring.append(pop[parents_index[k]].crossover_random(pop[parents_index[k+1]]))
			k += 2
		
		print "OFFSPRING INICIAL\n\n"

		for j in offspring:
			print "Individuo:\n" 
			print(j.get_fitness())
			#print(j.get_sigma())
			#print(j.get_cromossom())

		print "Acabou OFFSPRING INICIAL!!!!\n\n"
		
		for j in offspring:
			j.iterate()
		
		print "OFFSPRING FINAL\n\n"

		for j in offspring:
			print "Individuo:\n" 
			print(j.get_fitness())
			#print(j.get_sigma())
			#print(j.get_cromossom())

		print "Acabou OFFSPRING FINAL!!!!\n\n"
		
		offspring.sort(key=comp_EE)
		pop.sort(key=comp_EE)

		new_pop = []

		k = 0
		l = 0
		index = 0
		while (index < len(offspring)):
			if (lesser_EE(offspring[k],pop[l])):
				new_pop.append(offspring[k])
				k += 1
			else:
				new_pop.append(pop[l])
				l += 1
			index += 1

		'''print("\n\niteration:" + str(pop.it_number))
	                        print("fitness: " + str(pop.fitness))
	                        print("sigma: " + str(pop.sigma))'''
		pop = new_pop
		
		for j in pop:
			print "Individuo:\n" 
			print(j.get_fitness())
			#print(j.get_sigma())
			#print(j.get_cromossom())

		print "Acabou POP!"

	print "Acabou geral!!"
	
	for i in pop:
		print(i.get_fitness())

if __name__ == "__main__":
	main()