import pickle
import random
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


def en_sample(images,labels,sample_num):
    groups = [[] for i in range(10)]
    for i, j in enumerate(labels):
        groups[j].append(i)

    for i in range(10):
        groups[i] = random.sample(groups[i], sample_num)

    sample_images = []
    sample_labels = []
    for i in range(10):
        for j in groups[i]:
            sample_images.append(images[j])
            sample_labels.append(labels[j])

    random.seed(0)
    random.shuffle(sample_images)
    random.seed(0)
    random.shuffle(sample_labels)

    return np.asarray(sample_images), np.asarray(sample_labels)


# 200 per test
# 700 per train
filename_train_images = 'mnist/train-images.idx3-ubyte'
filename_train_labels = 'mnist/train-labels.idx1-ubyte'
filename_test_images = 'mnist/t10k-images.idx3-ubyte'
filename_test_labels = 'mnist/t10k-labels.idx1-ubyte'
train_images = load_images(filename_train_images)
train_images = train_images[:, :, :, np.newaxis]
train_labels = load_labels(filename_train_labels)
en_train_images, en_train_labels = en_sample(train_images, train_labels, 700)
test_images = load_images(filename_test_images)
test_images = test_images[:, :, :, np.newaxis]
test_labels = load_labels(filename_test_labels)
en_test_images, en_test_labels = en_sample(test_images, test_labels, 200)

cn_train_labels, cn_train_images, \
    cn_test_labels, cn_test_images = load_cn_dataset('mnist/ei339-cn-manual.pik')
cn_test_images = cn_test_images[:, :, :, np.newaxis]
cn_train_images = cn_train_images[:, :, :, np.newaxis]

# Data normalization
train_images = train_images.astype('float32')
en_train_images = en_train_images.astype('float32')
test_images = test_images.astype('float32')
en_test_images = en_test_images.astype('float32')
cn_train_images = cn_train_images.astype('float32')
cn_test_images = cn_test_images.astype('float32')
train_images /= 255
test_images /= 255
en_train_images /= 255
en_test_images /= 255
cn_train_images /= 255
cn_test_images /= 255


all_test_images = np.concatenate((test_images, cn_test_images))
all_test_labels = np.concatenate((test_labels, cn_test_labels))
all_train_images = np.concatenate((train_images, cn_train_images))
all_train_labels = np.concatenate((train_labels, cn_train_labels))

normal_test_images = np.concatenate((en_test_images, cn_test_images))
normal_test_labels = np.concatenate((en_test_labels, cn_test_labels))
normal_train_images = np.concatenate((en_train_images, cn_train_images))
normal_train_labels = np.concatenate((en_train_labels, cn_train_labels))

num_classes = 10
train_labels = to_categorical(train_labels, num_classes)
test_labels = to_categorical(test_labels, num_classes)
cn_train_labels = to_categorical(cn_train_labels-10, num_classes)
cn_test_labels = to_categorical(cn_test_labels-10, num_classes)

all_num_classes = 20
all_train_labels = to_categorical(all_train_labels, all_num_classes)
all_test_labels = to_categorical(all_test_labels, all_num_classes)
normal_train_labels = to_categorical(normal_train_labels, all_num_classes)
normal_test_labels = to_categorical(normal_test_labels, all_num_classes)



# round to 0 or 1
# train_images = np.around(train_images)
# test_images = np.around(test_images)
# cn_train_images = np.around(cn_train_images)
# cn_test_images = np.around(cn_test_images)


normal_test_images = np.around(normal_test_images)
normal_train_images = np.around(normal_train_images)