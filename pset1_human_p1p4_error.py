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
    n = len(x_vals)
    x_bar = np.mean(x_vals)
    y_bar = np.mean(y_vals)
    return (sum(x_vals*y_vals) - n*x_bar*y_bar) / (sum(x_vals**2) - n*x_bar)

# Problem 2
def compute_intercept_estimator(x_vals,y_vals):
    # Equation 5
    return np.mean(y_vals) - compute_slope_estimator(x_vals, y_vals) * np.mean(x_vals)

# Problem 3
def train_model(x_vals,y_vals):
    a = compute_slope_estimator(x_vals, y_vals)
    b = compute_intercept_estimator(x_vals, y_vals)
    return (a,b)

# Problem 4
def dL_da(x_vals,y_vals,a,b):
    # df/da = 2(axx + xy - bx)
    return 2*sum(a*x_vals**2 - x_vals*y_vals + b*x_vals)/len(x_vals)