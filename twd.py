# -*- coding: utf-8 -*-
"""
twd
=====
Firstly the space structure of set pair information granule can be divided into positive granule,
negative granule, different granule, which were similar and slightly different with three regions of
generalized three-way decision. The three kinds of information granules in set pair information granule space
were built based on certain positive degree, negative degree and different degree.
Secondly, according to the given threshold, set pair information granule is divided into
mutually disjointing positive region, negative region and different region.

Example
----------------------------
    >>> from twd import TWD
    >>> model = TWD(Lambda=.6, Gamma=.15, PP=0, BP=25, NP=5, PN=10, BN=100, NN=0)
    >>> model.predict(x_train, y_train, x_test)

Copyright Zeroto521
----------------------------
"""

import numpy as np


__version__ = '0.1.0'
__license__ = 'MIT'
__short_description__ = 'twd means Model of three-way decision'


class TWD():
    def __init__(self, Lambda=.6, Gamma=.15, PP=0, BP=25, NP=5, PN=10, BN=100, NN=0, a='1', b='-', c='0'):
        """twd means Model of three-way decision.

        twd
        =====
        Firstly the space structure of set pair information granule can be divided into positive granule,
        negative granule, different granule, which were similar and slightly different with three regions of
        generalized three-way decision. The three kinds of information granules in set pair information granule space
        were built based on certain positive degree, negative degree and different degree.
        Secondly, according to the given threshold, set pair information granule is divided into
        mutually disjointing positive region, negative region and different region.

        Example
        ----------------------------
            >>> from twd import TWD
            >>> model = TWD(Lambda=.6, Gamma=.15, PP=0, BP=25, NP=5, PN=10, BN=100, NN=0)
            >>> model.predict(x_train, y_train, x_test)

        Keyword Arguments
        ----------------------------
            Lambda {float} -- (default: {.6})
            Gamma {float} -- (default: {.15})
            PP {int} -- (default: {0})
            BP {int} -- (default: {25})
            NP {int} -- (default: {5})
            PN {int} -- (default: {10})
            BN {int} -- (default: {100})
            NN {int} -- (default: {0})
            a {str} -- (default: {'1'})
            b {str} -- (default: {'-'})
            c {str} -- (default: {'0'})
        """

        self.Lambda = Lambda
        self.Gamma = Gamma
        self.PP = PP
        self.BP = BP
        self.NP = NP
        self.PN = PN
        self.BN = BN
        self.NN = NN

        # define the flag make the model more universal
        self.a = a
        self.b = b
        self.c = c

    def _relevant_degree_helper(self, x_train, x_pred):
        a, c = 0, 0

        for i, j in zip(x_train, x_pred):
            a += 1 if i == j else 0

            if (i == self.c and j == self.a) or (i == self.a and j == self.c):
                c += 1

        a /= len(x_pred)
        c /= len(x_pred)
        b = 1 - a - c

        return a, b, c

    def _divide_regions(self, rdegrees):
        # 划分域
        S = [index for index, (a, _, _) in enumerate(rdegrees)
             if a >= self.Lambda]
        O = [index for index, (a, _, c) in enumerate(rdegrees)
             if a < self.Lambda and c >= self.Gamma]
        U = [index for index, (a, _, c) in enumerate(rdegrees)
             if a < self.Lambda and c < self.Gamma]

        return S, O, U

    def _intersect(self, x, y):
        return set(x).intersection(set(y))

    def _loss(self, S, O, U, X, anti_X):
        # 决策损失函数
        p_s, n_s, p_o, n_o, ab = 100, 100, 100, 100, 100

        if len(S) != 0:
            x_s = self._intersect(X, S)
            anti_x_s = self._intersect(anti_X, S)
            p_s = self.PP * len(x_s) / len(S) + self.PN * \
                len(anti_x_s) / len(S)
            n_s = self.NP * len(x_s) / len(S) + self.NN * \
                len(anti_x_s) / len(S)

        if len(O) != 0:
            x_o = self._intersect(X, O)
            anti_x_o = self._intersect(anti_X, O)
            p_o = self.PP * len(x_o) / len(O) + self.PN * \
                len(anti_x_o) / len(O)
            n_o = self.NP * len(x_o) / len(O) + self.BN * \
                len(anti_x_o) / len(O)

        if len(U) != 0:
            x_u = self._intersect(X, U)
            anti_x_u = self._intersect(anti_X, U)
            ab = self.BP * len(x_u) / len(U) + self.BN * len(anti_x_u) / len(U)

        return p_s, n_s, p_o, n_o, ab

    def _check_set(self, s):
        if self.a in s:
            xk = self.a
        elif self.c in s:
            xk = self.c
        else:
            xk = self.b

        return xk

    def _check_equal(self, r1, r2, r3):
        rs = min(r1, r2, r3)
        if r1 == rs:
            xk = self.a
        elif r2 == rs:
            xk = self.c
        else:
            xk = self.b

        return xk

    def _decide(self, y_train, bpd, bnd, S, O, U, I, D):
        i_set = set(y_train[I])
        d_set = set(y_train[D])
        index = np.arange(len(y_train))
        X = index[np.where(y_train == self.a)]
        anti_X = index[np.where(y_train != self.a)]

        if bpd < bnd:
            if len(d_set) == 1:
                xk = self._check_set(d_set)
            else:
                _, _, r1, r2, r3 = self._loss(S, O, U, X, anti_X)
                xk = self._check_equal(r1, r2, r3)
        elif bpd > bnd:
            if len(i_set) == 1:
                xk = self._check_set(i_set)
            else:
                r1, r2, _, _, r3 = self._loss(S, O, U, X, anti_X)
                xk = self._check_equal(r1, r2, r3)
        else:
            if len(i_set) == 1 and len(d_set) == 1 and set((self.a, self.c)) == (i_set | d_set):
                if self.a in i_set:
                    xk = self.a
                else:
                    xk = self.c
            else:
                xk = self.b

        return xk

    def _predict(self, x_pred, x_train, y_train):
        rdegrees = np.apply_along_axis(
            self._relevant_degree_helper, 1, x_train, x_pred=x_pred)

        S, O, U = self._divide_regions(rdegrees)

        bpd = max(rdegrees[:, 0])  # 最大正同度
        bnd = max(rdegrees[:, -1])  # 最大负反度

        index = np.arange(len(rdegrees))
        I = index[np.where(rdegrees[:, 0] == bpd)]  # 最大正同类
        D = index[np.where(rdegrees[:, -1] == bnd)]  # 最大负反类

        Xk = self._decide(y_train, bpd, bnd, S, O, U, I, D)

        return Xk

    def predict(self, x_train, y_train, x_pred):
        Xks = np.apply_along_axis(
            self._predict, 1, x_pred,
            x_train=x_train, y_train=y_train)

        return Xks
