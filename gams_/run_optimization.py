#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from gams_.power_generation import model
from pyomo.opt import SolverFactory
from pyomo.core.kernel.numvalue import value


__author__ = 'David Thierry'  #: May 2018


def main():
    ipopt = SolverFactory('ipopt')
    ipopt.solve(model, tee=True)
    for key in model.X.keys():
        print('X[{}]=\t{}'.format(key, value(model.X[key])))
    for key in model.P.keys():
        print('P[{}]=\t{}'.format(key, value(model.P[key])))
    for key in model.Z.keys():
        print('Z[{}]=\t{}'.format(key, value(model.Z[key])))
    print('OILPUR =\t{}'.format(value(model.OILPUR)))


if __name__ == '__main__':
    main()



