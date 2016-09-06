#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
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

    def run(self, agent):
        # train for all variants
        for pl in self.planes:
            # play 10 times
            self.train(pl, agent, 100)

    def train(self, pl, agent, n_trials=1):
        print "Plane {}".format(pl)  # [debug]

        shot_count = 0
        stats = [[0 for i in xrange(self.env.size)] for j in xrange(self.env.size)]

        for trial in xrange(n_trials):

            self.env.new_game(pl)
            agent.reset()

            done  = False
            while not done: #
                # wait for agent to shoot
                shot = agent.next_shoot()
                shot_count += 1

                # for measurement
                stats[shot[1]][shot[0]] += 1

                # apply the shot and get reward
                resp, reward = env.shoot(shot)

                if resp == 'H':
                    done = True

                # give a response to an agent
                agent.response(shot, resp, reward)

        # print stats
        print 'Average shot', shot_count / n_trials
        print 'Hit statistics:'

        for j in range(self.env.size):
            for  i in range(self.env.size):
                pct = stats[j][i] / float(n_trials)

                if pct < 0.10:
                    sys.stdout.write('\x1b[0m   \x1b[0m')
                elif pct < 0.30:
                    sys.stdout.write('\x1b[47m   \x1b[0m')
                elif pct < 0.80:
                    sys.stdout.write('\x1b[46m   \x1b[0m')
                else:
                    sys.stdout.write('\x1b[44m   \x1b[0m')

            sys.stdout.write('\n')
            sys.stdout.flush()

    def play(self):
        pass


if __name__ == '__main__':
    env = Environment() # create a game environment

    agent = LearningAgent(env)

    player2 = HumanSimulator(env)
    player2.run(agent)

    # train
    # p = Plane((7,1), 'N')
    # player2.train(p, agent, 100)

    print '*********************'

    # for s in sorted(agent.q):
    #      print s, agent.q[s]

    # learning is done, now start playing ?
    print 'Yo wanna play with me? So draw your plane...'
