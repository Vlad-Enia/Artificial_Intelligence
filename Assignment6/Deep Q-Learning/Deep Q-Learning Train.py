import collections
import time
import numpy as np
import gym
from tensorflow import keras
from keras.layers import Dense
from keras.regularizers import l2
from keras.losses import Huber
import random

learning_rate = 0.01
kernel_reg = l2()
loss_function = Huber()
optimizer = keras.optimizers.Adam(learning_rate=learning_rate, clipnorm=1.0)


def agent(state_shape, action_shape):
    """
        Method that creates a neural network which has as input a processed game state and as output a list of qs for each possible action.
        The neural network has three hidden layers and one output layer:
        - layer 1
            - 100 units
            - receives as input state_shape values
            - activation - ReLU
            - regularizer - L2
        - layer 3
            - 50 units
            - activation - ReLU
            - regularizer - L2
        - output layer
            - action_shape units
            - activation linear
        Optimizer - Adam
        Loss function - Huber, custom (see train method)
        :param state_shape: shape of a state, basically the shape of the input
        :param action_shape: shape the action set, basically the shape of the output
        :return: model described above
    """
    model = keras.Sequential()
    model.add(Dense(100, activation='relu', input_shape=(state_shape,), kernel_regularizer=kernel_reg))
    model.add(Dense(50, activation='relu', kernel_regularizer=kernel_reg))
    model.add(Dense(action_shape, activation='linear'))
    model.compile(loss=loss_function, optimizer=optimizer)
    return model


env = gym.make("FrozenLake-v1", is_slippery=False)
discount_factor = 0.8
batch_size = 50
state_shape = env.observation_space.n
action_shape = env.action_space.n


def one_hot(a):
    a = np.array(a)
    b = np.zeros((a.size, state_shape))
    b[np.arange(a.size), a] = 1
    return b


def train(replay_memory, model, target_model):
    if len(replay_memory) < batch_size:
        return

    batch = random.sample(replay_memory, batch_size)

    for sample in batch:
        state, action, reward, future_state, done = sample
        model_input = one_hot([state])
        current_q_list = model.predict(model_input)
        if not done:
            target_model_input = one_hot([future_state])
            future_q_max = max(target_model.predict(target_model_input)[0])
            current_q_list[0][action] = reward + discount_factor * future_q_max
        else:
            current_q_list[0][action] = reward

        model.fit(model_input, current_q_list, verbose=0, epochs=1)


train_episodes = 1000
moves_per_episode = 100
model = agent(state_shape, action_shape)
target_model = agent(state_shape, action_shape)
target_model.set_weights(model.get_weights())
replay_memory = collections.deque(maxlen=100000)

epsilon = 1
max_epsilon = 1
min_epsilon = 0.1
decay = max_epsilon / train_episodes
steps = 0

print('Started training...')
for episode in range(train_episodes):
    start_time = time.time()
    score = 0
    state = env.reset()
    for move in range(moves_per_episode):
        env.render()
        rand_nb = np.random.rand()
        if rand_nb <= epsilon:  # Explore
            action = np.random.randint(0, action_shape)
        else:  # Exploit action with maximum predicted Q, using our main model
            processed_input = one_hot([state])
            predicted_qs = model.predict(processed_input)
            action = np.argmax(predicted_qs[0])

        next_state, reward, done, _ = env.step(action)

        score += reward

        replay_memory.append([state, action, reward, next_state, done])

        train(replay_memory, model, target_model)

        state = next_state

        if steps >= 100:
            print('Copying weights from main model to target model...')
            target_model.set_weights(model.get_weights())
            steps = 0

        if done:
            break

    if done:
        print("\nEpisode {} DONE\n\t- score: {}\n\t- duration: {}\n\t- epsilon: {}".format(episode, score,
                                                                                           time.time() - start_time,
                                                                                           epsilon))
    else:
        print("\nEpisode {} \n\t- score: {}\n\t- duration: {}\n\t- epsilon: {}".format(episode, score,
                                                                                       time.time() - start_time,
                                                                                       epsilon))

    # Update epsilon after each episode
    if epsilon > min_epsilon:
        epsilon = epsilon - decay
    else:
        epsilon = min_epsilon

    model.save("model.h5")
    print("Model saved to disk")
    target_model.save("target_model.h5")
    print("Target model saved to disk")
