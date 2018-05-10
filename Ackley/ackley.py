import numpy as np

def ackleyFunc(cromossom):
	value = 0
	c1 = 20
	c2 = 0.2
	c3 = 2*np.pi

	cromossomTemp = cromossom
	root_mean_square = np.sqrt((cromossomTemp * cromossomTemp).mean())
	
	value = -c1*np.exp(-c2*root_mean_square)

	cosine_mean = np.cos(cromossomTemp*c3).mean()

	value = value - np.exp(cosine_mean) + c1 + np.exp(1)

	return value

class EE1:

	def __init__(self):
		self.cromossom = 30*np.random.rand(30,) - 15
		self.sigma = np.random.rand()
		self.fitness = ackleyFunc(self.cromossom)
		self.eps = 1e-12
		self.success = np.zeros(5)
		self.it_number = 0
		self.sigma_parameter = 0.82

	def set_cromossom(self, cromossom):
		self.cromossom = cromossom

	def set_sigma(self, sigma):
		self.sigma = sigma

	def set_fitness(self):
		self.fitness = ackleyFunc(self.cromossom)

	def set_success(self, success):
		self.success = success

	def set_it_number(self, it_number):
		self.it_number = it_number

	def set_success_index(self,index):
		self.success[index] = 1

	def get_sigma(self):
		return self.sigma

	def get_fitness(self):
		return self.fitness

	def get_cromossom(self):
		return self.cromossom

	def get_it_number(self):
		return self.it_number

	def get_success(self):
		return self.success

	def calc_sigma(self):
		newSigma = self.sigma
		if (self.it_number == 5):
			sumSucc = self.success.sum()
			if (sumSucc > 1):
				newSigma = newSigma/self.sigma_parameter
			elif (sumSucc < 1):
				newSigma = newSigma*self.sigma_parameter
		return newSigma

	def calc_mutation(self):
		cromossomTemp = self.cromossom

		newSigma = self.calc_sigma()
		cromossomTemp += newSigma*np.random.randn()

		newMember = EE1()
		newMember.set_cromossom(cromossomTemp)
		newMember.set_sigma(newSigma)
		newMember.set_fitness()

		return newMember

	def substitute(self, newMember):
		if (self.get_fitness() > newMember.get_fitness()):
			if (self.it_number == 5):
				newMember.set_it_number(1)
				newMember.set_success(np.zeros(5))
				newMember.set_success_index(0)
			else:
				newMember.set_success(self.success)
				newMember.set_success_index(self.it_number)
				newMember.set_it_number(self.it_number+1)

			return newMember
		else:
			if (self.it_number == 5):
				self.sigma = newMember.get_sigma()
				self.it_number = 1
				self.success = np.zeros(5)
			else:
				self.it_number = self.it_number + 1
			return self


class EE2:

	def __init__(self):
		self.cromossom = 30*np.random.rand(30,) - 15
		self.sigma = np.random.rand()
		self.fitness = ackleyFunc(self.cromossom)
		self.threshold = 0.5
		self.eps = 1e-12

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
		tal = 10/np.sqrt(30)
		newSigma = self.sigma * np.exp(tal*np.random.randn())
		
		if self.threshold > newSigma:
			newSigma = self.threshold

		return newSigma

	def calc_mutation(self):
		cromossomTemp = self.cromossom
		newSigma = self.calc_sigma()
		cromossomTemp += newSigma

		newMember = EE2()
		newMember.set_cromossom(cromossomTemp)
		newMember.set_sigma(newSigma)
		newMember.set_fitness()

		return newMember

	def substitute(self, newMember):
		if (self.get_fitness() - newMember.get_fitness() > self.eps):
			return newMember
		else:
			return self


def main():

	pop = EE1()
	print "Fitness_Inicial: %lf\n" % (pop.get_fitness())
	#print "Cromossomo_Inicial: "
	print (pop.get_cromossom())
	print "\n"

	for i in range(100):
		new_pop = pop.calc_mutation()
		print "Fitness_Gerado: %lf\n" % (new_pop.get_fitness())
		'''print "Cromossomo_Gerado: "
		print(new_pop.get_cromossom())
		print "\n"'''
		print "Sigma_Gerado: "
		print(new_pop.get_sigma())
		print "\n"
		pop = pop.substitute(new_pop)

		'''print "Sigma_Substituido: "
		print(pop.get_sigma())
		print "\n"'''
		print "Fitness_Final: " 
		print(pop.get_fitness())
		print "\n"
		print(pop.get_success())


if __name__ == "__main__":
    main()
