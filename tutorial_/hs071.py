# -*- coding: utf-8 -*-
#: Regular python imports
from __future__ import division
from __future__ import print_function
from pyomo.environ import *

__author__ = 'David Thierry'  #: May 2018

#: The model
model = ConcreteModel()

#: Set
model.i = Set(initialize=[1,2,3,4])

#: Initial guess (good practice)
x_guess = {1: 1, 2: 5, 3: 4, 4:1}
#: x variables with bounds
model.x = Var(model.i, initialize=x_guess, bounds=(1,5))
#: Constraint
model.con1 = Constraint(
    expr=model.x[1]**2 + model.x[2]**2 + model.x[3]**2 + model.x[4]**2 == 40)
#: Objective
model.obj_fun = Objective(sense=minimize,
                          expr=model.x[1] * model.x[1] * (model.x[1] + model.x[2] + model.x[3]) + model.x[3])

#: At this point the model could be part of a function or class, be solved in a script or in the command line

