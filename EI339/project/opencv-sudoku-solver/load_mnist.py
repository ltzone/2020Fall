import pickle

import numpy as np
import struct
from tensorflow.keras.utils import to_categorical


def load_images(file_name):
    binfile = open(file_name, 'rb')
    buffers = binfile.read()
    magic, num, rows, cols = struct.unpack_from('>IIII', buffers, 0)
    bits = num * rows * cols
    images = struct.unpack_from('>' + str(bits) + 'B', buffers, struct.calcsize('>IIII'))
    binfile.close()
    images = np.reshape(images, [num, rows, cols])
    return images


def load_labels(file_name):
    binfile = open(file_name, 'rb')
    buffers = binfile.read()
    magic, num = struct.unpack_from('>II', buffers, 0)
    labels = struct.unpack_from('>' + str(num) + "B", buffers, struct.calcsize('>II'))
    binfile.close()
    labels = np.reshape(labels, [num])
    return labels


def load_cn_dataset(filename='mnist/ei339-cn-manual.pik'):
    input_file = open(filename, 'rb')
    input = pickle.load(input_file)
    input_file.close()
    return (input["train_labels"], input["train_groups"],
            input["test_labels"], input["test_groups"])


filename_train_images = 'mnist/train-images.idx3-ubyte'
filename_train_labels = 'mnist/train-labels.idx1-ubyte'
filename_test_images = 'mnist/t10k-images.idx3-ubyte'
filename_test_labels = 'mnist/t10k-labels.idx1-ubyte'
train_images = load_images(filename_train_images)
train_images = train_images[:, :, :, np.newaxis]
train_labels = load_labels(filename_train_labels)
test_images = load_images(filename_test_images)
test_images = test_images[:, :, :, np.newaxis]
test_labels = load_labels(filename_test_labels)

cn_train_labels, cn_train_images, \
    cn_test_labels, cn_test_images = load_cn_dataset('mnist/ei339-cn-manual.pik')
cn_test_images = cn_test_images[:, :, :, np.newaxis]
cn_train_images = cn_train_images[:, :, :, np.newaxis]

# Data normalization
train_images = train_images.astype('float32')
test_images = test_images.astype('float32')
train_images /= 255
test_images /= 255

all_test_images = np.concatenate((test_images, cn_test_images))
all_test_labels = np.concatenate((test_labels, cn_test_labels))
all_train_images = np.concatenate((train_images, cn_train_images))
all_train_labels = np.concatenate((train_labels, cn_train_labels))

num_classes = 10
train_labels = to_categorical(train_labels, num_classes)
test_labels = to_categorical(test_labels, num_classes)
cn_train_labels = to_categorical(cn_train_labels-10, num_classes)
cn_test_labels = to_categorical(cn_test_labels-10, num_classes)

all_num_classes = 20
all_train_labels = to_categorical(all_train_labels, all_num_classes)
all_test_labels = to_categorical(all_test_labels, all_num_classes)

cn_train_images = cn_train_images.astype('float32')
cn_test_images = cn_test_images.astype('float32')
cn_train_images /= 255
cn_test_images /= 255

# round to 0 or 1
train_images = np.around(train_images)
test_images = np.around(test_images)
cn_train_images = np.around(cn_train_images)
cn_test_images = np.around(cn_test_images)
