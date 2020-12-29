import load_mnist
import numpy as np
import random
print(load_mnist.cn_test_images[0])
#
# test_labels = load_mnist.load_labels('mnist/t10k-labels.idx1-ubyte')
# groups = [[] for i in range(10)]
# for i, j in enumerate(test_labels):
#     groups[j].append(i)
#
# for i in range(10):
#     groups[i] = random.sample(groups[i],200)
#
# test_images = []
# test_labels = []
#
# for i in range(10):
#     for j in groups[i]:
#         test_labels.append(test_labels[i])
#
# print ([len(i) for i in groups])