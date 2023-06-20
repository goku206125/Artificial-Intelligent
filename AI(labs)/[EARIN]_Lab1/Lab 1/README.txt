How to Test Code

1. (Optional) Change the values of the hyperparameters to be tested in the code (learning_rate and
   max_iter), unless the preselected values are OK.
2. Run the code.
3. Choose desired parameters in the console.
4. The program will apply the algorithm for every combination of hyperparameters to be tested.
5. The program will print out the current hyperparameters being tested, the values of x* and f(x*)
   at the final iteration, the computation time, and a graph showing the behavior of f(x*) over
   the most recent set of iterations. A result of NaN means that the learning parameter was too
   high, and the function diverged to infinity.
6. Close each graph to get the program to test the next set of hyperparameters.
7. Once all hyperparameter combinations have been tested, you have the option to rerun the program
   with a different set of parameters.