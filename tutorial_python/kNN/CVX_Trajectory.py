import numpy as np
import matplotlib.pyplot as plt
import cvxpy
from cvxpy import *
from mpl_toolkits.mplot3d import Axes3D


dims = 3
T = 20
D = 0.1   # 100

def solve_subproblem(pk, p0, pT, c, verbose = False):
	p = Variable((T,dims))
	obj = sum_squares(diff(p, k = 1, axis = 1))

	constr = []
	for t in range(T):
		for i in range(c.shape[0]):
			constr += [D**2 - np.square((pk[t,:] - c[i,:])).sum() - 2*(pk[t,:] - c[i,:]).T*(p[t,:] - pk[t,:]) <= 0]
	constr += [p[0,:] == p0, p[T-1,:] == pT]
	prob = Problem(Minimize(obj), constr)
	prob.solve(solver = "ECOS")
	# if verbose:
	# 	print("Objective:", prob.value)
	return p.value

def cvx_ccv(p_init, p_start, p_end, obstacles, iters = 100, verbose = False):
	path = p_init
	for i in range(iters):
		path = solve_subproblem(path, p_start, p_end, obstacles, verbose)
		if path is None:
			raise Exception("Failed to solve subproblem")
	return path

# def trajectory_search():
# 	np.random.seed(1)
# 	nobs = 10
# 	mu = np.array([0.5, 0.5, 0.5])
# 	# obstacles = np.random.uniform(0, 1, size = (nobs, dims))
# 	obstacles = np.random.multivariate_normal(mu, 0.002*np.eye(3), size = nobs)
# 	# obstacles = np.r_[obstacles, np.array([[0.5, 0.5, 0.5]])]
# 	p_start = np.zeros(3)
# 	p_end = np.ones(3)
# 	p_init = np.array(3*[np.linspace(0,1,T)]).T
# 	path = cvx_ccv(p_init, p_start, p_end, obstacles, iters = 10, verbose = True)
# 	return path
np.random.seed(1)
nobs = 10
mu = np.array([0.5, 0.5, 0.5])
# obstacles = np.random.uniform(0, 1, size = (nobs, dims))
obstacles = np.random.multivariate_normal(mu, 0.002*np.eye(3), size = nobs)
# obstacles = np.r_[obstacles, np.array([[0.5, 0.5, 0.5]])]
p_start = np.zeros(3)
p_end = np.ones(3)
p_init = np.array(3*[np.linspace(0,1,T)]).T
path = cvx_ccv(p_init, p_start, p_end, obstacles, iters = 10, verbose = True)
#path = trajectory_search()
#print(path*300)
fig = plt.figure()
ax = fig.add_subplot(111, projection = "3d")
ax.plot(path[:,0], path[:,1], path[:,2])
ax.scatter(obstacles[:,0], obstacles[:,1], obstacles[:,2], color = "red")
plt.title("Optimal Trajectory")
plt.show()
