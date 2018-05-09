# -*- coding: utf-8 -*-
#: Imports
from __future__ import division
from __future__ import print_function
from pyomo.opt import SolverFactory
from pyomo.environ import *
from pyomo.core.kernel.numvalue import value

__author__ = 'David Thierry'  #: May 2017

#: The model
model = ConcreteModel()
#: The sets
model.G = Set(initialize=['gen1', 'gen2'])
model.F = Set(initialize=['oil', 'gas'])
model.K = Set(initialize=[0, 1, 2])

#: Parameter
#: Declared manually.

model.A = Param(model.G, model.F, model.K, mutable=True)
model.A[('gen1', 'oil', 0)] = 1.4609
model.A[('gen1', 'oil', 1)] = 1.5742
model.A[('gen1', 'oil', 2)] = 0.8008

model.A[('gen1', 'gas', 0)] = 1.5742
model.A[('gen1', 'gas', 1)] = 0.16310
model.A[('gen1', 'gas', 2)] = 0.000916

model.A[('gen2', 'oil', 0)] = 0.8008
model.A[('gen2', 'oil', 1)] = 0.20310
model.A[('gen2', 'oil', 2)] = 0.000916

model.A[('gen2', 'gas', 0)] = 0.7266
model.A[('gen2', 'gas', 1)] = 0.2256
model.A[('gen2', 'gas', 2)] = 0.000778



model.PMAX = Param(model.G, mutable=True)
model.PMAX['gen1'] = 30.0
model.PMAX['gen2'] = 25.0


model.PMIN = Param(model.G, mutable=True)
model.PMIN['gen1'] = 18.0
model.PMIN['gen2'] = 14.0


model.GASSUP = Param(initialize=10.0)
model.PREQ = Param(initialize=50.0, doc='Total power output required in MW')

#: bound initializing function
def bound_rule(mod, g):
    return value(model.PMIN[g]), value(model.PMAX[g])

#: initial guess function
def init_P_rule(mod, g):
    return value(model.PMIN[g]) + value(model.PMAX[g]) * 0.5

#: Variables
model.P = Var(model.G,
              domain=PositiveReals,
              bounds=bound_rule,
              doc='Total power output of generators in MW',
              initialize=init_P_rule)
model.X = Var(model.G, model.F,
              domain=PositiveReals,
              doc='Power outputs of generators for specific fuels')
model.Z = Var(model.F,
              domain=PositiveReals,
              doc='Power outputs of generators for specific fuels')
model.OILPUR = Var(doc='Amount of fuel oil purchased')


#: Define Constraint rules.
def tpower_init(mod):
    return sum(mod.P[g] for g in mod.G) >= mod.PREQ


def _pwr_init(mod, g):
    return mod.P[g] == sum(mod.X[g, f] for f in mod.F)


def _fueluse(mod, f):
    return mod.Z[f] >= sum(mod.A[g, f, k] * mod.X[g, f]**(k) for g in mod.G for k in mod.K)


def _oiluse_init(mod):
    return mod.OILPUR == mod.Z['oil']


#: Define Constraints
model.TPOWER = Constraint(rule=tpower_init)
model.PWR = Constraint(model.G, rule=_pwr_init)
model.OILUSE = Constraint(rule=_oiluse_init)
model.FUELUSE = Constraint(model.F, rule=_fueluse)

#: Set lower and upper bounds for

model.obj_func = Objective(sense=minimize, expr=model.OILPUR)
#
