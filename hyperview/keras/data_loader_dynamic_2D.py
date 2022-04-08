"""
This code is generated by Ridvan Salih KUZU @DLR
LAST EDITED:  01.06.2021
ABOUT SCRIPT:
It defines training, validation and evaluation data loader classes and functions
"""

import numpy as np
import pandas as pd
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.image import img_to_array,load_img
from numpy.random import randint
import glob
from sklearn.model_selection import train_test_split
from pathlib import Path
import random
import tensorflow as tf
import os
from glob import glob
import random
import albumentations as A


class DataGenerator():
    """
    THIS CLASS ORCHESTRATES THE TRAINING, VALIDATION, AND TEST DATA GENERATORS
    """
    def __init__(self, train_dir, label_dir, eval_dir,valid_size=0.2,image_shape=(128,128), batch_size=16,self_supervised=False):

        self.train_dir = train_dir
        self.label_dir = label_dir
        self.eval_dir = eval_dir
        self.batch_size = batch_size

        train_stats_log = '{}/stats.npy'.format(train_dir)
        eval_stats_log = '{}/stats.npy'.format(eval_dir)

        if (not os.path.exists(train_stats_log)):
            train_stats = DataReader._get_stats(train_dir)
            np.save(train_stats_log, train_stats)
        if (not os.path.exists(eval_stats_log)):
            eval_stats = DataReader._get_stats(eval_dir)
            np.save(eval_stats_log, eval_stats)

        self.train_stats = np.load(train_stats_log)
        self.eval_stats = np.load(eval_stats_log)
        tr_trans, val_trans, eval_trans = DataGenerator._init_transform(image_shape, self.train_stats, self.eval_stats)

        train_files = DataGenerator._load_data(train_dir)
        train_labels = DataGenerator._load_gt(label_dir)
        # train_labels = np.vsplit(train_labels, len(train_labels))
        train_files, valid_files, train_labels, valid_labels = train_test_split(train_files, train_labels,test_size=valid_size, random_state=42)

        eval_files = DataGenerator._load_data(eval_dir)
        eval_labels = np.zeros((len(eval_files),train_labels.shape[-1]))

        if self_supervised:
            train_files=np.concatenate([train_files,eval_files])
            train_labels = np.concatenate([train_labels, eval_labels])

        self.train_reader, self.train_len = DataGenerator._get_data_reader(train_files, train_labels, batch_size, tr_trans, image_shape,ext_aug=True,eval=False, stats=self.train_stats,self_supervised=self_supervised,drop_reminder=True,preload=False)
        self.valid_reader,self.valid_len = DataGenerator._get_data_reader(valid_files, valid_labels, batch_size, val_trans,image_shape, ext_aug=True,eval=False, stats=self.train_stats,self_supervised=self_supervised,drop_reminder=True,preload=False)

        if not self_supervised:
            self.evalid_reader,self.evalid_len = DataGenerator._get_data_reader(valid_files, valid_labels, batch_size, eval_trans,image_shape, ext_aug=False,eval=False, stats=self.train_stats, self_supervised=self_supervised,drop_reminder=True,preload=False)
            self.eval_reader,self.eval_len = DataGenerator._get_data_reader(eval_files, eval_labels, 1, eval_trans, image_shape,ext_aug=False, eval=True, stats=self.eval_stats,self_supervised=self_supervised,drop_reminder=False,preload=False)

        self.image_shape, self.label_shape = DataGenerator._get_dataset_features(self.valid_reader,self_supervised=self_supervised)

    @staticmethod
    def _get_dataset_features(reader,self_supervised):
        for feature, mask in reader:
        #for feature, mask, in reader.take(1):
            if self_supervised:
                image_shape = tuple([1, feature[0].shape[-3], feature[0].shape[-2], feature[0].shape[-1]])
            else:
                image_shape = tuple([1, feature.shape[-3], feature.shape[-2], feature.shape[-1]])
            label_shape = mask.shape[-1]
            return image_shape, label_shape,


    @staticmethod
    def _get_data_reader(train_files, train_labels, batch_size, tr_trans, image_shape,ext_aug, eval, stats,self_supervised,drop_reminder,preload):
        '''
           THIS FUNCTION SELECT THE GENERATOR TO BE RETURNED BY CONSIDERING IF TRAINING IS DISTRIBUTED OVER MULTIPLE GPU OR NOT.
           :param type: 'train', 'valid' or 'test' type
           :return: returns one of the generator type
          '''
        gen = DataReader(train_files, train_labels, batch_size, tr_trans, image_shape,ext_aug,eval, stats,self_supervised,drop_reminder,preload)
        gen_len=len(gen)

        if True:
            gen = DataGenerator.multi_generator(gen,self_supervised,eval)
        return gen,gen_len

    @staticmethod
    def multi_generator(data_gen,self_supervised,eval):
        '''
        THIS FUNCTION CONVERTS DATA GENERATOR FOR MULTIPLE GPU COMPATIBILITY.
        :param data_gen: 'train', 'valid' or 'test' generator
        :return: returns the generator with multi-gpu distribution policy
        '''

        if not self_supervised:
            if not eval:
                dataset = tf.data.Dataset.from_generator(data_gen.generator,
                                                 output_types=(tf.float64, tf.float64),
                                                 output_shapes=(tf.TensorShape([None, None,None, None, None]),
                                                                tf.TensorShape([None, None]))).take(data_gen.__len__())
            else:
                dataset = tf.data.Dataset.from_generator(data_gen.generator,
                                                         output_types=(tf.float64, tf.float64,tf.string),
                                                         output_shapes=(tf.TensorShape([None, None, None, None, None]),
                                                                        tf.TensorShape([None, None]),tf.TensorShape([None]))).take(data_gen.__len__())

        else:
            dataset = tf.data.Dataset.from_generator(data_gen.generator,
                                                     output_types=((tf.float64,tf.float64), tf.float64),
                                                     output_shapes=((tf.TensorShape([None, None, None, None, None]),tf.TensorShape([None, None, None, None, None])),
                                                                    tf.TensorShape([None, None]))).take(data_gen.__len__())

        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
        return dataset.with_options(options)

    @staticmethod
    def _load_data(directory: str):
        all_files = np.array(
            sorted(
                glob(os.path.join(directory, "*.npz")),
                key=lambda x: int(os.path.basename(x).replace(".npz", "")),
            )
        )
        return all_files

    @staticmethod
    def _load_gt(file_path: str):
        """Load labels for train set from the ground truth file.
        Args:
            file_path (str): Path to the ground truth .csv file.
        Returns:
            [type]: 2D numpy array with soil properties levels
        """
        gt_file = pd.read_csv(file_path)
        labels = gt_file[["P", "K", "Mg", "pH"]].values / np.array([325, 625, 400, 7.8])
        return labels

    @staticmethod
    def _init_transform(image_shape, train_stats, eval_stats):
        train_transform = A.Compose([
            A.Resize(image_shape[0], image_shape[1]),
            # A.Normalize(mean=train_stats[0]*train_stats[2], std=train_stats[1]*train_stats[2], max_pixel_value=1),
            A.GaussNoise(var_limit=0.000025, p=0.5),
            A.RandomRotate90(p=0.5),
            # A.Rotate(),
            A.RandomResizedCrop(image_shape[0], image_shape[1], ratio=(0.95, 1.05), p=0.5),
            A.Flip(p=0.5),
            A.ShiftScaleRotate(rotate_limit=90, shift_limit_x=0.05, shift_limit_y=0.05, p=0.5),
            # A.RandomBrightnessContrast(),

        ])

        valid_transform = A.Compose([
            A.Resize(image_shape[0], image_shape[1]),
            # A.Normalize(mean=train_stats[0]*train_stats[2], std=train_stats[1]*train_stats[2], max_pixel_value=1),
            A.GaussNoise(var_limit=0.000025, p=0.5),
            A.RandomRotate90(p=0.5),
            A.RandomResizedCrop(image_shape[0], image_shape[1], ratio=(0.95, 1.05), p=0.5),
            A.Flip(p=0.5),
            A.ShiftScaleRotate(rotate_limit=90, shift_limit_x=0.05, shift_limit_y=0.05, p=0.5),

        ])

        eval_transform = A.Compose([
            A.Resize(image_shape[0], image_shape[1]),
            # A.Normalize(mean=eval_stats[0]*eval_stats[2], std=eval_stats[1]*eval_stats[2], max_pixel_value=1)
        ])

        return train_transform, valid_transform, eval_transform


class DataReader(Sequence):
    """
    THIS CLASS BUILDS A DATA GENERATOR FOR UNET-BASED ARCHITECTURES.
    """
    def __init__(self, files, labels, batch_size, transform, image_shape, ext_aug=True, eval=False,stats=None,self_supervised=False,drop_reminder=True,preload=True):

        self.files=files
        self.augment_time=1
        self.labels = labels
        self.batch_size = batch_size
        self.transform=transform
        self.ext_aug = ext_aug
        self.image_shape = image_shape
        self.label_shape = self.labels[0].shape
        self.eval=eval
        self.stats=stats
        self.self_supervised = self_supervised
        self.is_shuffle=True
        self.pre_load=preload

        self.indexes = np.arange(len(files))
        self.indexes =self._augment_data(self.indexes,drop_reminder)
        if self.pre_load:
            self.data_preloaded, self.mask_preloaded=self._pre_load_data(files)
        else:
            self.data_preloaded=np.arange(len(files))
            self.mask_preloaded=np.arange(len(files))


        #self.on_epoch_end()

    def on_epoch_end(self):
        '''THIS FUNCTION UPDATES THE INDEXES AFTER EACH EPOCH.'''
        if self.is_shuffle == True:
            np.random.shuffle(self.indexes)

    def _pre_load_data(self,all_files):
        datalist = []
        masklist = []

        for file_name in all_files:
            with np.load(file_name) as npz:
                image = npz['data']
                mask = (1 - npz['mask'].astype(int))

                datalist.append(image)
                masklist.append(mask)

        return datalist,masklist


    def _augment_data(self, data_frame, drop_reminder=True):
        im_list = []

        for i in range(self.augment_time):
            im_list.extend(data_frame)
        if drop_reminder:
            offset = int(np.ceil(len(im_list) / self.batch_size)) * self.batch_size - len(im_list)
            im_list.extend(data_frame[:offset])

        return im_list

    def __len__(self):
        '''THIS FUNCTION DENOTES THE NUMBER OF BATCHES PER EPOCH.'''
        return int(np.floor(len(self.indexes)/self.batch_size))

    def generator(self):
        while True:
            start=0
            end=self.batch_size
            if not self.self_supervised:  # IF STANDARD SUPERVISED LEARNING, RETURNS ONLY IMAGE AND MASK PAIRS

                X = np.empty((self.batch_size, 1, *self.image_shape, 150))
                Y = np.empty((self.batch_size, *self.label_shape))
                lab = [None] * self.batch_size
                while start < self.__len__():
                    indexes = self.indexes[start:end]
                    for i, ID in enumerate(indexes):
                        label = self.labels[ID]
                        if self.ext_aug:
                            if random.choice([True, False]):
                                label = label + np.random.uniform(-0.01, 0.01)
                        X[i, 0,], Y[i,], lab[i] = self._deparse_single_image(self.data_preloaded[ID],
                                                                             self.mask_preloaded[ID],
                                                                             self.files[ID]), label, self.files[ID]
                    if self.eval:
                        yield X, Y, lab
                    else:
                        yield X, Y

                    start += self.batch_size
                    end += self.batch_size
            else:
                X = np.empty((self.batch_size, 1, *self.image_shape, 150))
                Y = np.empty((self.batch_size, 1, *self.image_shape, 150))
                z = np.empty((self.batch_size, 1))
                while start < self.__len__():
                    indexes = self.indexes[start:end]
                    for i, ID in enumerate(indexes[:len(indexes) // 2]):
                        X[i, 0,] = self._deparse_single_image(self.data_preloaded[ID], self.mask_preloaded[ID],self.files[ID])
                        Y[i, 0,] = self._deparse_single_image(self.data_preloaded[ID], self.mask_preloaded[ID],self.files[ID])
                        z[i,] = 0  # HALF OF THE BATCH IS PREPARED WITH THE DIFFERENT AUGMENTATION VIEWS OF THE SAME IMAGE
                    for i, ID in enumerate(indexes[len(indexes) // 2:]):
                        X[i + len(indexes) // 2, 0,] = self._deparse_single_image(self.data_preloaded[ID],self.mask_preloaded[ID],self.files[ID])
                        Y[len(indexes) - i - 1, 0,] = self._deparse_single_image(self.data_preloaded[ID],self.mask_preloaded[ID],self.files[ID])
                        z[i + len(indexes) // 2,] = 1  # HALF OF THE BATCH IS PREPARED WITH THE DIFFERENT AUGMENTATION VIEWS OF THE DIFFERENT IMAGES
                    yield (X, Y), z
                    start += self.batch_size
                    end += self.batch_size




    def __getitem__(self, index):
        '''THIS FUNCTION GENERATES ONE BATCH OF DATA FOR SINGLE GPU LEARNING'''

        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        if not self.self_supervised: # IF STANDARD SUPERVISED LEARNING, RETURNS ONLY IMAGE AND MASK PAIRS
            X = np.empty((self.batch_size,1, *self.image_shape,150))
            Y = np.empty((self.batch_size, *self.label_shape))
            lab = [None] * self.batch_size
            for i, ID in enumerate(indexes):
                label = self.labels[ID]
                if self.ext_aug:
                    if random.choice([True, False]):
                        label=label+np.random.uniform(-0.01,0.01)
                X[i,0,], Y[i,], lab[i] = self._deparse_single_image(self.data_preloaded[ID],self.mask_preloaded[ID],self.files[ID]),label,self.files[ID]
            if self.eval:
                return X,Y,lab
            else:
                return X, Y
        else: # IF SELF SUPERVISED LEARNING
            X = np.empty((self.batch_size,1, *self.image_shape,150))
            Y = np.empty((self.batch_size,1, *self.image_shape,150))
            z = np.empty((self.batch_size, 1))
            for i, ID in enumerate(indexes[:len(indexes)//2]):
                X[i,0,]= self._deparse_single_image(self.data_preloaded[ID],self.mask_preloaded[ID],self.files[ID])
                Y[i,0,] = self._deparse_single_image(self.data_preloaded[ID],self.mask_preloaded[ID],self.files[ID])
                z[i,]=0 # HALF OF THE BATCH IS PREPARED WITH THE DIFFERENT AUGMENTATION VIEWS OF THE SAME IMAGE
            for i, ID in enumerate(indexes[len(indexes) // 2:]):
                X[i+len(indexes) // 2,0,] = self._deparse_single_image(self.data_preloaded[ID],self.mask_preloaded[ID],self.files[ID])
                Y[len(indexes)-i-1,0,] = self._deparse_single_image(self.data_preloaded[ID],self.mask_preloaded[ID],self.files[ID])
                z[i+len(indexes) // 2,] = 1 # HALF OF THE BATCH IS PREPARED WITH THE DIFFERENT AUGMENTATION VIEWS OF THE DIFFERENT IMAGES
            return [X, Y], z

    def _shape_pad(self,data, shape):
        padded = np.pad(data,
                        ((0, 0),
                         (0, (shape[0] - data.shape[1])),
                         (0, (shape[1] - data.shape[2]))),
                        'wrap')
        # print(padded.shape)
        return padded

    def _deparse_single_image(self,data, mask,file):

        if not self.pre_load:
            with np.load(file) as npz:
                data = npz['data']
                mask = (1 - npz['mask'].astype(int))
        if self.ext_aug and self.self_supervised:
            if random.choice([True, False]):
                data = (data * mask)
        else:
            data = (data * mask)

        sh=data.shape[1:]
        max_edge = np.max(sh)
        min_edge = np.min(sh) #AUGMENT BY SHAPE
        flag=True
        if False: #ext_aug:
            if min_edge>32:
                x = np.random.randint(sh[0]+1 - min_edge)
                y = np.random.randint(sh[1]+1 - min_edge)
                data=data[:,x:(x+min_edge),y:(y+min_edge)]
                flag=False

        if flag:
            if max_edge<self.image_shape[0]:
                max_edge=self.image_shape
            else:
                max_edge=(max_edge,max_edge)
            data = self._shape_pad(data, max_edge)
            data = data.transpose((1, 2, 0))

        data = data / np.max(self.stats[-1])  # MAX
        augmented = self.transform(image=data)
        data = augmented['image']

        return data

