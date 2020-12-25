import tensorflow as tf
from tensorflow.keras import layers, models
import os
import time
from tensorflow_core.python.keras import Sequential

import load_mnist

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class LeNet(Sequential):
    def __init__(self):
        super().__init__()

        self.add(layers.Conv2D(6, (5, 5), padding="same",
                               input_shape=(28, 28, 1), activation='tanh'))
        # TODO: dynamic shape
        self.add(layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
        # self.add(layers.Activation('sigmoid'))
        self.add(layers.Conv2D(16, kernel_size=(5, 5), strides=(1, 1),
                               activation='tanh', padding='valid'))
        self.add(layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
        # self.add(layers.Activation('sigmoid'))
        self.add(layers.Flatten())
        self.add(layers.Dense(120, activation='tanh'))
        self.add(layers.Dense(84, activation='tanh'))
        self.add(layers.Dense(10, activation='softmax'))
        self.compile(optimizer=tf.keras.optimizers.Adam(0.001),
                     loss=tf.keras.losses.categorical_crossentropy,
                     metrics=[tf.keras.metrics.categorical_accuracy])

class CnNet(Sequential):
    def __init__(self, num_classes):
        super().__init__()

        self.add(layers.Conv2D(6, (5, 5), padding="same",
                               input_shape=(28, 28, 1), activation='tanh'))
        # TODO: dynamic shape
        self.add(layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
        # self.add(layers.Activation('sigmoid'))
        self.add(layers.Conv2D(16, kernel_size=(5, 5), strides=(1, 1),
                               activation='tanh', padding='valid')),
        self.add(layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
        # self.add(layers.Activation('sigmoid'))
        self.add(layers.Flatten())
        self.add(layers.Dense(120, activation='tanh'))
        self.add(layers.Dense(84, activation='tanh'))
        self.add(layers.Dense(num_classes, activation='softmax'))
        self.compile(optimizer=tf.keras.optimizers.Adam(0.001),
                     loss=tf.keras.losses.categorical_crossentropy,
                     metrics=[tf.keras.metrics.categorical_accuracy])





train_set = 'ALL' # 'EN' or 'ALL'
epoches = 20
batch_size = 100
comment = "0"

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
    train_images = load_mnist.all_train_images
    train_labels = load_mnist.all_train_labels
    test_images = load_mnist.all_test_images
    test_labels = load_mnist.all_test_labels

model = CnNet(num_classes)
model.fit(train_images, train_labels,
            epochs=epoches, batch_size=batch_size, verbose=1)

current_time = time.strftime("%d_%H_%M", time.localtime())
model.save(f'train/{train_set}_{current_time}_e{epoches}_b{batch_size}_{comment}')
model.evaluate(test_images,test_labels)


# new_model = models.load_model(f'train/res_cn')

# new_model.evaluate(load_mnist.all_train_images, load_mnist.all_test_labels,
#                batch_size=32, verbose=1)

# dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y))
# dataset = dataset.batch(32)
# dataset = dataset.repeat()
# val_dataset = tf.data.Dataset.from_tensor_slices((val_x, val_y))
# val_dataset = val_dataset.batch(32)
# val_dataset = val_dataset.repeat()
#
# model.fit(dataset, epochs=10, steps_per_epoch=30,
#           validation_data=val_dataset, validation_steps=3)
