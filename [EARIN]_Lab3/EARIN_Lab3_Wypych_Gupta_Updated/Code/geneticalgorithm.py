import random
import numpy as np
import math
import statistics

# Booth function
def booth_function(x, y):
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2

# Initialization of an individual using random distribution within specified search space
def create_individual(search_space):
    x = random.uniform(search_space[0], search_space[1])
    y = random.uniform(search_space[0], search_space[1])
    return (x, y)

# Initialization of the population
def create_population(pop_size, search_space):
    return [create_individual(search_space) for _ in range(pop_size)]

# Selection of the best individual based on fitness out of n random individuals in the population
def tournament_selection(population, fitnesses, tournament_size):
    best_fitness = math.inf
    selected_indices = random.sample(range(len(population)), tournament_size)
    for i in selected_indices:
        if (fitnesses[i] < best_fitness):
            best_fitness = fitnesses[i]
            best_index = i
    return best_index

# Reproduction using the two parents that won their tournaments
def crossover(parent1, parent2, crossover_rate, odd = False):
    x1, y1 = parent1
    x2, y2 = parent2
    r = random.random()

    # If the total population size is odd, only one child is created, otherwise two are created. If the random number generated is less than the crossover rate, the children are a mix
    # of their parents. Otherwise. the children are identical to their parents.
    if odd:
        if r < crossover_rate:
            # The child inherits half of each parent's genes. Which half they get is decided randomly, similar to how it is in biologal organisms. In this algorithm, the child is a weighted
            # average of the x and y values of the parents.
            r = random.random()
            cx = (x1 * r) + (x2 * (1 - r))
            cy = (y1 * (1 - r)) + (y2 * r)

            return (cx, cy)
        else:
            return parent1
    else:
        if r < crossover_rate:
            # To ensure twins aren't generated, the weights created by the random number are inverted for the second child.
            r = random.random()
            cx1 = (x1 * r) + (x2 * (1 - r))
            cy1 = (y1 * (1 - r)) + (y2 * r)
            cx2 = (x1 * (1 - r)) + (x2 * r)
            cy2 = (y1 * r) + (y2 * (1 - r))

            return (cx1, cy1), (cx2, cy2)
        else:
            return parent1, parent2

# There is a chance one or both of a child's genes will mutate. This is represented by the variable mutation_rate. A mutation is represented by the x or y value of the individual being
# randomly regenerated within the search space. How strong the mutation is affects how much the gene's original values influence its new values. If mutation_strength is between 0 and 1,
# the new gene is a weighted average of the original gene and the new random gene. If mutation_strength is greater than 1, the new gene value is multiplied by mutation_strength and the
# original gene value contributes nothing.
def mutate(individual, mutation_rate, mutation_strength, search_space):
    x, y = individual
    r = random.random()
    if r < mutation_rate:
        x = (x * min(0, (1 - mutation_strength))) + (random.uniform(search_space[0], search_space[1]) * mutation_strength)
    r = random.random()
    if r < mutation_rate:
        y = (y * min(0, (1 - mutation_strength))) + (random.uniform(search_space[0], search_space[1]) * mutation_strength)
    return (x, y)

# Generational genetic algorithm
def ga_optimize(pop_size, generations, crossover_rate, mutation_rate, mutation_strength, tournament_size, search_space):
    # A new population is initialized each time the algorithm is run.
    population = create_population(pop_size, search_space)

    # The most relevant information to keep track of is the best fitness history, which is the history of the best individual within each generation. In this case, the best individual
    # is the one that best minimizes the Booth Function. The average and mean fitness histories are recorded for deeper analytical purposes.
    best_fitness_history = []
    average_fitness_history = []
    median_fitness_history = []

    # The algorithm is run for n generations, and each includes generation includes a reproduction phase. Since the information of the 1st generation before reproduction and the last generation
    # after reproduction is relevant, at least part of the algorithm is run an additional time after the last generation.
    for gen in range(generations + 1):
        # The fitnesses of each individual are found and the histories are appended.
        fitnesses = [booth_function(x, y) for x, y in population]
        best_fitness_history.append(min(fitnesses))
        average_fitness_history.append(statistics.mean(fitnesses))
        median_fitness_history.append(statistics.median(fitnesses))
        new_population = []

        if (gen == generations):
            break

        # In the generational genetic algorithm, each new generation completely replaces the old one, and the population size always remains the same. First, the each parent is found by
        # hosting a tournament of tournament_size randomly selected individuals. Then, the parents produce offspring, which have a chance of mutating. This repeats until the new generation
        # is filled.
        while len(new_population) < len(population):
            parent1_index = tournament_selection(population, fitnesses, tournament_size)
            # This loop ensures that the two parents are always different
            while True:
                parent2_index = tournament_selection(population, fitnesses, tournament_size)

                if (parent2_index != parent1_index):
                    break
            # If the population size is odd, the last set of parents create only one child.
            if ((len(population) - len(new_population)) != 1):
                offspring1, offspring2 = crossover(population[parent1_index], population[parent2_index], crossover_rate)
                offspring2 = mutate(offspring2, mutation_rate, mutation_strength, search_space)
                new_population.append(offspring2)
            else:
                offspring1 = crossover(population[parent1_index], population[parent2_index], crossover_rate, True)

            offspring1 = mutate(offspring1,  mutation_rate, mutation_strength, search_space)
            new_population.append(offspring1)

        population = new_population

    # Find the x and y values of the best individual after the final generation
    for x, y in population:
        if (booth_function(x, y) == best_fitness_history[generations]):
            best_individual = (x, y)
    

    return best_individual, best_fitness_history, average_fitness_history, median_fitness_history