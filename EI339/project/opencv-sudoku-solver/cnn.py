import tensorflow as tf
from tensorflow.keras import layers, models
import os
import time
from tensorflow_core.python.keras import Sequential
from tensorflow_core.python.keras.callbacks import *
from tensorflow_core.python.keras.utils import to_categorical

import load_mnist

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


# class LeNet(Sequential):
#     def __init__(self):
#         super().__init__()
#         self.add(layers.Conv2D(6, (5, 5), padding="same",
#                                input_shape=(28, 28, 1), activation='tanh'))
#         self.add(layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
#         self.add(layers.Conv2D(16, kernel_size=(5, 5), strides=(1, 1),
#                                activation='tanh', padding='valid'))
#         self.add(layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
#         self.add(layers.Flatten())
#         self.add(layers.Dense(120, activation='tanh'))
#         self.add(layers.Dense(84, activation='tanh'))
#         self.add(layers.Dense(10, activation='softmax'))
#         self.compile(optimizer=tf.keras.optimizers.Adam(0.001),
#                      loss=tf.keras.losses.categorical_crossentropy,
#                      metrics=[tf.keras.metrics.categorical_accuracy])

class CnNet(Sequential):
    def __init__(self, num_classes):
        super().__init__()

        # self.add(layers.Conv2D(6, (5, 5), padding="same",
        #                        input_shape=(28, 28, 1), activation='tanh'))
        self.add(layers.Conv2D(6, (5, 5), padding="same",
                               input_shape=(28, 28, 1), activation='tanh'))
        self.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
        # self.add(layers.Conv2D(16, kernel_size=(5, 5), strides=(1, 1),
        #                        activation='tanh', padding='valid')),
        self.add(layers.Conv2D(16, kernel_size=(5, 5), strides=(1, 1),
                               activation='tanh', padding='valid')),
        self.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))


        self.add(layers.Flatten())
        self.add(layers.Dense(120, activation='tanh'))
        self.add(layers.Dense(84, activation='tanh'))
        # self.add(layers.Dense(240, activation='tanh'))
        # self.add(layers.Dense(128, activation='tanh'))
        self.add(layers.Dense(num_classes, activation='softmax'))
        self.compile(optimizer=tf.keras.optimizers.Adam(0.001),
                     loss=tf.keras.losses.categorical_crossentropy,
                     metrics=[tf.keras.metrics.categorical_accuracy])


model = CnNet(20)
model.summary()



train_set = 'ALL' # 'EN' or 'ALL'
epoches = 10
batch_size = 100
comment = "maxpool_original"

if train_set == "CN":
    num_classes = 10
    train_images = load_mnist.cn_train_images
    train_labels = load_mnist.cn_train_labels
    test_images = load_mnist.cn_test_images
    test_labels = load_mnist.cn_test_labels
elif train_set == "EN":
    num_classes = 10
    train_images = load_mnist.train_images
    train_labels = load_mnist.train_labels
    test_images = load_mnist.test_images
    test_labels = load_mnist.test_labels
else:
    num_classes = 20
    # train_images = load_mnist.normal_train_images
    # train_labels = load_mnist.normal_train_labels
    # print(train_images[0],train_labels[0])
    # test_images = load_mnist.normal_test_images
    # test_labels = load_mnist.normal_test_labels
    train_images = load_mnist.all_train_images
    train_labels = load_mnist.all_train_labels
    test_images = load_mnist.all_test_images
    test_labels = load_mnist.all_test_labels

model = CnNet(num_classes)


current_time = time.strftime("%d%H%M", time.localtime())
save_path = f'train/{train_set}_{comment}_{current_time}'
os.mkdir(save_path)


logger_callback = CSVLogger(save_path+"/log.csv")

model.fit(train_images, train_labels,
            epochs=epoches, batch_size=batch_size, verbose=1, callbacks=[logger_callback])

model.save(save_path)
# model.evaluate(test_images,test_labels)


_, _, cn_test_labels, _ = load_mnist.load_cn_dataset('mnist/ei339-cn-manual.pik')
cn_test_labels = to_categorical(cn_test_labels, 20)


eval_res = model.evaluate(load_mnist.cn_test_images, cn_test_labels)

with open(save_path+"/log.csv", "a") as f:
    f.write(str(eval_res))
    f.write("\n")
    model.summary(print_fn=lambda x: f.write(x + '\n'))
