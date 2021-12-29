import gym
import pickle
import numpy as np
env = gym.make("FrozenLake-v1", is_slippery=False)

file = open('q_table.txt', 'rb')
q_table = pickle.load(file)
file.close()

total_epochs, total_penalties = 0, 0
episodes = 100

for _ in range(episodes):
    state = env.reset()
    epochs, penalties, reward = 0, 0, 0

    done = False

    while not done:
        action = np.argmax(q_table[state])
        state, reward, done, info = env.step(action)

        if reward == -10:
            penalties += 1

        epochs += 1

    total_penalties += penalties
    total_epochs += epochs

print(f"Results after {episodes} episodes:")
print(f"Average steps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")