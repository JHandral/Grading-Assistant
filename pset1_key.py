# Problem 1

# GRADING RUBRIC for problem 1
# 2 points possible:
# If the answer is correct, the student receives 2 points;
# If the answer clearly demonstrates effort and knowledge, the student only receives 1 point;
# Otherwise, the student receives 0 points.

# Correct answer:
def compute_slope_estimator(x, y):
	# Calculate the mean of x and y
	x_mean = np.mean(x)
	y_mean = np.mean(y)
    
	# Calculate the numerator of the slope estimator
	numerator = np.sum(x * y) - len(x) * x_mean * y_mean
    
	# Calculate the denominator of the slope estimator
	denominator = np.sum(x**2) - len(x) * x_mean**2
    
	# Calculate the slope estimator
	slope_estimator = numerator / denominator
    
	return slope_estimator

# Problem 2

# GRADING RUBRIC for problem 2
# 2 points possible:
# If the answer is correct, the student receives 2 points;
# If the answer clearly demonstrates effort and knowledge, the student only receives 1 point;
# Otherwise, the student receives 0 points.

# Correct answer:
def compute_intercept_estimator(x, y):
	# Calculate the mean of x and y
	x_mean = np.mean(x)
	y_mean = np.mean(y)
    
	# Calculate the slope estimator using the previously defined function
	slope_estimator = compute_slope_estimator(x, y)
    
	# Calculate the intercept estimator
	intercept_estimator = y_mean - slope_estimator * x_mean
    
	return intercept_estimator

# Problem 3

# GRADING RUBRIC for problem 3
# 2 points possible:
# If the answer is correct, the student receives 2 points;
# If the answer clearly demonstrates effort and knowledge, the student only receives 1 point;
# Otherwise, the student receives 0 points.

# Correct answer:
def train_model(x_vals,y_vals):
    a = compute_slope_estimator(x_vals, y_vals)
    b = compute_intercept_estimator(x_vals, y_vals)
    return (a,b)

# Problem 4

# GRADING RUBRIC for problem 4
# 2 points possible:
# If the answer is correct, the student receives 2 points;
# If the answer clearly demonstrates effort and knowledge, the student only receives 1 point;
# Otherwise, the student receives 0 points.

# Correct answer:
def dL_da(x_vals,y_vals,a,b):
    # df/da = 2(axx - xy + bx)
    return 2*sum(a*x_vals**2 - x_vals*y_vals + b*x_vals)/len(x_vals)