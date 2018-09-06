import numpy as np
import kNN.kNNtest as knn

x,y = knn.implement_kNN(np.load('policeman_lr.npy'))
print(x,y)