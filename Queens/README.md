# AgentesAutonomos

This project is to solve the 8 queens problem using genetic algorithms.

## Architecture ##

* **Board**: represents a subject, its genotipe is an integer using 24 bits, 
  each 3 bits represent the colunm of a queen, its position represents the row

* **Queens**: the main module. In it we create our population of Boards, 
  evolve it, and generate statistics of covergence

* **Time**: time helper with a start and pause functions to compare algorithims 
  execution times
  
## Play with Project ##

In the queens module there are configurations which you can play with:

* EXEC_NUMBER # number of algorithims execution to create statistics
* ITERATIONS # number of iterations to run for each execution of the algorithim

* POPULATION_SIZE # size of the population

* PARENTS_SELECTION # ROULETTE or BEST_OUT_OF_N

* FIT_TYPE # EXPONENTIAL_FIT or LINEAR_FIT or PARABOLIC_FIT
* GROUP_SIZE # for bestOutOfN is the number of possible parents to chose the final parents for this iteration

* PARENTS_SUBSTITUTION # BEST_SURVIVES (replaces only if the child is better) or ALWAYS_REPLACE (always replace parent with child)

* CROSSOVER_METHOD # CUT_AND_CROSSFILL or CICLE_CROSSOVER

* CROSSOVER_CHANCE # 0-100
* MUTATION_CHANCE # 0-100


**obs.:** The PARENTS_SIZE and CHILDREN_SIZE are broken and must remain 2

Our best result was condiguring:
* PARENTS_SELECTION ROULETTE
* POPULATION_SIZE 7
* PARENTS_SUBSTITUTION BEST_SURVIVES
* MUTATION_CHANCE 100
* CROSSOVER_CHANCE 0
