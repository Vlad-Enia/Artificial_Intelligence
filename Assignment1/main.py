# (0.2) Alegeți o reprezentare a unei stări a problemei. Reprezentarea trebuie să fie suficient de explicită pentru a conține toate informaţiile necesare pentru continuarea găsirii unei soluții dar trebuie să fie și suficient de formalizată pentru a fi ușor de prelucrat/memorat.
# (0.2) Identificați stările speciale (inițială și finală) și implementați funcția de inițializare (primește ca parametrii instanța problemei, întoarce starea inițială) și funcția booleană care verifică dacă o stare primită ca parametru este finală.
import numpy as np
import copy
import queue
import random


def init(n):
    H = [False] * n
    W = [False] * n
    b = False
    state = [H, W, b]
    return state


def check_final(state):
    return sum(state[0]) == len(state[0]) and sum(state[1]) == len(state[1]) and state[2] == True


def women_without_husband(state, shore):
    for i in range(0, len(state[0])):
        if state[1][i] == shore and state[0][i] != state[1][i]:
            return True
    return False


def validate_transition(state, params):
    if len(params) > 4 or len(params) < 2:  # Sunt 1 sau 2 persoane
        return False
    for i in range(0, len(params), 2):  # Persoanele sunt pe acelasi mal cu barca
        if state[params[i]][params[i + 1]] != state[2]:
            return False
    for i in range(0, len(params), 2):
        if i == 1:  # caz in care se muta sotia
            # Sa fie sotul ei pe malul destinatie deja SAU Pe malul destinatie sa nu fie niciun alt SOT SAU  -> Mutare valida
            if state[0][params[i + 1]] == state[1][params[i + 1]] or state[0].count(state[1][params[i + 1]]) == 0:
                continue
            else:
                return False
        else:  # caz in care se muta sotul
            if \
                    (
                            state[0][params[i + 1]] == state[1][params[i + 1]]  ### Sunt pe acelasi mal
                            or
                            (state[0][params[i + 1]] != state[1][params[i + 1]]  ### Sunt pe maluri diferite
                             and
                             state[0].count(state[1][params[i + 1]]) == 0
                            )  ### Dar nu sunt barbati ramasi pe malul pe care a ramas femeia
                    ) \
                            and women_without_husband(state, state[0][
                        params[i + 1]]) == False:  # pe malul destinatie nu sunt femei fara sot
                continue
            else:
                return False
    return True


def transition(state, params):
    ## Daca tranzitia este valida returnam o stare modificata altfel returnam aceeasi stare
    state_copy = copy.deepcopy(state)
    for i in range(0, len(params), 2):
        state_copy[params[i]][params[i + 1]] = not state_copy[params[i]][params[i + 1]]
    state_copy[2] = not state_copy[2]
    if validate_transition(state_copy, params):
        return state_copy
    else:
        return state


def solve_BKT(state, visited_states, all_transitions, partial_solution):
    if (check_final(state) == True):
        print("Solution found for BKT")
        print("Transitions made to final solution:")
        print(partial_solution)
        return
    else:
        for t in all_transitions:
            state_copy = transition(state, t)
            if state_copy != state and state_copy not in visited_states:
                visited_states.append(state_copy)
                new_partial_solution = copy.deepcopy(partial_solution)
                new_partial_solution.append(state_copy)
                solve_BKT(state_copy, visited_states, all_transitions, new_partial_solution)


def solve_BFS(state, all_transitions, visited_states, q, tr_parent_dict):
    visited_states.append(state)
    if (check_final(state) == True):
        print("Solution found for BFS")
        print("Trying to rebuild solution:")
        #print("Parent dict:",tr_parent_dict)
        current = repr(state)
        initial_state = repr([[False] * len(state[0]), [False] * len(state[0]), False])
        final = [initial_state]
        while current != initial_state:
            final.insert(1, current)
            current = tr_parent_dict[current]
        print(final)
        return
    for t in all_transitions:
        new_state = transition(state, t)
        if new_state != state and new_state not in visited_states:
            if repr(new_state) not in tr_parent_dict:
                tr_parent_dict[repr(new_state)] = repr(state)
            q.put(new_state)
    while not q.empty():
        neighbour = q.get()
        if neighbour not in visited_states:
            solve_BFS(neighbour, all_transitions, visited_states, q, tr_parent_dict)


def evaluate(state):
    return sum(state[0])+sum(state[1])


def min_finder_first(state,all_transitions,transitions_made):
    possible_transitions=[[x,y] for x in all_transitions for y in all_transitions if x!=y]
    local=False
    while not local:
        random.shuffle(all_transitions)
        local=False
        initial_state=state
        for transition_pair in possible_transitions:
            # Transition from A to B
            new_state=transition(state,transition_pair[0])
            if new_state==state:
                continue
            elif check_final(new_state):
                transitions_made.append(new_state)
                return new_state,transitions_made

           # Transition from B to A
            new_state2=transition(new_state,transition_pair[1])
            if new_state2 == new_state:
                continue

            #If new solution is better
            if evaluate(new_state2)>evaluate(state):
                state=new_state2
                transitions_made.append(new_state)
                transitions_made.append(new_state2)
                break
        if initial_state==state:
            local=True
    return state,transitions_made

def hill_climbing_first_improvement(state,all_transitions,nr_of_iterations):
    global_local_maximum=state
    global_local_maximum_path=[]
    for i in range(nr_of_iterations):
        random.shuffle(all_transitions)
        local_maximum,transitions_made=min_finder_first(state,all_transitions,[])
        if evaluate(local_maximum)>evaluate(global_local_maximum):
            print("New local maxima found: ",local_maximum)
            global_local_maximum=local_maximum
            global_local_maximum_path=transitions_made
    print("Best solution found:",global_local_maximum)
    print("Path to solution:",global_local_maximum_path)

def h(state):
    return 2*len(state[0])-evaluate(state)


def evaluate_a_star(state,path_len):
    return path_len+h(state)


def a_star(state,all_transitions,tr_parent_dict):
    q=[]
    transitions_made=[]
    path_len=0
    while True:
        path_len+=1
        for t in all_transitions:
            new_state=transition(state,t)
            if new_state!=state and ((new_state,path_len) not in q) and new_state not in transitions_made:
                if repr(new_state) not in tr_parent_dict: #push in the dictionary only the first time we are visiting a node
                    tr_parent_dict[repr(new_state)] = repr(state)
                q.append((new_state,path_len))

        q.sort(key=lambda e: evaluate_a_star(e[0],path_len))
        current_element=q.pop(0)
        transitions_made.append(current_element[0])
        state=current_element[0]
        if(check_final(current_element[0])):
            print("Transitions made by A* search:")
            for e in transitions_made:
                print(e)
            print("Trying to rebuild solution:")
            current = repr(current_element[0])
            initial_state = repr([[False] * len(state[0]), [False] * len(state[0]), False])
            final = [initial_state]
            while current != initial_state:
                final.insert(1, current)
                current = tr_parent_dict[current]
            print(final)
            return current_element[0],transitions_made,tr_parent_dict


while True:
    COUPLE_NUMBER=int(input("Add the number of couples:"))
    state = init(COUPLE_NUMBER)
    print("Initial state:", state)
    one_man_transitions = [[x, y] for x in range(0, 2) for y in range(0, len(state[0]))]
    two_man_transitions = [x + y for x in one_man_transitions for y in one_man_transitions if x != y and x[0]<=x[1]]
    all_transitions = one_man_transitions + two_man_transitions
    print("All transitions possible:",all_transitions)
    random.shuffle(all_transitions)  # <- Shuffle transitions

    SOLVER_TYPE=int(input("Add the solver type \n1 for BKT, \n2 for BFS, \n3 for HillClimbing, \n4 for A* search:\n"))
    if SOLVER_TYPE==1:
        solve_BKT(state, [state], all_transitions, [state])
    elif SOLVER_TYPE==2:
        solve_BFS(state, all_transitions, [], queue.Queue(), dict())
    elif SOLVER_TYPE==3:
        NUMBER_OF_GENERATIONS=int(input("Add the number of iterations for hillclimbing first improvement:"))
        hill_climbing_first_improvement(state, all_transitions, NUMBER_OF_GENERATIONS)
    elif SOLVER_TYPE==4:
        a_star(state, all_transitions, dict())

#solve_BFS(state, all_transitions, [], queue.Queue(), dict())
#hill_climbing_first_improvement(state,all_transitions,100)

#(0.2) Implementați strategia Hillclimbing.
#(0.2) Implementați strategia A*
#(0.2) Implementați un meniu care permite, după introducerea instanței, selectarea strategiei care va fi încercată.

