#peg solitaire
#Fatih Genç 150119905
from copy import copy, deepcopy
import time
import random

#We are holding initial board look and the target matrix.The zero values are used for the outside of the board. And also used for facilitating finding the possible move.
# A = Active P = Passive.   For Ex 1A 2A 3A are full of pegs and the 17P is Empty

initial_matrix = [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                      ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                      ["0", "0", "0", "0", "1A", "2A", "3A", "0", "0", "0", "0"],
                      ["0", "0", "0", "0", "4A", "5A", "6A", "0", "0", "0", "0"],
                      ["0", "0", "7A", "8A", "9A", "10A", "11A", "12A", "13A", "0", "0"],
                      ["0", "0", "14A", "15A", "16A", "17P", "18A", "19A", "20A", "0", "0"],
                      ["0", "0", "21A", "22A", "23A", "24A", "25A", "26A", "27A", "0", "0"],
                      ["0", "0", "0", "0", "28A", "29A", "30A", "0", "0", "0", "0"],
                      ["0", "0", "0", "0", "31A", "32A", "33A", "0", "0", "0", "0"],
                      ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                      ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]
target_matrix = [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                 ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                 ["0", "0", "0", "0", "1P", "2P", "3P", "0", "0", "0", "0"],
                 ["0", "0", "0", "0", "4P", "5P", "6P", "0", "0", "0", "0"],
                 ["0", "0", "7P", "8P", "9P", "10P", "11P", "12P", "13P", "0", "0"],
                 ["0", "0", "14P", "15P", "16P", "17A", "18P", "19P", "20P", "0", "0"],
                 ["0", "0", "21P", "22P", "23P", "24P", "25P", "26P", "27P", "0", "0"],
                 ["0", "0", "0", "0", "28P", "29P", "30P", "0", "0", "0", "0"],
                 ["0", "0", "0", "0", "31P", "32P", "33P", "0", "0", "0", "0"],
                 ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                 ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]

#we add as a parameter the amount of seconds that the function should run before it starts running
def Breadth_First_Search(timelimitsecond,timestring):
    global initial_matrix
    global target_matrix

    #Defining frontier list and the nodes inside of this frontier list. We need to hold Board look, removed_peg_number,the move done in that step
    #For the initial state of this board it holds only the board look.
    frontier_list = [{"board": initial_matrix, "removed_peg_number": "initial_state", "move": "initial_state",
                      "moves": ["initial_state"]}]
    #We need to define our explored list. Also we need to define temp frontier list because we will sort the moves according to the removed peg. So we need to create temporary list.
    #We need to create Sub optimal solutions list and optimal solutions list
    #We created temp matrix for more understandble coding
    explored_list = []
    temp_frontier_list = []
    sub_optimal_solutions = []
    optimal_solutions = []
    temp_matrix = []
    #"is there any possible move" if the node has sub optimal look, we need to differentiate. Therefore we can say if there is no move in the future, is_there_any_possible_move=0
    is_there_any_possible_move = 0
    #We are taking the time when program begins to search. The other variables are also using the syntaxes and for the time limit
    beginning_time = time.time()
    diff_time = 0
    diff_time_with_format = ""
    diff_time_seconds = 0
    ending_time = 0
    #If the given time ends our program return time_error=1. Thus our program will stop running
    time_error = 0
    #memory error counter if it is 1, memory error happened
    memory_error=0
    #check ist optimal founded or not
    Optimal_Found=0


    #check for memory error
    try:
        # Beginning of our search method
        # If the first item of the frontier list look not same with the target matrix, program continue to search or if there is no item in frontier list, that means there is no more node to search.
        # And also if time error is 1 that means we are out of time. No need to continue searching
        while( Optimal_Found==0 and len(frontier_list) != 0 and time_error==0):
            #First we took the board matrix to matrix variable and we created past moves list. Because we are holding past move information of every node
            matrix=frontier_list[0]["board"]
            past_moves=[]
            #We are holding the moves and appending because we will add the child nodes moves to parent node moves
            for i in frontier_list[0]["moves"]:
                past_moves.append(i)
            #If there is any possible move according to the First item of frontier list, we are finding in this part
            #We are taking values line by line
            for item in matrix:
                #We are taking values for each peg on this board
                for element in item:
                    #Check whether inside of this element indicate 'P' or not. If yes that means empty.Then we're going to start thinking if we can move the pegs around here.
                    if (element.find("P")!=-1):
                        #We save the pegs on the left, on the right, on the top and bottom

                        first_upper=matrix[matrix.index(item) - 1][item.index(element)]
                        second_upper=matrix[matrix.index(item) - 2][item.index(element)]

                        first_bottom=matrix[matrix.index(item)+1][item.index(element)]
                        second_bottom=matrix[matrix.index(item)+2][item.index(element)]

                        first_left=matrix[matrix.index(item)][item.index(element)-1]
                        second_left=matrix[matrix.index(item)][item.index(element)-2]

                        first_right=matrix[matrix.index(item)][item.index(element)+1]
                        second_right=matrix[matrix.index(item)][item.index(element)+2]

                        #Enter here if the two upper pegs of the empty space are not empty
                        if(first_upper.find("A")!=-1 and second_upper.find("A")!=-1):
                            #If it came here, we set the value of our if is there any possible move variable to 1, since our parent node will not be a sub-optimal solution.
                            #Here we have recorded the board image that will be formed after the move using the new matrix function.
                            is_there_any_possible_move = 1
                            temp_matrix=New_Matrix("up", matrix, matrix.index(item), item.index(element), element)
                            #We saved the pegs
                            removed_peg=first_upper[0:first_upper.find("A")]
                            moved_peg=second_upper[0:second_upper.find("A")]
                            target_peg=matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            #Appending the new move to the parent's past moves
                            past_moves.append(moved_peg + "->" + target_peg)
                            #Put the information inside the temp frontier list
                            temp_frontier_list.append({"board":temp_matrix, "removed_peg_number":removed_peg,"move":moved_peg+"->"+target_peg,"moves":[]})
                            #Append the past moves inside the last element added to the temp frontier list
                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            #We need to pop last move because we dont want to change parent's past moves. There can be three more children
                            past_moves.pop()

                        #Enter here if the two bottom pegs of the empty space are not empty
                        if(first_bottom.find("A")!=-1 and second_bottom.find("A")!=-1):
                            # If it came here, we set the value of our if is there any possible move variable to 1, since our parent node will not be a sub-optimal solution.
                            # Here we have recorded the board image that will be formed after the move using the new matrix function.
                            is_there_any_possible_move = 1
                            temp_matrix=New_Matrix("bottom", matrix, matrix.index(item), item.index(element), element)
                            # We saved the pegs
                            removed_peg=first_bottom[0:first_bottom.find("A")]
                            moved_peg = second_bottom[0:second_bottom.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            #Appending the new move to the parent's past moves
                            past_moves.append(moved_peg + "->" + target_peg)
                            #Put the information inside the temp frontier list
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg, "move": moved_peg + "->" + target_peg,
                                 "moves": []})
                            #Append the past moves inside the last element added to the temp frontier list
                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            #We need to pop last move because we dont want to change parent's past moves. There can be more children
                            past_moves.pop()

                        # Enter here if the two left pegs of the empty space are not empty
                        if(first_left.find("A")!=-1 and second_left.find("A")!=-1):
                            # If it came here, we set the value of our if is there any possible move variable to 1, since our parent node will not be a sub-optimal solution.
                            # Here we have recorded the board image that will be formed after the move using the new matrix function.
                            is_there_any_possible_move = 1
                            temp_matrix=New_Matrix("left",matrix,matrix.index(item),item.index(element), element)
                            # We saved the pegs
                            removed_peg = first_left[0:first_left.find("A")]
                            moved_peg = second_left[0:second_left.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            # Appending the new move to the parent's past moves
                            past_moves.append(moved_peg + "->" + target_peg)
                            # Put the information inside the temp frontier list
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg, "move": moved_peg + "->" + target_peg,
                                 "moves": []})
                            # Append the past moves inside the last element added to the temp frontier list
                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            # We need to pop last move because we dont want to change parent's past moves. There can be more children
                            past_moves.pop()

                        # Enter here if the two right pegs of the empty space are not empty
                        if (first_right.find("A")!=-1 and second_right.find("A")!=-1):
                            # If it came here, we set the value of our if is there any possible move variable to 1, since our parent node will not be a sub-optimal solution.
                            # Here we have recorded the board image that will be formed after the move using the new matrix function.
                            is_there_any_possible_move = 1
                            temp_matrix=New_Matrix("right", matrix, matrix.index(item), item.index(element), element)
                            # We saved the pegs
                            removed_peg = first_right[0:first_right.find("A")]
                            moved_peg = second_right[0:first_right.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            # Appending the new move to the parent's past moves
                            past_moves.append(moved_peg + "->" + target_peg)
                            # Put the information inside the temp frontier list
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg, "move": moved_peg + "->" + target_peg,
                                 "moves": []})
                            # Append the past moves inside the last element added to the temp frontier list
                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            # We need to pop last move because we dont want to change parent's past moves. There can be three more children
                            past_moves.pop()

    #while loop ends here

            # if there is no possible move
            if (is_there_any_possible_move==0):
                #if matrix same with the target matrix enter
                if (matrix==target_matrix):
                    #if optimal solutions list has no element then append
                    if(len(optimal_solutions)==0):
                        Optimal_Found=1
                        optimal_solutions.append(frontier_list[0])
                #if matrix not same with the target matrix enter
                else:
                    #if sub optimal solutions have no element append immediately
                    if(len(sub_optimal_solutions)==0):
                        sub_optimal_solutions.append(frontier_list[0])
                    #if sub optimal solutions have any element then check the remaining peg numbers
                    else:
                        old_remaining_peg_number = 32 - (len(sub_optimal_solutions[0]["moves"]) - 1)
                        new_remaining_peg_number = 32 - (len(frontier_list[0]["moves"]) - 1)
                        # if new node has less remaining peg number than old then change it
                        if(new_remaining_peg_number<old_remaining_peg_number):
                            sub_optimal_solutions.pop(0)
                            sub_optimal_solutions.append(frontier_list[0])

            #this part related to the removed peg's number
            #we put the possible moves into the temp frontier list and now we will sort according to the removed peg number
            removed_peg_sorted = sorted(temp_frontier_list, key=lambda k: (int(k['removed_peg_number'])))
            #now we are appending the sorted values to the frontier list by order
            for i in removed_peg_sorted:
                frontier_list.append(i)
            #clear operations
            removed_peg_sorted.clear()
            temp_frontier_list.clear()
            #we are moving the frontier list element to the explored list because we used it
            explored_list.append(frontier_list[0])
            #we delete the element we use from the frontier list
            frontier_list.pop(0)
            #reseting possible move counter
            is_there_any_possible_move = 0
            #checking time
            ending_time = time.time()
            diff_time = ending_time - beginning_time
            diff_time_with_format = time.strftime("%H:%M:%S", time.gmtime(diff_time))
            diff_time_seconds = time_operations(diff_time_with_format)

            #if elapsed time is greater than or equal to our time limit enter here
            if (timelimitsecond - diff_time_seconds <= 0):
                #we dont want to go through the loop again therefore we are making our time error variable 1
                time_error = 1
    except MemoryError:
        memory_error=1
    #In this part, we have finished the search method and now we go to the printing part of the information we have obtained.
    #initial state peg number is 32
    total_peg = 32
    remaining_peg = 0
    if (memory_error==1):
        print("Memory error has occurred. results found before the error occurred")
    else:
        print("No memory error occurred.")
    #if there is an optimal solution enter
    if (len(optimal_solutions) > 0):
        print("Optimum solution found.")
        print(optimal_solutions[0]["moves"])
        print_board(optimal_solutions[0]["board"])
    #if there is no optimal solution enter
    else:
        if(memory_error==1):
            print("Error occurrence time -> " + time.strftime("%H:%M:%S", time.gmtime(diff_time)))
        print("No optimal solution found – Time Limit -> " + timestring)
        #if there is a sub optimal solution enter
        if (len(sub_optimal_solutions) > 0):
            #finding remainin peg count
            remaining_peg = total_peg - (len(sub_optimal_solutions[0]["moves"]) - 1)
            print("Sub-optimum Solution Found with " + str(remaining_peg) + " remaining pegs")
            print(sub_optimal_solutions[0]["moves"])
            print_board(sub_optimal_solutions[0]["board"])
        # if there is no sub optimal solution enter
        else:
            print("sub optimal solution not found")

    print("Time spent -> ", time.strftime("%H:%M:%S", time.gmtime(diff_time)))
    # we took the number of element inside the explored list.Thus we obtain the expanded node during the search
    print("The number of nodes expanded during the search.")
    print(len(explored_list))
    # for finding max stored node in memory we can add len of explored list to the len of frontier list
    print("Max number of nodes stored in the memory during the search.")
    print(len(explored_list) + len(frontier_list))

#we add as a parameter the amount of seconds that the function should run before it starts running
def Depth_First_Search(timelimitsecond,timestring):
    global initial_matrix
    global target_matrix

    # Defining frontier list and the nodes inside of this frontier list. We need to hold Board look, removed_peg_number,the move done in that step
    # For the initial state of this board it holds only the board look.
    frontier_list = [{"board": initial_matrix, "removed_peg_number": "initial_state", "move": "initial_state",
                      "moves": ["initial_state"]}]
    # We need to define our explored list. Also we need to define temp frontier list because we will sort the moves according to the removed peg. So we need to create temporary list.
    # We need to create Sub optimal solutions list and optimal solutions list
    # We created temp matrix for more understandable coding
    explored_list = []
    sub_optimal_solutions=[]
    optimal_solutions=[]
    temp_frontier_list = []
    # "is there any possible move" if the node has sub optimal look, we need to differentiate. Therefore we can say if there is no move in the future, is_there_any_possible_move=0
    is_there_any_possible_move=0
    # We are taking the time when program begins to search. The other variables are also using the syntaxes and for the time limit
    beginning_time = time.time()
    diff_time=0
    diff_time_with_format=""
    diff_time_seconds=0
    ending_time=0
    # If the given time ends our program return time_error=1. Thus our program will stop running
    time_error=0
    memory_error=0
    Optimal_Found=0
    #check for memory error
    try:
    # Beginning of our search method
    # If the first item of the frontier list look not same with the target matrix, program continue to search or if there is no item in frontier list, that means there is no more node to search.
    # And also if time error is 1 that means we are out of time. No need to continue searching
        while (Optimal_Found==0 and len(frontier_list) != 0 and time_error==0):

            # First we took the board matrix to matrix variable and we created past moves list. Because we are holding past move information of every node
            matrix = frontier_list[0]["board"]
            past_moves = []



            # We are holding the moves and appending because we will add the child nodes moves to parent node moves
            for i in frontier_list[0]["moves"]:
                past_moves.append(i)

            # If there is any possible move according to the First item of frontier list, we are finding in this part
            # We are taking values line by line
            for item in matrix:
                # We are taking values for each peg on this board
                for element in item:
                    # Check whether inside of this element indicate 'P' or not. If yes that means empty.Then we're going to start thinking if we can move the pegs around here.
                    if (element.find("P") != -1):
                        # We save the pegs on the left, on the right, on the top and bottom
                        first_upper = matrix[matrix.index(item) - 1][item.index(element)]
                        second_upper = matrix[matrix.index(item) - 2][item.index(element)]

                        first_bottom = matrix[matrix.index(item) + 1][item.index(element)]
                        second_bottom = matrix[matrix.index(item) + 2][item.index(element)]

                        first_left = matrix[matrix.index(item)][item.index(element) - 1]
                        second_left = matrix[matrix.index(item)][item.index(element) - 2]

                        first_right = matrix[matrix.index(item)][item.index(element) + 1]
                        second_right = matrix[matrix.index(item)][item.index(element) + 2]

                        # Enter here if the two upper pegs of the empty space are not empty
                        if (first_upper.find("A") != -1 and second_upper.find("A") != -1):
                            # If it came here, we set the value of our if is there any possible move variable to 1, since our parent node will not be a sub-optimal solution.
                            # Here we have recorded the board image that will be formed after the move using the new matrix function.
                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("up", matrix, matrix.index(item), item.index(element), element)
                            # we saved the pegs
                            removed_peg = first_upper[0:first_upper.find("A")]
                            moved_peg = second_upper[0:second_upper.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            # Appending the new move to the parent's past moves
                            past_moves.append(moved_peg + "->" + target_peg)
                            # Put the information inside the temp frontier list
                            temp_frontier_list.append({"board": temp_matrix, "removed_peg_number": removed_peg,
                                                       "move": moved_peg + "->" + target_peg, "moves": []})
                            # Append the past moves inside the last element added to the temp frontier list
                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            # We need to pop last move because we dont want to change parent's past moves. There can be three more children
                            past_moves.pop()

                        # Enter here if the two bottom pegs of the empty space are not empty
                        if (first_bottom.find("A") != -1 and second_bottom.find("A") != -1):
                            # If it came here, we set the value of our if is there any possible move variable to 1, since our parent node will not be a sub-optimal solution.
                            # Here we have recorded the board image that will be formed after the move using the new matrix function.
                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("bottom", matrix, matrix.index(item), item.index(element), element)
                            # we saved the pegs
                            removed_peg = first_bottom[0:first_bottom.find("A")]
                            moved_peg = second_bottom[0:second_bottom.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            # Appending the new move to the parent's past moves
                            past_moves.append(moved_peg + "->" + target_peg)
                            # Put the information inside the temp frontier list
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg,
                                 "move": moved_peg + "->" + target_peg,
                                 "moves": []})
                            # Append the past moves inside the last element added to the temp frontier list
                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            # We need to pop last move because we dont want to change parent's past moves. There can be more children
                            past_moves.pop()

                        # Enter here if the two left pegs of the empty space are not empty
                        if (first_left.find("A") != -1 and second_left.find("A") != -1):
                            # If it came here, we set the value of our if is there any possible move variable to 1, since our parent node will not be a sub-optimal solution.
                            # Here we have recorded the board image that will be formed after the move using the new matrix function.
                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("left", matrix, matrix.index(item), item.index(element), element)
                            # we saved the pegs
                            removed_peg = first_left[0:first_left.find("A")]
                            moved_peg = second_left[0:second_left.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            # Appending the new move to the parent's past moves
                            past_moves.append(moved_peg + "->" + target_peg)
                            # Put the information inside the temp frontier list
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg,
                                 "move": moved_peg + "->" + target_peg,
                                 "moves": [], "node_number": 0,"level":0})
                            # Append the past moves inside the last element added to the temp frontier list
                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            # We need to pop last move because we dont want to change parent's past moves. There can be more children
                            past_moves.pop()

                        # Enter here if the two right pegs of the empty space are not empty
                        if (first_right.find("A") != -1 and second_right.find("A") != -1):
                            # If it came here, we set the value of our if is there any possible move variable to 1, since our parent node will not be a sub-optimal solution.
                            # Here we have recorded the board image that will be formed after the move using the new matrix function.
                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("right", matrix, matrix.index(item), item.index(element), element)
                            # we saved the pegs
                            removed_peg = first_right[0:first_right.find("A")]
                            moved_peg = second_right[0:first_right.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            # Appending the new move to the parent's past moves
                            past_moves.append(moved_peg + "->" + target_peg)
                            # Put the information inside the temp frontier list
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg,
                                 "move": moved_peg + "->" + target_peg,
                                 "moves": []})
                            # Append the past moves inside the last element added to the temp frontier list
                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            # We need to pop last move because we dont want to change parent's past moves. There can be more children
                            past_moves.pop()
            #if there is any no possible move enter
            if (is_there_any_possible_move==0):
                #if matrix same with the target matrix enter
                if (matrix==target_matrix):
                    #if there is no optimal solution enter and append to the list
                    if(len(optimal_solutions)==0):
                        Optimal_Found=1
                        optimal_solutions.append(frontier_list[0])
                #if matrix not same with the target matrix enter
                else:
                    #if there is no sub optimal solution, append to the list
                    if(len(sub_optimal_solutions)==0):
                        sub_optimal_solutions.append(frontier_list[0])
                    #if there is no sub optimal solution enter
                    else:
                        #check the previous remaining peg number and the new
                        old_remaining_peg_number = 32 - (len(sub_optimal_solutions[0]["moves"]) - 1)
                        new_remaining_peg_number = 32 - (len(frontier_list[0]["moves"]) - 1)
                        #if new one less than old one, change it
                        if(new_remaining_peg_number<old_remaining_peg_number):
                            sub_optimal_solutions.pop(0)
                            sub_optimal_solutions.append(frontier_list[0])

            # this part related to the removed peg's number
            # we put the possible moves into the temp frontier list and now we will sort according to the removed peg number
            removed_peg_sorted = sorted(temp_frontier_list, key=lambda k: (int(k['removed_peg_number'])))
            # we explored first element of frontier list. Therefore add to the explored and pop from frontier
            explored_list.append(frontier_list[0])
            frontier_list.pop(0)
            #this part adds the children sorted according to the removed peg numbers to the beginning of the frontier list in order.
            position=0
            for i in removed_peg_sorted:
                frontier_list.insert(position,i)
                position += 1
            #clear operations
            temp_frontier_list.clear()
            #reset is there any possible move counter
            is_there_any_possible_move=0
            #time operations
            ending_time = time.time()
            diff_time=ending_time-beginning_time
            diff_time_with_format=time.strftime("%H:%M:%S", time.gmtime(diff_time))
            diff_time_seconds=time_operations(diff_time_with_format)

            if (timelimitsecond-diff_time_seconds<=0):
                #raise a time error if the time limit less than the elapsed time
                time_error=1
    except MemoryError:
        #memory error counter
        memory_error=1


    total_peg=32
    remaining_peg=0
    #check if there is memory error or not
    if (memory_error==1):
        print("Memory error has occurred. results found before the error occurred")
    else:
        print("No memory error occurred.")
    #if there is optimal solution then print
    if (len(optimal_solutions)>0):
        print("Optimum solution found.")
        print(optimal_solutions[0]["moves"])
        print_board(optimal_solutions[0]["board"])
    #if sub optimal solution not found
    else:
        if (memory_error == 1):
            print("Error occurrence time -> " + time.strftime("%H:%M:%S", time.gmtime(diff_time)))
        print("No optimal solution found – Time Limit -> "+ timestring)
        #if there is sub optimal solution,print
        if(len(sub_optimal_solutions)>0):
            remaining_peg = total_peg - (len(sub_optimal_solutions[0]["moves"]) - 1)
            print("Sub-optimum Solution Found with "+str(remaining_peg)+" remaining pegs")
            print(sub_optimal_solutions[0]["moves"])
            print_board(sub_optimal_solutions[0]["board"])
        #if there is no sub optimal solution, print
        else:
            print("sub optimal solution not found")
    print("Time spent -> ",time.strftime("%H:%M:%S", time.gmtime(diff_time)))
    #For printing number of node expanded we use len of explored list
    print("The number of nodes expanded during the search.")
    print(len(explored_list))
    #For printing max number of node stored in the memory we use len of explored list + len of frontier list
    print("Max number of nodes stored in the memory during the search.")
    print(len(explored_list) + len(frontier_list))

#we add as a parameter the amount of seconds that the function should run before it starts running
#this part same as the Depth_First_Search but only difference is removed_peg_sorted list recreated according to the random selection line 651-654 is the only difference
def Depth_First_Search_Random_Selection(timelimitsecond,timestring):
    global initial_matrix
    global target_matrix

    frontier_list = [{"board": initial_matrix, "removed_peg_number": "initial_state", "move": "initial_state",
                      "moves": ["initial_state"]}]
    explored_list = []
    sub_optimal_solutions = []
    optimal_solutions = []
    temp_frontier_list = []
    is_there_any_possible_move = 0
    beginning_time = time.time()
    diff_time = 0
    diff_time_with_format = ""
    diff_time_seconds = 0
    ending_time = 0
    time_error = 0
    memory_error=0
    Optimal_Found=0

    try:
        while (Optimal_Found==0 and len(frontier_list) != 0 and time_error == 0):

            matrix = frontier_list[0]["board"]
            past_moves = []


            for i in frontier_list[0]["moves"]:
                past_moves.append(i)

            for item in matrix:
                for element in item:
                    if (element.find("P") != -1):

                        first_upper = matrix[matrix.index(item) - 1][item.index(element)]
                        second_upper = matrix[matrix.index(item) - 2][item.index(element)]

                        first_bottom = matrix[matrix.index(item) + 1][item.index(element)]
                        second_bottom = matrix[matrix.index(item) + 2][item.index(element)]

                        first_left = matrix[matrix.index(item)][item.index(element) - 1]
                        second_left = matrix[matrix.index(item)][item.index(element) - 2]

                        first_right = matrix[matrix.index(item)][item.index(element) + 1]
                        second_right = matrix[matrix.index(item)][item.index(element) + 2]

                        if (first_upper.find("A") != -1 and second_upper.find("A") != -1):

                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("up", matrix, matrix.index(item), item.index(element), element)
                            removed_peg = first_upper[0:first_upper.find("A")]
                            moved_peg = second_upper[0:second_upper.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            past_moves.append(moved_peg + "->" + target_peg)
                            temp_frontier_list.append({"board": temp_matrix, "removed_peg_number": removed_peg,
                                                       "move": moved_peg + "->" + target_peg, "moves": []})
                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            past_moves.pop()

                        if (first_bottom.find("A") != -1 and second_bottom.find("A") != -1):

                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("bottom", matrix, matrix.index(item), item.index(element), element)
                            removed_peg = first_bottom[0:first_bottom.find("A")]
                            moved_peg = second_bottom[0:second_bottom.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            past_moves.append(moved_peg + "->" + target_peg)
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg,
                                 "move": moved_peg + "->" + target_peg,
                                 "moves": []})

                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            past_moves.pop()

                        if (first_left.find("A") != -1 and second_left.find("A") != -1):

                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("left", matrix, matrix.index(item), item.index(element), element)
                            removed_peg = first_left[0:first_left.find("A")]
                            moved_peg = second_left[0:second_left.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            past_moves.append(moved_peg + "->" + target_peg)
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg,
                                 "move": moved_peg + "->" + target_peg,
                                 "moves": []})

                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            past_moves.pop()

                        if (first_right.find("A") != -1 and second_right.find("A") != -1):
                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("right", matrix, matrix.index(item), item.index(element), element)
                            removed_peg = first_right[0:first_right.find("A")]
                            moved_peg = second_right[0:first_right.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            past_moves.append(moved_peg + "->" + target_peg)
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg,
                                 "move": moved_peg + "->" + target_peg,
                                 "moves": [], "node_number": 0, "level": 0})

                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            past_moves.pop()

            if (is_there_any_possible_move == 0):
                if (matrix == target_matrix):
                    if (len(optimal_solutions) == 0):
                        Optimal_Found=1
                        optimal_solutions.append(frontier_list[0])

                else:
                    if (len(sub_optimal_solutions) == 0):
                        sub_optimal_solutions.append(frontier_list[0])
                    else:
                        old_remaining_peg_number = 32 - (len(sub_optimal_solutions[0]["moves"]) - 1)
                        new_remaining_peg_number = 32 - (len(frontier_list[0]["moves"]) - 1)
                        if (new_remaining_peg_number < old_remaining_peg_number):
                            sub_optimal_solutions.pop(0)
                            sub_optimal_solutions.append(frontier_list[0])
            #make the possible moves sorted
            removed_peg_sorted = sorted(temp_frontier_list, key=lambda k: (int(k['removed_peg_number'])))
            #then mix the list.
            random.shuffle(removed_peg_sorted)
            explored_list.append(frontier_list[0])
            frontier_list.pop(0)
            position = 0
            for i in removed_peg_sorted:
                frontier_list.insert(position, i)
                position += 1
            temp_frontier_list.clear()

            is_there_any_possible_move = 0
            ending_time = time.time()
            diff_time = ending_time - beginning_time
            diff_time_with_format = time.strftime("%H:%M:%S", time.gmtime(diff_time))
            diff_time_seconds = time_operations(diff_time_with_format)


            if (timelimitsecond - diff_time_seconds <= 0):

                time_error = 1


    except MemoryError:
        memory_error=1

    total_peg = 32
    remaining_peg = 0
    if (memory_error==1):
        print("Memory error has occurred. results found before the error occurred")
    else:
        print("No memory error occurred.")
    if (len(optimal_solutions) > 0):
        print("Optimum solution found.")
        print(optimal_solutions[0]["moves"])
        print_board(optimal_solutions[0]["board"])
    else:
        if (memory_error == 1):
            print("Error occurrence time -> " + time.strftime("%H:%M:%S", time.gmtime(diff_time)))
        print("No optimal solution found – Time Limit -> " + timestring)
        if (len(sub_optimal_solutions) > 0):
            remaining_peg = total_peg - (len(sub_optimal_solutions[0]["moves"]) - 1)
            print("Sub-optimum Solution Found with " + str(remaining_peg) + " remaining pegs")
            print(sub_optimal_solutions[0]["moves"])
            print_board(sub_optimal_solutions[0]["board"])

        else:
            print("sub optimal solution not found")
    print("Time spent -> ", time.strftime("%H:%M:%S", time.gmtime(diff_time)))
    print("The number of nodes expanded during the search.")
    print(len(explored_list))
    print("Max number of nodes stored in the memory during the search.")
    print(len(explored_list) + len(frontier_list))

#we add as a parameter the amount of seconds that the function should run before it starts running
def Iterative_Depth_First_Search(timelimitsecond,timestring):

    global initial_matrix
    global target_matrix

    #Defining variables
    frontier_list = [{"board": initial_matrix, "removed_peg_number": "initial_state", "move": "initial_state",
                      "moves": ["initial_state"]}]
    explored_list = []
    Explored_List_Item_Count=0
    Max_Memory_Number=0
    Max_Memory_Temp_Number=0
    sub_optimal_solutions = []
    optimal_solutions = []
    temp_frontier_list = []
    is_there_any_possible_move = 0
    #time variables
    beginning_time = time.time()
    diff_time = 0
    diff_time_with_format = ""
    diff_time_seconds = 0
    ending_time = 0
    #if we pass the time limit then return time error.
    time_error = 0
    #level counter
    iterative_counter=0
    #For memory error
    memory_error=0
    #check whether optimal solution found or not
    optimal_solution_found=0
    #this loop makes it progress level by level
    try:
        while(iterative_counter<=32 and time_error==0 and optimal_solution_found==0):
            if(len(frontier_list)==0):
                frontier_list.append({"board": initial_matrix, "removed_peg_number": "initial_state", "move": "initial_state",
                          "moves": ["initial_state"]})
            iterative_counter += 1
            #this loop performs a depth first search for the specified level limit
            while (len(frontier_list) != 0 and time_error==0 and optimal_solution_found == 0 ):

                #appending past moves
                matrix = frontier_list[0]["board"]
                past_moves = []

                for i in frontier_list[0]["moves"]:
                    past_moves.append(i)

                #find possible moves to add to frontier
                #same code with the depth first search method
                for item in matrix:
                    for element in item:
                        if (element.find("P") != -1):

                            first_upper = matrix[matrix.index(item) - 1][item.index(element)]
                            second_upper = matrix[matrix.index(item) - 2][item.index(element)]

                            first_bottom = matrix[matrix.index(item) + 1][item.index(element)]
                            second_bottom = matrix[matrix.index(item) + 2][item.index(element)]

                            first_left = matrix[matrix.index(item)][item.index(element) - 1]
                            second_left = matrix[matrix.index(item)][item.index(element) - 2]

                            first_right = matrix[matrix.index(item)][item.index(element) + 1]
                            second_right = matrix[matrix.index(item)][item.index(element) + 2]

                            if (first_upper.find("A") != -1 and second_upper.find("A") != -1):

                                is_there_any_possible_move = 1
                                temp_matrix = New_Matrix("up", matrix, matrix.index(item), item.index(element), element)
                                removed_peg = first_upper[0:first_upper.find("A")]
                                moved_peg = second_upper[0:second_upper.find("A")]
                                target_peg = matrix[matrix.index(item)][item.index(element)]
                                target_peg = target_peg[0:-1]
                                past_moves.append(moved_peg + "->" + target_peg)
                                temp_frontier_list.append({"board": temp_matrix, "removed_peg_number": removed_peg,
                                                           "move": moved_peg + "->" + target_peg, "moves": []})

                                for i in past_moves:
                                    temp_frontier_list[-1]["moves"].append(i)
                                past_moves.pop()


                            if (first_bottom.find("A") != -1 and second_bottom.find("A") != -1):

                                is_there_any_possible_move = 1
                                temp_matrix = New_Matrix("bottom", matrix, matrix.index(item), item.index(element), element)
                                removed_peg = first_bottom[0:first_bottom.find("A")]
                                moved_peg = second_bottom[0:second_bottom.find("A")]
                                target_peg = matrix[matrix.index(item)][item.index(element)]
                                target_peg = target_peg[0:-1]
                                past_moves.append(moved_peg + "->" + target_peg)
                                temp_frontier_list.append(
                                    {"board": temp_matrix, "removed_peg_number": removed_peg,
                                     "move": moved_peg + "->" + target_peg,
                                     "moves": []})

                                for i in past_moves:
                                    temp_frontier_list[-1]["moves"].append(i)
                                past_moves.pop()

                            if (first_left.find("A") != -1 and second_left.find("A") != -1):

                                is_there_any_possible_move = 1
                                temp_matrix = New_Matrix("left", matrix, matrix.index(item), item.index(element), element)
                                removed_peg = first_left[0:first_left.find("A")]
                                moved_peg = second_left[0:second_left.find("A")]
                                target_peg = matrix[matrix.index(item)][item.index(element)]
                                target_peg = target_peg[0:-1]
                                past_moves.append(moved_peg + "->" + target_peg)
                                temp_frontier_list.append(
                                    {"board": temp_matrix, "removed_peg_number": removed_peg,
                                     "move": moved_peg + "->" + target_peg,
                                     "moves": []})

                                for i in past_moves:
                                    temp_frontier_list[-1]["moves"].append(i)
                                past_moves.pop()

                            if (first_right.find("A") != -1 and second_right.find("A") != -1):
                                is_there_any_possible_move = 1
                                temp_matrix = New_Matrix("right", matrix, matrix.index(item), item.index(element), element)
                                removed_peg = first_right[0:first_right.find("A")]
                                moved_peg = second_right[0:first_right.find("A")]
                                target_peg = matrix[matrix.index(item)][item.index(element)]
                                target_peg = target_peg[0:-1]
                                past_moves.append(moved_peg + "->" + target_peg)
                                temp_frontier_list.append(
                                    {"board": temp_matrix, "removed_peg_number": removed_peg,
                                     "move": moved_peg + "->" + target_peg,
                                     "moves": []})

                                for i in past_moves:
                                    temp_frontier_list[-1]["moves"].append(i)
                                past_moves.pop()

                #check is there any possible move
                if (is_there_any_possible_move == 0):
                    if (matrix == target_matrix):
                        #if optimal solution found, change counter and append to the list
                        if (len(optimal_solutions) == 0):
                            optimal_solution_found=1
                            optimal_solutions.append(frontier_list[0])
                    #if solution is not optimal then it would be sub optimal. According to remaining peg number append to the list or not
                    else:
                        if (len(sub_optimal_solutions) == 0):
                            sub_optimal_solutions.append(frontier_list[0])
                        else:
                            old_remaining_peg_number = 32 - (len(sub_optimal_solutions[0]["moves"]) - 1)
                            new_remaining_peg_number = 32 - (len(frontier_list[0]["moves"]) - 1)
                            if (new_remaining_peg_number < old_remaining_peg_number):
                                sub_optimal_solutions.pop(0)
                                sub_optimal_solutions.append(frontier_list[0])

                removed_peg_sorted = sorted(temp_frontier_list, key=lambda k: (int(k['removed_peg_number'])))
                #if there is no possible move for the parent,just add the parent to the explored list and pop from the frontier list.
                if (len(removed_peg_sorted)==0):

                    explored_list.append(frontier_list[0])
                    frontier_list.pop(0)
                    # Counting the Expanded nodes and holding the data of max memory temp
                    Explored_List_Item_Count += 1
                    if (Max_Memory_Temp_Number < (len(frontier_list) + len(explored_list))):
                        Max_Memory_Temp_Number = len(frontier_list) + len(explored_list)
                    #reset operations
                    temp_frontier_list.clear()
                    is_there_any_possible_move = 0
                    #time operations
                    ending_time = time.time()
                    diff_time = ending_time - beginning_time
                    diff_time_with_format = time.strftime("%H:%M:%S", time.gmtime(diff_time))
                    diff_time_seconds = time_operations(diff_time_with_format)
                    #time check
                    if (timelimitsecond - diff_time_seconds <= 0):
                        time_error = 1
                #if there are possible moves,check the possible moves lenght.
                else:
                    #if iterative counter bigger or equal to the lenght,append to the explored and pop from the frontier
                    if (iterative_counter>=len(removed_peg_sorted[0]["moves"])):
                        explored_list.append(frontier_list[0])
                        frontier_list.pop(0)
                        #add to the frontier
                        position = 0
                        for i in removed_peg_sorted:
                            frontier_list.insert(position, i)
                            position += 1
                        #Counting the Expanded nodes and holding the data of max memory temp
                        Explored_List_Item_Count += 1
                        if (Max_Memory_Temp_Number<(len(frontier_list)+len(explored_list))):
                            Max_Memory_Temp_Number = len(frontier_list)+len(explored_list)
                        #reset operations
                        temp_frontier_list.clear()
                        is_there_any_possible_move = 0
                        #time operations
                        ending_time = time.time()
                        diff_time = ending_time - beginning_time
                        diff_time_with_format = time.strftime("%H:%M:%S", time.gmtime(diff_time))
                        diff_time_seconds = time_operations(diff_time_with_format)
                        #check time
                        if (timelimitsecond - diff_time_seconds <= 0):
                            time_error = 1
                    #if iterative counter less than possible moves's lenght
                    else:
                        #add parent to the explored and pop from the frontier
                        explored_list.append(frontier_list[0])
                        frontier_list.pop(0)
                        # Counting the Expanded nodes and holding the data of max memory temp
                        Explored_List_Item_Count += 1
                        if (Max_Memory_Temp_Number < (len(frontier_list) + len(explored_list))):
                            Max_Memory_Temp_Number = len(frontier_list) + len(explored_list)
                        #reset operations
                        temp_frontier_list.clear()
                        is_there_any_possible_move = 0
                        #time operations
                        ending_time = time.time()
                        diff_time = ending_time - beginning_time
                        diff_time_with_format = time.strftime("%H:%M:%S", time.gmtime(diff_time))
                        diff_time_seconds = time_operations(diff_time_with_format)

                        #check time
                        if (timelimitsecond - diff_time_seconds <= 0):
                            time_error = 1

            if(Max_Memory_Number<Max_Memory_Temp_Number):
                Max_Memory_Number=Max_Memory_Temp_Number
            explored_list.clear()
            frontier_list.clear()
    except MemoryError:
        memory_error=1

    total_peg = 32
    remaining_peg = 0
    if (memory_error==1):
        print("Memory error has occurred. results found before the error occurred")
    else:
        print("No memory error occurred.")
    if (len(optimal_solutions) > 0):
        print("Optimum solution found.")
        print(optimal_solutions[0]["moves"])
        print_board(optimal_solutions[0]["board"])
    else:
        print("No optimal solution found – Time Limit -> " + timestring)
        if (len(sub_optimal_solutions) > 0):
            remaining_peg = total_peg - (len(sub_optimal_solutions[0]["moves"]) - 1)
            print("Sub-optimum Solution Found with " + str(remaining_peg) + " remaining pegs")
            print(sub_optimal_solutions[0]["moves"])
            print_board(sub_optimal_solutions[0]["board"])

        else:
            print("sub optimal solution not found")
    print("Time spent -> ", time.strftime("%H:%M:%S", time.gmtime(diff_time)))
    print("The number of nodes expanded during the search.")
    print(Explored_List_Item_Count)
    print("Max number of nodes stored in the memory during the search.")
    print(Max_Memory_Number)

#we add as a parameter the amount of seconds that the function should run before it starts running
#this part same as the Depth_First_Search but only difference is removed_peg_sorted list recreated according to the reversed. Only differences are in the line 1099-1103
def Depth_First_Search_Heuristic(timelimitsecond,timestring):
    frontier_list = [{"board": initial_matrix, "removed_peg_number": "initial_state", "move": "initial_state",
                      "moves": ["initial_state"]}]
    #this part is the same as depth first search only difference is
    explored_list = []
    sub_optimal_solutions = []
    optimal_solutions = []
    temp_frontier_list = []
    is_there_any_possible_move = 0
    beginning_time = time.time()
    diff_time = 0
    diff_time_with_format = ""
    diff_time_seconds = 0
    ending_time = 0
    time_error = 0
    memory_error=0
    Optimal_Found=0

    try:
        while (Optimal_Found==0 and len(frontier_list) != 0 and time_error == 0):

            matrix = frontier_list[0]["board"]
            past_moves = []


            for i in frontier_list[0]["moves"]:
                past_moves.append(i)


            for item in matrix:
                for element in item:
                    if (element.find("P") != -1):

                        first_upper = matrix[matrix.index(item) - 1][item.index(element)]
                        second_upper = matrix[matrix.index(item) - 2][item.index(element)]

                        first_bottom = matrix[matrix.index(item) + 1][item.index(element)]
                        second_bottom = matrix[matrix.index(item) + 2][item.index(element)]

                        first_left = matrix[matrix.index(item)][item.index(element) - 1]
                        second_left = matrix[matrix.index(item)][item.index(element) - 2]

                        first_right = matrix[matrix.index(item)][item.index(element) + 1]
                        second_right = matrix[matrix.index(item)][item.index(element) + 2]

                        if (first_upper.find("A") != -1 and second_upper.find("A") != -1):

                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("up", matrix, matrix.index(item), item.index(element), element)
                            removed_peg = first_upper[0:first_upper.find("A")]
                            moved_peg = second_upper[0:second_upper.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            past_moves.append(moved_peg + "->" + target_peg)
                            temp_frontier_list.append({"board": temp_matrix, "removed_peg_number": removed_peg,
                                                       "move": moved_peg + "->" + target_peg, "moves": []})

                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            past_moves.pop()


                        if (first_bottom.find("A") != -1 and second_bottom.find("A") != -1):

                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("bottom", matrix, matrix.index(item), item.index(element), element)
                            removed_peg = first_bottom[0:first_bottom.find("A")]
                            moved_peg = second_bottom[0:second_bottom.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            past_moves.append(moved_peg + "->" + target_peg)
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg,
                                 "move": moved_peg + "->" + target_peg,
                                 "moves": []})

                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            past_moves.pop()

                        if (first_left.find("A") != -1 and second_left.find("A") != -1):

                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("left", matrix, matrix.index(item), item.index(element), element)
                            removed_peg = first_left[0:first_left.find("A")]
                            moved_peg = second_left[0:second_left.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            past_moves.append(moved_peg + "->" + target_peg)
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg,
                                 "move": moved_peg + "->" + target_peg,
                                 "moves": []})

                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            past_moves.pop()
                        if (first_right.find("A") != -1 and second_right.find("A") != -1):
                            is_there_any_possible_move = 1
                            temp_matrix = New_Matrix("right", matrix, matrix.index(item), item.index(element), element)
                            removed_peg = first_right[0:first_right.find("A")]
                            moved_peg = second_right[0:first_right.find("A")]
                            target_peg = matrix[matrix.index(item)][item.index(element)]
                            target_peg = target_peg[0:-1]
                            past_moves.append(moved_peg + "->" + target_peg)
                            temp_frontier_list.append(
                                {"board": temp_matrix, "removed_peg_number": removed_peg,
                                 "move": moved_peg + "->" + target_peg,
                                 "moves": []})

                            for i in past_moves:
                                temp_frontier_list[-1]["moves"].append(i)
                            past_moves.pop()


            if (is_there_any_possible_move == 0):
                if (matrix == target_matrix):
                    if (len(optimal_solutions) == 0):
                        Optimal_Found=1
                        optimal_solutions.append(frontier_list[0])

                else:
                    if (len(sub_optimal_solutions) == 0):
                        sub_optimal_solutions.append(frontier_list[0])
                    else:
                        old_remaining_peg_number = 32 - (len(sub_optimal_solutions[0]["moves"]) - 1)
                        new_remaining_peg_number = 32 - (len(frontier_list[0]["moves"]) - 1)
                        if (new_remaining_peg_number < old_remaining_peg_number):
                            sub_optimal_solutions.pop(0)
                            sub_optimal_solutions.append(frontier_list[0])

            removed_peg_sorted = sorted(temp_frontier_list, key=lambda k: (int(k['removed_peg_number'])))

            explored_list.append(frontier_list[0])
            frontier_list.pop(0)
            #reversed list bigger to smaller
            position = 0
            for i in reversed(removed_peg_sorted):
                frontier_list.insert(position, i)
                position += 1
            temp_frontier_list.clear()
            is_there_any_possible_move = 0
            ending_time = time.time()
            diff_time = ending_time - beginning_time
            diff_time_with_format = time.strftime("%H:%M:%S", time.gmtime(diff_time))
            diff_time_seconds = time_operations(diff_time_with_format)

            if (timelimitsecond - diff_time_seconds <= 0):
                time_error = 1
    except MemoryError:
        memory_error=1

    total_peg = 32
    remaining_peg = 0
    if (memory_error==1):
        print("Memory error has occurred. results found before the error occurred")
    else:
        print("No memory error occurred.")
    if (len(optimal_solutions) > 0):
        print("Optimum solution found.")
        print(optimal_solutions[0]["moves"])
        print_board(optimal_solutions[0]["board"])
    else:
        print("No optimal solution found – Time Limit -> " + timestring)
        if (len(sub_optimal_solutions) > 0):
            remaining_peg = total_peg - (len(sub_optimal_solutions[0]["moves"]) - 1)
            print("Sub-optimum Solution Found with " + str(remaining_peg) + " remaining pegs")
            print(sub_optimal_solutions[0]["moves"])
            print_board(sub_optimal_solutions[0]["board"])

        else:
            print("sub optimal solution not found")
    print("Time spent -> ", time.strftime("%H:%M:%S", time.gmtime(diff_time)))
    print("The number of nodes expanded during the search.")
    print(len(explored_list))
    print("Max number of nodes stored in the memory during the search.")
    print(len(explored_list) + len(frontier_list))

#Replace the old image of the board with the new image according to the desired action.
def New_Matrix(position,matrix1,index_of_column,index_of_row,empty_peg):
    temp_matrix=deepcopy(matrix1)
    if(position=="left"):

        will_be_empty=temp_matrix[index_of_column][index_of_row-2]
        will_be_empty = will_be_empty.replace("A", "P")
        temp_matrix[index_of_column][index_of_row-2]=will_be_empty

        will_be_removed=temp_matrix[index_of_column][index_of_row-1]
        will_be_removed=will_be_removed.replace("A","P")
        temp_matrix[index_of_column][index_of_row - 1] = will_be_removed

        will_be_active=temp_matrix[index_of_column][index_of_row]
        will_be_active = will_be_active.replace("P", "A")
        temp_matrix[index_of_column][index_of_row] = will_be_active

        return temp_matrix


    elif(position=="right"):

        will_be_empty = temp_matrix[index_of_column][index_of_row + 2]
        will_be_empty = will_be_empty.replace("A", "P")
        temp_matrix[index_of_column][index_of_row + 2] = will_be_empty

        will_be_removed = temp_matrix[index_of_column][index_of_row + 1]
        will_be_removed = will_be_removed.replace("A", "P")
        temp_matrix[index_of_column][index_of_row + 1] = will_be_removed

        will_be_active = temp_matrix[index_of_column][index_of_row]
        will_be_active = will_be_active.replace("P", "A")
        temp_matrix[index_of_column][index_of_row] = will_be_active

        return temp_matrix

    elif(position=="up"):

        will_be_empty = temp_matrix[index_of_column-2][index_of_row]
        will_be_empty = will_be_empty.replace("A", "P")
        temp_matrix[index_of_column-2][index_of_row] = will_be_empty

        will_be_removed = temp_matrix[index_of_column-1][index_of_row]
        will_be_removed = will_be_removed.replace("A", "P")
        temp_matrix[index_of_column-1][index_of_row] = will_be_removed

        will_be_active = temp_matrix[index_of_column][index_of_row]
        will_be_active = will_be_active.replace("P", "A")
        temp_matrix[index_of_column][index_of_row] = will_be_active

        return temp_matrix

    elif(position=="bottom"):

        will_be_empty = temp_matrix[index_of_column + 2][index_of_row]
        will_be_empty = will_be_empty.replace("A", "P")
        temp_matrix[index_of_column + 2][index_of_row] = will_be_empty

        will_be_removed = temp_matrix[index_of_column + 1][index_of_row]
        will_be_removed = will_be_removed.replace("A", "P")
        temp_matrix[index_of_column + 1][index_of_row] = will_be_removed

        will_be_active = temp_matrix[index_of_column][index_of_row]
        will_be_active = will_be_active.replace("P", "A")
        temp_matrix[index_of_column][index_of_row] = will_be_active

        return temp_matrix

    else:
        print("New Matrix fonksiyonu parametresi position yanlış girildi")
        return "hata"

#a function to view the board by looking at the matrix to show the final image
def print_board(BoardMatrix):
    print("The board looks like this. ( Xs indicate filled places and Os indicate empty spaces.) ")
    #check each element in the matrix
    for line in BoardMatrix:
        #check each item in that element
        for item in line:
            #if zero than print space
            if (item=="0"):
                print(" ", end=' ')
            #if "P", it means empty slot
            elif("P" in item):
                print("O", end=' ')
            #if "A", it means not empty slot
            elif("A" in item):
                print("x", end=' ')
            else:
                print("hata")
        print()

def time_operations(timeinput):

    #Split the given time input
    timedata=timeinput.split(":")
    #According to the position convert to hour minute or second. Also checks the (01-> is not int if given input 01 then takes 1 as a variable)
    if (timedata[0][0]=="0"):
        hour=int(timedata[0][1])
    else:
        hour=int(timedata[0])
    if (timedata[1][0] == "0"):
        minute = int(timedata[1][1])
    else:
        minute = int(timedata[1])
    if (timedata[2][0] == "0"):
        second = int(timedata[2][1])
    else:
        second = int(timedata[2])
    #convert to seconds and add them up
    total_second=(hour*60*60)+(minute*60)+second
    return total_second
#Create menu
def menu():
    print("---------------------------------------------------------------------- Menu ----------------------------------------------------------------------")
    print("1-) Breadth-First Search")
    print("2-) Depth-First Search")
    print("3-) Iterative Deepening Search")
    print("4-) Depth-First Search with Random Selection")
    print("5-) Depth-First Search with a Node Selection Heuristic")
    #take choice
    while (True):
        userchoice= input("Choose the method you wanted to search with ")
        if (userchoice=="1"):
            break
        elif (userchoice=="2"):
            break
        elif (userchoice=="3"):
            break
        elif (userchoice=="4"):
            break
        elif (userchoice=="5"):
            break
        else:
            print("Try Again")
            continue
    #check if its valid or not. If not then try again
    while(True):
        timeinput = input("Write the time limit ? Ex(01:00:00)(Hour:Minute:Sec))")
        if (len(timeinput)!=8):
            print("Pls try again")
            continue
        elif(timeinput[2]!=":" or timeinput[5]!=":"):
            print("Pls try again")
            continue
        elif((timeinput[0:2].isnumeric()==False) or (timeinput[3:5].isnumeric()==False) or (timeinput[6:].isnumeric()==False)):
            print("Pls try again")
            continue
        elif (int(timeinput[0:2])>24 or int(timeinput[3:5])>=60 or int(timeinput[6:])>=60):
            print("Pls try again")
            continue
        elif (timeinput[0:2]=="00" and timeinput[3:5]=="00" and timeinput[6:]==00):
            print("You can not run the program 0 seconds")
        else:
            break
    #print the total seconds that program will run
    print("Seconds the program will run " + str(time_operations(timeinput)))
    #according to the user choice run the search method
    if (userchoice == "1"):
        print("Search Method -> Breadth First Search     Time Limit -> "+timeinput)
        Breadth_First_Search(time_operations(timeinput),timeinput)
    elif (userchoice == "2"):
        print("Search Method -> Depth First Search     Time Limit -> " + timeinput)
        Depth_First_Search(time_operations(timeinput),timeinput)
    elif (userchoice == "3"):
        print("Search Method -> Iterative Depth First Search     Time Limit -> " + timeinput)
        Iterative_Depth_First_Search(time_operations(timeinput),timeinput)
    elif (userchoice == "4"):
        print("Search Method -> Depth First Search Random Selection    Time Limit -> " + timeinput)
        Depth_First_Search_Random_Selection(time_operations(timeinput),timeinput)
    elif (userchoice == "5"):
        print("Search Method -> Depth First Search Heuristic     Time Limit -> " + timeinput)
        Depth_First_Search_Heuristic(time_operations(timeinput),timeinput)
    else:
        print("hata mesajı")
#Run whole code
menu()



