#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import math

class Plane(object):
    """Plane object"""
    degrees = {'N': 0, 'E': 90, 'S': 180, 'W': -90}
    body = [(-2,1), (-1,1), (0,1), (1,1), (2,1), (0,2), (-1,3), (0,3), (1,3)] # head relative points

    def __init__(self, head, direction):
        self.head = head
        self.direction = direction

        # rotate the plane
        radian = self.degrees[self.direction] * math.pi / 180
        self.body = [( round(p[0]*math.cos(radian)-p[1]*math.sin(radian)),
            round(p[0]*math.sin(radian)+p[1]*math.cos(radian)))
            for p in self.body]

    def check(self, shot):
        if self.head == shot:
            return 'H' # head shot

        for p in self.body:
            if shot[0] == self.head[0] + p[0] and shot[1] == self.head[1] + p[1]:
                return 'B' # body shot
        # miss
        return 'M'

    def __str__(self):
        return "{}{}".format(self.direction, self.head)

    def __repr__(self):
        return self.__str__()

class Environment(object):
    """Game environment"""
    directions = ['E', 'N', 'W', 'S']
    size = 10


    def __init__(self):
        pass

    def new_game(self, plane):
        self.plane = plane

        self.board = [[' ' for i in xrange(self.size)] for j in xrange(self.size)]

        self.hints = [] # hints for head positions
        self._update_hints(None, None)

    def shoot(self, shot):

        reward = 0.0
        hint_old = len(self.hints)
        shot_resp = self.plane.check(shot)

        # reward
        if shot_resp == 'H': # head shot
            reward = 100.0
            self.board[shot[1]][shot[0]] = shot_resp
        else:
            #  -10000.0 for repeated shot
            if self.board[shot[1]][shot[0]] != ' ':
                reward = -1000.0
            else:
                self._update_hints(shot, shot_resp)
                reward = hint_old - len(self.hints)

                # old reward policy
                # if shot_resp == 'B':
                #     reward = 10.0
                # elif shot_resp == 'M':
                #     reward = -1.0

            # update the board
            self.board[shot[1]][shot[0]] = shot_resp

        # debug
        # print shot, shot_resp, reward
        # print self.hints

        return shot_resp, reward

        # for next shot
    def get_hints(self):
        return self.hints

    def get_board(self):
        return self.board

    def _update_hints(self, shot, shot_resp):
        if len(self.hints) == 0:
            self.hints = self.all_planes()
        else:
            hints_1 = []
            for pl in self.hints:
                if pl.check(shot) == shot_resp:
                    hints_1.append(pl)
            self.hints = hints_1

    def all_planes(self):
        planes = []

        for h in range(self.size * self.size):
            for d in self.directions:
                # check if valid
                if Environment.valid(h, d):
                    p = Plane( (h % 10, h / 10), d)
                    planes.append(p)
        return planes



    # display the environment
    def show(self):
        matrix = ['_' for i in xrange(self.size * self.size)]
        matrix[self.plane.head[1]*self.size + self.plane.head[0]] = 'H'

        for p in self.plane.body:
            x = self.plane.head[0] + p[0]
            y = self.plane.head[1] + p[1]
            matrix[ int(y*self.size + x) ] = 'B'

        # TODO: show shots as '*'

        for i in xrange(self.size):
            for j in xrange(self.size):
                print matrix[i*self.size + j],

            print '\n'

    @classmethod
    def random_plane(cls):
        h = random.choice(range(Environment.size * Environment.size))
        d = random.choice(Environment.directions)

        # repeat until valid
        while not Environment.valid(h, d):
            h = random.choice(range(Environment.size * Environment.size))
            d = random.choice(Environment.directions)

        return Plane((h % 10, h / 10), d)


    @classmethod
    def valid(cls, head, direction):
        x = head % Environment.size
        y = head / Environment.size

        if direction == 'N':
            return 1 < x and x < 8 and y < 7

        if direction == 'S':
            return 1 < x and x < 8 and 2 < y

        if direction == 'E':
            return 1 < y and y < 8 and 2 < x

        if direction == 'W':
            return 1 < y and y < 8 and x < 7

        return False
