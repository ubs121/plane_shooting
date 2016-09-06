#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import numpy as np

class LearningAgent():
    """An agent that learns to shoot"""
    alpha = 0.1
    gamma = 0.2
    epsilon = 0.5

    def __init__(self, env):
        self.env = env
        self.q = {} # q learning memory

    def reset(self):
        self.state = ""
        self.actions = [i for i in range(self.env.size * self.env.size)] # all possible actions/shoots
        self.action = 0

    def build_state(self):
        hints = self.env.get_hints() # head hints
        board = self.env.get_board() # board

        # current board as state
        s = []
        for r in xrange(self.env.size):
            s += board[r]

        # hints as state
        # s = []
        # for p in hints:
        #     s.append(p.head[1]*10 + p.head[0])

        return tuple(s)

    def next_shoot(self):
        self.state = self.build_state()

        shot = 0

        if random.random() < self.epsilon:
            shot = random.choice(self.actions)
        else:
            sa_Q_values = [self.q.get((self.state, a), 0.0) for a in self.actions]
            sa_max = max(sa_Q_values)

            sa_max_indexes = [i for i in range(len(self.actions)) if sa_Q_values[i] == sa_max]
            i = random.choice(sa_max_indexes)
            shot = self.actions[i]

        # (x, y) хэлбэрт оруулах
        y = shot / self.env.size
        x = shot % self.env.size

        return (x, y)

    def response(self, shot, shot_resp, reward):
        # next state
        next_state = self.build_state()

        # Learn policy based on last state, action, reward
        self.learn(self.state, shot, reward, next_state)

        # limit actions according to hint
        acts = []
        hints = self.env.get_hints()
        for h in hints:
            acts.append(h.head[1]*self.env.size + h.head[0])
        self.actions = acts


    def learn(self, state1, action1, reward1, state2):
        if state1 == None or len(self.actions) == 0:
            # no previuos state
            return

        sa1 = self.q.get((state1, action1), 0.0)
        sa2_maxQ = max([self.q.get((state2, a), 0.0) for a in self.actions])

        # Q learning formula: Q(s,a) <- Q(s,a)+alpha[r+ gamma* max Q(s',a')-Q(s,a)]
        self.q[(state1, action1)] = sa1 + self.alpha * (reward1 + self.gamma*sa2_maxQ - sa1)
