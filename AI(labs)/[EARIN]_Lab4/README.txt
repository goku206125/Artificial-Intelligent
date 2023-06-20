How to Test Code

1. I found the original data set given for this task on the internet, and the program downloads the data set (so an internet connection is required).
   However, this does mean that you don't need anything but the code to run the program.
2. Run the code.
3. You will be asked to enter some parameters (with minumum and maximum values for each stated).
4. The program will perform each algorithm tested a number of times equal to the number of trials entered.
5. The program will output the plots of the TSNE for each algorithm after each trial. Points belonging to the training set have solid colors. Whereas
   points belonging to the validation are colored with outlines. The inside color represents the predicted value. The outside color represents the actual 
   value if the prediction is incorrect. If the prediction is correct, the outside color is black.
6. To make the program progress, close each graph.
7. After the final trial, the program will output the average computation time, the confusion matrix, and relevent averaged statistical information for each
   algorithm tested. The confusion matrices are normalized to the actual values.
