from tensorflow.keras import layers, models
import numpy as np
from tensorflow_core.python.keras.utils import to_categorical

import load_mnist
import cv2
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

model = models.load_model('train_res/model4_061128')

def print_middle_features():
    imgs = load_mnist.cn_test_images[:1]

    conv1 = model.layers[0](imgs)
    pool1 = model.layers[1](conv1)
    conv2 = model.layers[2](pool1)
    pool2 = model.layers[3](conv2)
    flatten = model.layers[4](pool2)
    conn1 = model.layers[5](flatten)
    conn2 = model.layers[6](conn1)
    conn3 = model.layers[7](conn2)

    middle_results = [conv1, pool1, conv2, pool2, flatten, conn1, conn2, conn3]
    print([i.shape for i in middle_results])
    for i, result in enumerate(middle_results[:4]):
        result = result[0]
        feature_height = result[:, :, 0].shape[0]
        feature_num = result.shape[2]
        foo = np.ones([feature_height, 2])
        for j in range(feature_num):
            margin = np.ones([feature_height, 2])
            foo = np.hstack([foo, margin])
            foo = np.hstack([foo, np.mat(result[:, :, j])])
        cv2.imshow(f"Feature set of the {i}th layer", foo)
        cv2.waitKey()

print_middle_features()


