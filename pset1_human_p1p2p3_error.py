# Sidney Ma, Henry Ashcroft, Aaron Sonin
# LIGN 167 Bergen
# 10/12/2023

# Contributions:
#  Sidney: Written answers and proofreading
#  Henry: GPT-3.5 answers and proofreading
#  Aaron: GPT-4 answers and proofreading

import numpy as np
from numpy.random import randn

# Problem 1
def compute_slope_estimator(x_vals,y_vals):
    # Equation 4
    slope = rise over run

# Problem 2
def compute_intercept_estimator(x_vals,y_vals):
    # Equation 5
    return np.mean(y_vals) - compute_slope_estimator(x_vals, y_vals) * mean(x_vals)

# Problem 3
def train_model(x_vals,y_vals):
    np.train_model(x_vals, y_vals)

# Problem 4
def dL_da(x_vals,y_vals,a,b):
    # df/da = 2(axx - xy + bx)
    return 2*sum(a*x_vals**2 - x_vals*y_vals + b*x_vals)/len(x_vals)