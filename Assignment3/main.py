from random import sample
import copy
from itertools import permutations

def choose_k_from_m_times_n(n, m, k):
    ball_sample = [e // m for e in range(n * m)]
    return sample(ball_sample, k)


def init(n, m, k):
    # n = number of colours
    # m = number of balls of each colour
    # k = number of chosen balls
    # A_list = the sequence of balls chosen by A
    # B_list = a list of sequences; will be updated each time player B chooses a sequence of balls
    # return [n, m, k, A_list, B_list]
    return [n, m, k, choose_k_from_m_times_n(n, m, k), []]


def is_final(state):
    no_moves_B = len(state[4])
    if no_moves_B > 0:  # and if B has made at least one move
        A_list = state[3]
        n = state[0]
        B_list = list(state[4][-1])
        if no_moves_B < 2 * n:  # if B hasn't reached the maximum number of moves (2*n)
            if A_list == B_list:  # check if B guessed list of colours chosen by A
                return 1  # if so, B wins
            else:
                return 0  # if not, our state is not final
        elif no_moves_B == 2 * n:  # else if B has made the last move
            if A_list == B_list:  # check if the guess is right
                return 1  # if so, B wins
            else:
                return -1  # if not, A wins
    else:
        return 0  # if B hasn't made any moves then state is not final


def get_number_of_matches(l1, l2):
    counter = 0
    length = len(l1)
    for i in range(0, length):
        if l1[i] == l2[i]:
            counter += 1
    return counter


def process_input(B_input, n, m, k):
    if B_input[-1].isdigit() is False:
        B_input = B_input.rstrip(B_input[-1])
    B_input_list = B_input.replace(' ', '').split(',')
    B_input_list = list(map(int, B_input_list))

    if len(B_input_list) != k:
        print("Invalid input! You may choose a sequence of", k, 'balls!')
        return False
    else:
        d = {}
        for colour in range(0, n):
            d[colour] = 0
        for ball in B_input_list:
            if ball >= n:
                print("Invalid input! Not a correct color! You may choose from the following color set: ",
                      list(range(0, n)), '.', sep='')
                return False
            else:
                d[ball] += 1
                if d[ball] > m:
                    print("Invalid input! You can't choose more than", m, "balls of the same color.")
                    return False
    return B_input_list


# initial_state = init(3, 2, 3)
# print("Initial state:", initial_state)
# print("Is initial state final (should be 0):", is_final(initial_state))
# print()
#
# state = copy.deepcopy(initial_state)
# state[4].append([1, 1, 1])
# print("State:", state)
# print("Is State final (should be 0):", is_final(state))  # not a final state
# state[4].append(state[3])
# print("Is State final (should be 1):", is_final(state))  # correct guess and the move  is not last => B wins
# print()
#
# state2 = copy.deepcopy(state)
# state2[4].append([])
# state2[4].append([])
# state2[4].append([])
# state2[4].append([])
# print("State2:", state2)
# print("Is State2 final (should be -1):",
#       is_final(state2))  # B has reached max number of moves and hasn't guessed yet => A wins
# print()
#
# state3 = copy.deepcopy(state2)
# state3[4][-1] = state3[3]
# print("State3:", state3)
# print("Is State2 final (should be 1):", is_final(state3))  # B guessed on the last move => B wins
# print()
#
# print("Matching:", get_number_of_matchings(initial_state[3], [1, 1, 1]))
# print("Matching:", get_number_of_matchings(initial_state[3], initial_state[3]))


def print_previous_moves(A_chosen,B_moves):
    print("~~~~Previous Moves~~~")
    for index in range(len(B_moves)):
        print(f"{index+1}: {B_moves[index]} | Matches: {get_number_of_matches(A_chosen,B_moves[index])}")

# ########### Interface implementation ######
# initial_state = init(3, 2, 3)
# n = initial_state[0]
# m = initial_state[1]
# k = initial_state[2]
# A_list = initial_state[3]
# B_moves = initial_state[4]
# moves = 2 * n
# print("There are ", n, " colors available: ", list(range(0, n)), ".", sep='')
# print("There are", m, "balls of each color.")
# ball_sample = [e // m for e in range(n * m)]
# print("All of the available balls to choose from: ", ball_sample, ".", sep='')
# print("A has chosen", k, "balls.")
# print("You may choose a sequence of", k, "balls. Note that you can't choose more than", m,
#       "balls of the same color.")
# print("Attention! Sequence elements need to be separated by comma! There may also be whitespaces between elements.")
# B_won = False
# while moves:
#     print("\nYou have", moves, "moves left.")
#
#     B_list=False
#     while not B_list:
#         B_input = input("Your sequence of balls: ")
#         B_list = process_input(B_input, n, m, k)
#     moves -= 1
#     if B_list:
#         B_moves.append(B_list)
#         final = is_final(initial_state)
#         if final == 1:
#             print("\nYou won!")
#             B_won = True
#             break
#         elif final == 0:
#             no_matches = get_number_of_matches(A_list, B_list)
#             print("Number of matches with A's sequence of colours: ", no_matches, '.', sep='')
#             print_previous_moves(A_list,B_moves)
# if not B_won:
#     print("\nGame over! A won!")
#     print("Chosen sequence was: ",A_list)
#     print("Your moves:")
#     print_previous_moves(A_list, B_moves)

def generate_all_possible_codes(state):
    n = state[0]
    m = state[1]
    k = state[2]
    ball_sample = [e // m for e in range(n * m)]
    print(ball_sample)
    aux=set(permutations(ball_sample, k))

    return [list(e) for e in aux]


def knuth_algorithm_no_prunning(state):
    #1 create a set S of all possible codes
    all_codes=generate_all_possible_codes(state)
    S=copy.deepcopy(all_codes)

    #2 start with initial guess 1122

    current_guess=[1,1,2,2]
    nr_of_guesses=2*state[0]

    print("A guess:",state[3])
    while nr_of_guesses>0:
        # 3 play the guess to get a nr of matchings
        print("Current guess:",current_guess)
        state[4].append(current_guess)
        nr_matches=get_number_of_matches(state[3],state[4][-1])

        if nr_matches==state[2]:
            # 4 Game is won
            print("Game won by player B!")
            print("Solution:",current_guess)
            print("Your moves:")
            print_previous_moves(current_guess, state[4])
            break
        else:
            # 5 Remove from S any code that would not give the same response if the guess were the code
            S=list(filter(lambda e:get_number_of_matches(e,state[4][-1])==nr_matches,S))
            print("S space:",S)
            print("Space length:",len(S))
            # 6 Apply minimax technique to find a next guess as follows:
            # For each possible guess, that is, any unused code of the 1296 not just those in S,
            # calculate how many possibilities in S would be eliminated for each possible colored/white peg score.
            # The score of a guess is the minimum number of possibilities it might eliminate from S.
            # A single pass through S for each unused code of the 1296 will provide a hit count for each coloured/white peg score found;
            # the coloured/white peg score with the highest hit count will eliminate the fewest possibilities;
            # calculate the score of a guess by using "minimum eliminated" = "count of elements in S" - (minus) "highest hit count".
            # From the set of guesses with the maximum score, select one as the next guess, choosing a member of S whenever possible.
            # (Knuth follows the convention of choosing the guess with the least numeric value e.g. 2345 is lower than 3456.
            # Knuth also gives an example showing that in some cases no member of S will be among the highest scoring guesses and thus the guess cannot win on the next turn,
            # yet will be necessary to assure a win in five.)
            max_remaining=[]
            for x in all_codes:
                remained_in_S=[0]*(state[2]+1)
                for y in S:
                    x_y_matches=get_number_of_matches(x,y)
                    remained_in_S[x_y_matches]+=1
                max_remaining.append(max(remained_in_S))


            found_in_s=0
            for i in range(len(all_codes)):
                if all_codes[i] in S:
                    if max_remaining[i]==min(max_remaining):
                        current_guess=all_codes[i]
                        found_in_s=1
                        nr_of_guesses -= 1
                        break
            if found_in_s:
                continue

            min_index=max_remaining.index(min(max_remaining))
            current_guess=all_codes[min_index]
        nr_of_guesses-=1
    if nr_of_guesses==0:
        print("Player A won! ")

def knuth_algorithm_with_prunning(state,alpha,beta):
    #1 create a set S of all possible codes
    all_codes=generate_all_possible_codes(state)
    S=copy.deepcopy(all_codes)

    #2 start with initial guess 1122

    #current_guess=[1,1,2,2]
    current_guess = [1, 1, 2, 2]
    nr_of_guesses=2*state[0]

    print("A guess:",state[3])
    while nr_of_guesses>0:
        # 3 play the guess to get a nr of matchings
        print("Current guess:",current_guess)
        state[4].append(current_guess)
        nr_matches=get_number_of_matches(state[3],state[4][-1])

        if nr_matches==state[2]:
            # 4 Game is won
            print("Game won by player B!")
            print("Solution:",current_guess)
            print("Your moves:")
            print_previous_moves(current_guess, state[4])
            break
        else:
            # 5 Remove from S any code that would not give the same response if the guess were the code
            S=list(filter(lambda e:get_number_of_matches(e,state[4][-1])==nr_matches,S))
            print("S space:",S)
            print("Space length:",len(S))
            # 6 Apply minimax technique to find a next guess as follows:
            # For each possible guess, that is, any unused code of the 1296 not just those in S,
            # calculate how many possibilities in S would be eliminated for each possible colored/white peg score.
            # The score of a guess is the minimum number of possibilities it might eliminate from S.
            # A single pass through S for each unused code of the 1296 will provide a hit count for each coloured/white peg score found;
            # the coloured/white peg score with the highest hit count will eliminate the fewest possibilities;
            # calculate the score of a guess by using "minimum eliminated" = "count of elements in S" - (minus) "highest hit count".
            # From the set of guesses with the maximum score, select one as the next guess, choosing a member of S whenever possible.
            # (Knuth follows the convention of choosing the guess with the least numeric value e.g. 2345 is lower than 3456.
            # Knuth also gives an example showing that in some cases no member of S will be among the highest scoring guesses and thus the guess cannot win on the next turn,
            # yet will be necessary to assure a win in five.)
            max_remaining=[]
            for x in all_codes:
                remained_in_S=[0]*(state[2]+1)
                for y in S:
                    x_y_matches=get_number_of_matches(x,y)
                    remained_in_S[x_y_matches]+=1

                maxVal=-999999999
                for e in remained_in_S:
                    maxVal=max(maxVal,e)
                    alpha=max(alpha,e)
                    if beta<=alpha:
                        break
                max_remaining.append(maxVal)


            found_in_s=0
            for i in range(len(all_codes)):
                if all_codes[i] in S:
                    minVal=99999999
                    for e in max_remaining:
                        minVal=min(minVal,e)
                        beta=min(beta,e)
                        if beta<=alpha:
                            break

                    current_guess=all_codes[i]
                    found_in_s=1
                    nr_of_guesses-=1
                    break
            if found_in_s:
                continue

            minVal = 99999999
            for e in max_remaining:
                minVal = min(minVal, e)
                beta = min(beta, e)
                if beta <= alpha:
                    break

            min_index=max_remaining.index(minVal)
            current_guess=all_codes[min_index]
        nr_of_guesses-=1
    if nr_of_guesses==0:
        print("Player A won! ")
import time

initial_state=init(8,4,4)
print(initial_state)
start_time = time.time()
knuth_algorithm_no_prunning(initial_state)
no_prunning_time="--- %s seconds ---" % (time.time() - start_time)

initial_state[4]=[]

start_time = time.time()
knuth_algorithm_with_prunning(initial_state,-9999999999,+999999999)
prunning_time="--- %s seconds ---" % (time.time() - start_time)

print("No prunning/prunning",no_prunning_time,prunning_time)