#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import random
import importlib
from environment import Environment, Plane
from agent import LearningAgent

class HumanSimulator(object):
    """Simulates a human player"""

    def __init__(self, env):
        self.env = env

        self.planes = self.env.all_planes()

    def run(self, agent, n_trials=1):
        # loop over all variants
        for pl in self.planes:
            print "Plane {}".format(pl)  # [debug]

            self.train(pl, agent, n_trials)

            # print performance
            for i in range(self.env.size):
                print self.env.board[i]


    def train(self, pl, agent, n_trials=1):
        for trial in xrange(n_trials):
            #pl = self.env.random_plane()
            self.env.new_game(pl)
            agent.reset()

            done  = False
            shot_count = 0

            while not done: #
                # wait for agent to shoot
                shot = agent.next_shoot()
                shot_count += 1

                # apply the shot and get reward
                resp, reward = env.shoot(shot)

                if resp == 'H':
                    done = True

                # give a response to an agent
                agent.response(shot, resp, reward)

            #print 'Total shot', shot_count #, agent.q

    def play(self):
        pass


if __name__ == '__main__':
    env = Environment() # create a game environment

    agent = LearningAgent(env)

    player2 = HumanSimulator(env)
    player2.run(agent, n_trials=100) # Run the agent for a finite number of trials

    print '*********************'

    # for s in sorted(agent.q):
    #     print s, agent.q[s]

    # learning is done, now start playing ?
    print 'Yo wanna play with me? So draw your plane...'
