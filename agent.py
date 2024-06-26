import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from helper import plot
import math

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self, game):
        self.game = game
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        # TODO: model, trainer
        self.model = Linear_QNet(13, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    
    def get_state(self):
        state = [
            self.game.level.car.angle, self.game.level.car.speed * math.cos(math.radians(self.game.level.car.angle)), self.game.level.car.speed * math.sin(math.radians(self.game.level.car.angle)), self.game.level.car.speed, self.game.level.car.dtheta, 
            self.game.level.track.flag.x - self.game.level.car.x, self.game.level.track.flag.y - self.game.level.car.y,
            self.game.level.car.raytrace()[0], self.game.level.car.raytrace()[1], self.game.level.car.raytrace()[2], self.game.level.car.raytrace()[3], self.game.level.car.raytrace()[4], self.game.level.car.raytrace()[5]
        ]
        return np.array(state, dtype=np.float64)
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) 
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train(game):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record_time = 0
    Area_Reward = 0
    agent = Agent(game)
    while True:
        # get old state
        state_old = agent.get_state()
        # get move
        final_move = agent.get_action(state_old)
        # perform move and get new state
        reward, done, score = game.play_step(final_move)#implement this
        Area_Reward += reward
        state_new = agent.get_state()

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory
            agent.n_games += 1
            agent.train_long_memory()

            if score < record_time:
                record_time = score
                agent.model.save()
            Average_Reward = Area_Reward/game.frame_iteration
            print('Game', agent.n_games, 'Average Reward', Average_Reward, 'Record Time:', record_time)
            Area_Reward = 0
            game.resetAI()
            plot_scores.append(Average_Reward)
            total_score += Average_Reward
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()

