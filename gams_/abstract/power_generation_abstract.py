# -*- coding: utf-8 -*-
#: Imports
from __future__ import division
from __future__ import print_function
from pyomo.opt import SolverFactory
from pyomo.environ import *
from pyomo.core.kernel.numvalue import value

__author__ = 'David Thierry'  #: May 2017

#: The model
model = AbstractModel()
#: The sets
model.G = Set()
model.F = Set()
model.K = Set()

#: Parameter
model.A = Param(model.G, model.F, model.K)
model.PMAX = Param(model.G)
model.PMIN = Param(model.G)
model.GASSUP = Param()
model.PREQ = Param(doc='Total power output required in MW')

#: Variables
model.P = Var(model.G, domain=PositiveReals, doc='Total power output of generators in MW')
model.X = Var(model.G, model.F, domain=PositiveReals, doc='Power outputs of generators for specific fuels')
model.Z = Var(model.F, domain=PositiveReals, doc='Power outputs of generators for specific fuels')
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
for i in model.G:
    model.P[i].setlb(model.PMIN[i])
    model.P[i].setub(model.PMAX[i])
    model.P[i].set_value((model.PMIN[i] + model.PMAX[i]) * 0.5)

model.obj_func = Objective(sense=minimize, expr=model.OILPUR)
#
