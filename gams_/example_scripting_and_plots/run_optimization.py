#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from gams_.example_scripting_and_plots.power_generation import model
from pyomo.opt import SolverFactory
from pyomo.core.kernel.numvalue import value
import matplotlib.pyplot as plt

__author__ = 'David Thierry'  #: May 2018


def main():
    ipopt = SolverFactory('ipopt')

    xlg1o = []
    xlg1g = []
    plg1 = []
    ubl = []
    for i in range(0, 20):
        ipopt.solve(model, tee=True)
        ub = (10.5 - 15) / 20 * i + 15
        print("Upper bound {}".format(ub))
        model.Z['gas'].setub(ub)
        for key in model.X.keys():
            print('X[{}]=\t{}'.format(key, value(model.X[key])))
        for key in model.P.keys():
            print('P[{}]=\t{}'.format(key, value(model.P[key])))
        for key in model.Z.keys():
            print('Z[{}]=\t{}'.format(key, value(model.Z[key])))
        print('OILPUR =\t{}'.format(value(model.OILPUR)))
        xlg1o.append(value(model.X['gen1', 'oil']))
        xlg1g.append(value(model.X['gen1', 'gas']))
        plg1.append(value(model.Z['gas']))
        ubl.append(ub)
    plt.subplot(3, 1, 1)
    plt.plot(ubl, xlg1g)
    plt.xlabel('Z upper bound')
    plt.ylabel('x g1 g')

    plt.subplot(3, 1, 2)
    plt.plot(ubl, xlg1o)
    plt.xlabel('Z upper bound')
    plt.ylabel('x g1 o')

    plt.subplot(3, 1, 3)
    plt.plot(ubl, plg1)
    plt.xlabel('Z upper bound')
    plt.ylabel('Z gas')
    plt.show()

    plt.show()



if __name__ == '__main__':
    main()
