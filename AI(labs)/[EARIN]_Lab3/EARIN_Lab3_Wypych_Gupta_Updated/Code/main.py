import random
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import statistics
import sys

from geneticalgorithm import *

# Booth function
def booth_function(x, y):
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2

# These next four functions ensure that the inputs are of the proper type and within the appropriate range
def get_int_input(prompt, minval = -math.inf, maxval = math.inf):
    while True:
        try:
            value = int(input(prompt))
            if (value < minval or value > maxval):
                print("Input is outside of specified range.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_int_inputs(prompt, min_value = -math.inf, max_value = math.inf):
    while True:
        try:
            user_input = input(prompt)
            int_list = [int(i) for i in user_input.split()]
            
            if len(int_list) == 0:
                raise ValueError("Invalid input. No integers inputted.")

            for i in int_list:
                if (i > max_value or i < min_value):
                    raise ValueError("Invalid input. One or more integers inputted are out of range.")

            return int_list
        except ValueError as e:
            print(f"Error: {e}. Please enter valid integers.")

def get_float_inputs(prompt, min_value = -math.inf, max_value = math.inf):
    while True:
        try:
            user_input = input(prompt)
            float_list = [float(i) for i in user_input.split()]
            
            if len(float_list) == 0:
                raise ValueError("Invalid input. No numbers inputted.")

            for i in float_list:
                if (i > max_value or i < min_value):
                    raise ValueError("Invalid input. One or more numbers inputted are out of range.")

            return float_list
        except ValueError as e:
            print(f"Error: {e}. Please enter valid numbers.")

def get_search_space_input(prompt):
    while True:
        try:
            user_input = input(prompt)
            float_list = [float(i) for i in user_input.split()]
            if (len(float_list) != 2):
                print("Invalid input. There must be exactly two values.")
                continue
            elif (float_list[0] > float_list[1]):
                print("Invalid input. The first value cannot be greater than the second value.")
                continue
            return float_list
        except ValueError:
            print("Invalid input. Please enter a valid search space.")

# Returns the nth elements of a nested list
def extract_nested_elements(lst, element):
    return [item[element] for item in lst]

# Runs the generational genetic algorithm for each combination of parameters inputted
def mass_analysis(pop_size_vals, generations_vals, crossover_rate_vals, mutation_rate_vals, mutation_strength_vals, tournament_size_vals, search_space, trials, output_mode):

    times = []
    best_values = []
    best_solutions = []
    average_solutions = []
    median_solutions = []
    best_fitness_histories = []
    average_fitness_histories = []
    median_fitness_histories = []

    for generations in generations_vals:
        for pop_size in pop_size_vals:
            for crossover_rate in crossover_rate_vals:
                for mutation_rate in mutation_rate_vals:
                    for mutation_strength in mutation_strength_vals:
                        for tournament_size in tournament_size_vals:
                            
                            # Run the genetic algorithm a number of times for each combination of parameters inputted, averaging the results 
                            for count in range(trials):
                                start_time = time.time() 
                                best_individual, best_fitness_history, average_fitness_history, median_fitness_history = ga_optimize(pop_size, generations, crossover_rate, mutation_rate, 
                                                                                                                                     mutation_strength, tournament_size, search_space)
                                stop_time = time.time()
                                elapsed_time = stop_time - start_time

                                if (output_mode == 2 or output_mode == 4):
                                    # Plot the best fitness history of each trial on the same graph to show the variation within the same set of parameters
                                    plt.plot(best_fitness_history)

                                times.append(elapsed_time)
                                best_values.append(best_individual)
                                best_solutions.append(best_fitness_history[generations])
                                average_solutions.append(average_fitness_history[generations])
                                median_solutions.append(median_fitness_history[generations])
                                best_fitness_histories.append(best_fitness_history)
                                average_fitness_histories.append(average_fitness_history)
                                median_fitness_histories.append(median_fitness_history)

                            # Average the fitness histories from the same set of parameters
                            for m in range(generations + 1):
                                best_fitness_history[m] = statistics.mean(extract_nested_elements(best_fitness_histories, m))
                                average_fitness_history[m] = statistics.mean(extract_nested_elements(average_fitness_histories, m))
                                median_fitness_history[m] = statistics.mean(extract_nested_elements(median_fitness_histories, m))
                            
                            # Print the parameters
                            print(f"generations: {generations}  pop size: {pop_size}  search space: {search_space[0]}, {search_space[1]}  trials: {trials}")
                            print(f"crossover rate: {crossover_rate}  mutation rate: {mutation_rate}  mutation strength: {mutation_strength}  tournament size: {tournament_size}")

                            # Print the overall data after the final generation for each set of parameters. If there is more than one trial, the standard deviation is included.
                            if (trials > 1):
                                print(f"Best individual: mean x = {statistics.mean(extract_nested_elements(best_values, 0))} y = {statistics.mean(extract_nested_elements(best_values, 1))}"
                                      f", std dev x = {statistics.stdev(extract_nested_elements(best_values, 0))} y = {statistics.stdev(extract_nested_elements(best_values, 1))}")
                                print(f"Best solution: mean f(x, y) = {statistics.mean(best_solutions)}, std dev f(x, y) = {statistics.stdev(best_solutions)}")
                                print(f"Average solution: mean f(x, y) = {statistics.mean(average_solutions)}, std dev f(x, y) = {statistics.stdev(average_solutions)}")
                                print(f"Median solution: mean f(x, y) = {statistics.mean(median_solutions)}, std dev f(x, y) = {statistics.stdev(median_solutions)}")
                                print("Average time of optimization: {:6f} seconds\n".format(statistics.mean(times)))
                            else:
                                print(f"Best individual: mean x = {best_values[0][0]} y = {best_values[0][1]}")
                                print(f"Best solution: mean f(x, y) = {best_solutions[0]}")
                                print(f"Average solution: mean f(x, y) = {average_solutions[0]}")
                                print(f"Median solution: f(x, y) = {median_solutions[0]}")
                                print("Time of optimization: {:6f} seconds\n".format(times[0]))

                            if (output_mode == 2 or output_mode == 4):
                                # Plot the best fitness history from all the trials
                                plt.xlabel("Generation")
                                plt.ylabel("Best Fitness")
                                plt.title(f"Best Fitness per Generation pop: {pop_size} cr: {crossover_rate} mr: {mutation_rate} ms: {mutation_strength} ts: {tournament_size}")
                                plt.show()

                            # Reset lists for next set of parameters
                            times.clear()
                            best_values.clear()
                            best_solutions.clear()
                            average_solutions.clear()
                            median_solutions.clear()
                            best_fitness_history.clear()
                            best_fitness_histories.clear()
                            average_fitness_history.clear()
                            average_fitness_histories.clear()
                            median_fitness_history.clear()
                            median_fitness_histories.clear()


def main():
    
    while True:
        # User input for optimization parameters
        pop_size_vals = get_int_inputs("Enter population sizes to test separated by spaces (min 3): ", 3)
        generations_vals = get_int_inputs("Enter numbers of generations to test separated by spaces (min 1): ", 1)
        crossover_rate_vals = get_float_inputs("Enter crossover rates to test separated by spaces (min 0, max 1): ", 0, 1)
        mutation_rate_vals = get_float_inputs("Enter mutation rates to test separated by spaces (min 0, max 1): ", 0, 1)
        mutation_strength_vals = get_float_inputs("Enter mutation strengths to test separated by spaces (min 0): ", 0)
        tournament_size_vals = get_int_inputs("Enter tournament sizes to test separated by spaces (min 2, max (smallest pop size tested - 1)): ", 2, min(pop_size_vals) - 1)
        search_space = get_search_space_input("Enter the minimum and maximum values (separated by a space) of the search space: ")
        trials = get_int_input("Enter number of trials to perform (min 1): ", 1)

        # User input for data display type
        output_mode = get_int_input("Enter 1 to print numerical results to the console without graphs, \n2 to print results to the console with graphs,"
                                   " \n3 to save the results in a txt file without printing graphs, \nor 4 to save results in a txt file and to print the graphs: ", 1, 4)
        print()


        # Print data in txt file
        if (output_mode > 2):
            original_stdout = sys.stdout

            with open('Lab3data.txt', 'w') as f:
                sys.stdout = f

                mass_analysis(pop_size_vals, generations_vals, crossover_rate_vals, mutation_rate_vals, mutation_strength_vals, tournament_size_vals, search_space, trials, output_mode)

                sys.stdout = original_stdout
        # Print data in console
        else:
            mass_analysis(pop_size_vals, generations_vals, crossover_rate_vals, mutation_rate_vals, mutation_strength_vals, tournament_size_vals, search_space, trials, output_mode)

        # User can choose to perform another analysis with new parameters
        if get_int_input("Enter 1 to perform another test of 0 to exit: ", 0, 1):
            continue
        else:
            break

    

if __name__ == "__main__":
    main()