How to Test Code

1. (Optional) Change values of the available parameters, which can be found near the top of the main and directionalsweep files.
   point_modifier is a multiplier that affect's the AI's decisionmaking when 0 or more stones are detected in 
   a row. display_points determines what information about the point system is shown after each turn. Set this to
   0 to not show any points, 1 to only show the total points calculated for the current boardstate, and 2 to also
   show the number of points each stone contributes to the total score. recursion_depth is how deep the minmax
   algorithm goes (not recommended to increase to more than 2). optimization allows you to choose which minmax
   algorithm to use. They both use alpha beta pruning, but one is much faster than the other. Setting it to True
   makes use of the faster version.
   By default, all the values are set up for proper analysis.
2. Run the code.
3. Choose if you wish to play as X or O.
4. When it is your turn, input a letter and a number separated by a space that correspond to the tile you wish to
   place a stone
5. The AI will automatically move when it is their turn. Sometimes, it may take a while for it to choose a move,
   particularly with the unoptimized algorithm. Afterwards, it displays the number and percentage of pruned branches
   as well as the time it took for the algorithm to find the best move.
6. The move the AI made will be displayed at the top of the map. Additionally, if display_points is kept on at 2,
   the tabulated values of each stone placed and the total points will be listed. This is what the AI "sees" when
   it is trying to find the best move. A positive score is favorable for the AI, whereas a negative score is
   favorable for the human player.
7. The game ends when one player wins.