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
                               input_shape=(28, 28, 1), activation='sigmoid'))
        # TODO: dynamic shape
        self.add(layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
        # self.add(layers.Activation('sigmoid'))
        self.add(layers.Conv2D(16, kernel_size=(5, 5), strides=(1, 1),
                               activation='sigmoid', padding='valid'))
        self.add(layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'))
        # self.add(layers.Activation('sigmoid'))
        self.add(layers.Flatten())
        self.add(layers.Dense(120, activation='tanh'))
        self.add(layers.Dense(84, activation='tanh'))
        self.add(layers.Dense(20, activation='softmax'))
        self.compile(optimizer=tf.keras.optimizers.Adam(0.001),
                     loss=tf.keras.losses.categorical_crossentropy,
                     metrics=[tf.keras.metrics.categorical_accuracy])




model = LeNet()

model.fit(load_mnist.all_train_images, load_mnist.all_train_labels,
          epochs=10, batch_size=100, verbose=1)

current_time = time.strftime("%d-%H:%M", time.localtime())
model.save(f'train/[{current_time}]res_mixed')

new_model = models.load_model(f'train/[{current_time}]res_mixed')

new_model.evaluate(load_mnist.all_train_images, load_mnist.all_test_labels,
               batch_size=32, verbose=1)

# dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y))
# dataset = dataset.batch(32)
# dataset = dataset.repeat()
# val_dataset = tf.data.Dataset.from_tensor_slices((val_x, val_y))
# val_dataset = val_dataset.batch(32)
# val_dataset = val_dataset.repeat()
#
# model.fit(dataset, epochs=10, steps_per_epoch=30,
#           validation_data=val_dataset, validation_steps=3)
