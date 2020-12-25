import os
import pickle

import cv2
import numpy as np
import random


# Preprocess the public dataset
# for num in range(1, 11):
#     num_folder = os.walk("EI339-CN/" + str(num) + "/testing")
#     test_group = []
#     for path, _, imgs in num_folder:
#         for i, img in enumerate(imgs):
#             img_dir = os.path.join(path,img)
#             img_ori = cv2.imread(img_dir)
#             grayImage = 255 - cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
#             ret, thresh = cv2.threshold(grayImage, 128, 0, cv2.THRESH_TOZERO)
#             cv2.imwrite(f"processed_test/{num}/{i}.png", thresh)
#
# for num in range(1, 11):
#     num_folder = os.walk("EI339-CN/" + str(num) + "/training")
#     test_group = []
#     for path, _, imgs in num_folder:
#         for i, img in enumerate(imgs):
#             img_dir = os.path.join(path,img)
#             img_ori = cv2.imread(img_dir)
#             grayImage = 255 - cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
#             ret, thresh = cv2.threshold(grayImage, 128, 0, cv2.THRESH_TOZERO)
#             cv2.imwrite(f"processed_train/{num}/{i}.png", thresh)

# Read and pack


train_labels = []
train_groups = []
for num in range(1, 11):
    num_folder = os.walk("EI339-Filtered/train/" + str(num))
    train_group = []
    for path, _, imgs in num_folder:
        for img in imgs:
            img_dir = os.path.join(path,img)
            img_ori = cv2.imread(img_dir)
            if img_ori is None:
                continue
            img_ori = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
            img_ori = img_ori.astype('float32')
            train_group.append(img_ori)
    train_labels += [num % 10 + 10 for i in range(len(train_group))]
    train_groups += train_group

random.seed(0)
random.shuffle(train_groups)
random.seed(0)
random.shuffle(train_labels)



test_labels = []
test_groups = []
for num in range(1, 11):
    num_folder = os.walk("EI339-Filtered/test/" + str(num))
    test_group = []
    for path, _, imgs in num_folder:
        for img in imgs:
            img_dir = os.path.join(path,img)
            img_ori = cv2.imread(img_dir)
            if img_ori is None:
                continue
            img_ori = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
            img_ori = img_ori.astype('float32')
            test_group.append(img_ori)
    test_labels += [num % 10 + 10 for i in range(len(test_group))]
    test_groups += test_group

random.seed(0)
random.shuffle(test_groups)
random.seed(0)
random.shuffle(test_labels)


train_groups = np.asarray(train_groups)
train_labels = np.asarray(train_labels)
test_groups = np.asarray(test_groups)
test_labels = np.asarray(test_labels)
ei339_cn = {
    "train_labels": train_labels,
    "train_groups": train_groups,
    "test_labels": test_labels,
    "test_groups": test_groups
}
dump_file = open('mnist/ei339-cn-manual.pik','wb')
pickle.dump(ei339_cn, dump_file)

