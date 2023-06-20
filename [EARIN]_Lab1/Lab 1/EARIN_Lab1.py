import numpy as np
import matplotlib.pyplot as plt
import time

# These next two functions ensure that the user's inputs are valid
def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_choice_input(prompt, choices):
    while True:
        choice = input(prompt).lower()
        if choice in choices:
            return choice
        else:
            print(f"Invalid input. Please enter one of the following choices: {', '.join(choices)}")

# The function that is to be minimized. Due to the way arrays are numbered, x[0] corresponds to x_1 in the task (x[1] is x_2, x[2] is x_3).
def f(x, a, b, c):
    return abs(a) * (1 - x[0])**2 + abs(b) * (x[1] - x[0]**2)**2 + abs(c) * (x[2] - x[1]**2)**2

# The gradient of the function, which has been solved analytically
def gradient(x, a, b, c):
    df_dx1 = -2 * abs(a) * (1 - x[0]) + 4 * abs(b) * (x[1] - x[0]**2) * (-2 * x[0])
    df_dx2 = 2 * abs(b) * (x[1] - x[0]**2) + 4 * abs(c) * (x[2] - x[1]**2) * (-2 * x[1])
    df_dx3 = 2 * abs(c) * (x[2] - x[1]**2)
    return np.array([df_dx1, df_dx2, df_dx3])

"""
This function applies the gradient descent method for the selected parameters and hyperparameters. It changes the values of x_1, x_2, and x_3
based on a combination of the gradient at that point and some learning rate. If the gradient and/or the learning parameter are not too high,
the new values of x_1, x_2, and x_3 should be closer to the minimum of the function.
"""
def gradient_descent(a, b, c, x_init, learning_rate, max_iter):

    x = x_init
    # The variable f_values keeps track of the function value at each iteration.
    f_values = []

    for current_iter in range(max_iter):
        grad = gradient(x, a, b, c)
        x = x - learning_rate * grad
        f_values.append(f(x, a, b, c))

    return x, f_values


while True:
    # Get parameters and initial point from user
    a = get_float_input("Enter the value of parameter a: ")
    b = get_float_input("Enter the value of parameter b: ")
    c = get_float_input("Enter the value of parameter c: ")

    choice = get_choice_input("Do you want to specify the initial vector x_init? (y/n): ", ["y", "n"])

    # If user wants to choose the initial vector, they do so here. Otherwise, a random (within the specified range) initial vector is used.
    x_init = None
    if choice == "y":
        x_init = np.array([get_float_input("Enter x1: "), get_float_input("Enter x2: "), get_float_input("Enter x3: ")])
    else:
        x_init = np.random.uniform(-10, 10, 3)
        print(f"Randomly generated initial vector x_init: {x_init}")
   
    # These are the chosen values of the hyperparameters to be tested
    learning_rate = [0.00001, 0.0001, 0.001, 0.01]
    max_iter = [100, 1000, 10000, 100000, 500000]

    # Vary the learning rate
    for lr in learning_rate:
        # Vary the maximum number of iterations
        for mi in max_iter:
            # Minimize using the gradient descent method
            start_time = time.time()
            result, f_values = gradient_descent(a, b, c, x_init, lr, mi)
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Display learning rate and maximum number of iterations
            print(f"Learning rate: {lr}")
            print(f"Maximum number of iterations: {mi}")
            print()  # Add an empty line

            print(f"The found solution x*: {result}")
            print(f"The value of the function f(x*): {f(result, a, b, c)}")
            print(f"Computation time: {elapsed_time:.4f} seconds")
            print()  # Add an empty line

            # Plot the function value at each iteration for all chosen hyperparameters
            if (mi == max_iter[0]):
                plt.plot(range(1, mi+1), f_values)
            else:
                plt.plot(range((mi//10), mi+1), f_values[(mi//10)-1:])
            plt.xlabel('Number of Iterations')
            plt.ylabel('Function Value (f(x*))')
            plt.title(f'Gradient Descent Convergence (Learning Rate: {lr})')
            plt.show()

    recalculate = get_choice_input("Do you want to recalculate with different inputs? (y/n): ", ["y", "n"])
    if recalculate == "n":
        break

