# 1. Manual definition of a state and a transition
class State():
    def __init__(self, size, obstacles, start, finish):
        lake = [['F' for i in range(size)] for j in range(size)]
        for e in obstacles:
            lake[e[0]][e[1]] = 'H'
        lake[start[0]][start[1]] = 'S'
        lake[finish[0]][finish[1]] = 'G'
        self.lake = lake
        self.current = start

    def __str__(self):
        return str((self.lake, self.current))


def create_initial_state(size, obstacles, start, finish):
    lake = [['F' for i in range(size)] for j in range(size)]
    for e in obstacles:
        lake[e[0]][e[1]] = 'H'
    lake[start[0]][start[1]] = 'S'
    lake[finish[0]][finish[1]] = 'G'
    current = start
    return (lake, current)


def move(s, action):
    if action == 'Up':
        s.current = (max(0, s.current[0] - 1), s.current[1])
    elif action == 'Right':
        s.current = (s.current[0], min(len(s.lake[0]), s.current[1] + 1))
    elif action == 'Down':
        s.current = (min(len(s.lake), s.current[0] + 1), s.current[1])
    elif action == 'Left':
        s.current = (s.current[0], max(0, s.current[1] - 1))
    return s


state = State(size=4, obstacles=[(1, 1), (1, 3), (2, 3), (3, 0)], start=(0, 0), finish=(3, 3))
print(state)
POSSIBLE_MOVES = {'Up', 'Right', 'Down', 'Left'}
print(move(state, 'Up'))
print(move(state, 'Right'))
print(move(state, 'Down'))
print(move(state, 'Left'))


# Training using Q-Learning.
########### I.C 
### Look at this before: https://www.youtube.com/watch?v=qhRNvCVVJaA :)
### Note: We will only explore when we don't have any information about a state (A line of the table is only with 0). We can do this because:
###       1. We only have one reward
###       2. We don't want the shortest path
import numpy as np
import gym
import pickle

env = gym.make("FrozenLake-v1", is_slippery=False)
n_states = env.observation_space.n
n_actions = env.action_space.n
print("Number of actions:", n_actions)  # Should print 16 since we have a 4x4 grid
print("Number of states:", n_states)  # Should print 4 since we can move in 4 directions Left/Down/Right/Up

# Initialize the Q-table to 0
Q_table = np.zeros((n_states, n_actions))  # 16x4 grid
print("Q table:\n", Q_table)  # 16x4 grid full with 0

################ HYPERPARAMETERS ##################
N_EPISODES = 1000  # Number of runs (from start to goal or to death or out of moves)
MOVES_PER_ITER = 100  # Number of moves available per run
gamma = 0.99  # discount factor
lr = 0.01  # learning rate
################ ################ ##################
rewards_per_episode = list()

for e in range(N_EPISODES):
    current_state = env.reset()
    done = False
    total_episode_reward = 0

    for i in range(MOVES_PER_ITER):
        # env.render() #uncomment to check paths
        # If we don't have any info about a state pick randomly (otherwise np.argmax returns left and we will never move)
        if sum(Q_table[current_state, :]) == 0:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q_table[current_state, :])  # select the best action for current state

        next_state, reward, done, _ = env.step(
            action)  # apply the action/step and get the next state, the reward and if the state is final

        # We update our Q-table using the Q-learning iteration
        # (CHECK Q-value Updation from: https://www.analyticsvidhya.com/blog/2021/02/understanding-the-bellman-optimality-equation-in-reinforcement-learning/ )
        Q_table[current_state, action] = (1 - lr) * Q_table[current_state, action] + lr * (
                reward + gamma * max(Q_table[next_state, :]))
        total_episode_reward = total_episode_reward + reward
        # If the episode is finished, we leave the for loop
        if done:
            break
        current_state = next_state
    rewards_per_episode.append(total_episode_reward)

file = open('q_table.txt', 'wb')
pickle.dump(Q_table, file)
file.close()

print(rewards_per_episode)
print("Number of solutions found:", sum(rewards_per_episode))
print(f"Average success ratio:{sum(rewards_per_episode) * 100 / N_EPISODES}%")
print("Final Q table:\n", Q_table)
