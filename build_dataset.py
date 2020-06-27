import os
import pandas as pd
from glob import glob
import shutil

from absl import app
from absl import flags
from absl import logging

from sklearn.model_selection import StratifiedShuffleSplit

FLAGS = flags.FLAGS

flags.DEFINE_string('raw_data_dir', None, '/path/to/raw_data_dir')
flags.DEFINE_string('data_dir', None, '/path/to/new_data_dir')
flags.DEFINE_float('test_size', 0.15, 'Test size')
flags.DEFINE_integer('kfold', 5, 'K size in Kfold Cross-Validation')
flags.DEFINE_integer('seed', 3, 'Random seed value')

CT_NonCOVID = 'CT_NonCOVID'
CT_COVID = 'CT_COVID'

def extract_dir_to_df(root_dir: str)-> pd.DataFrame:
    dirnames = os.listdir(root_dir)
    dirnames = [dire for dire in dirnames 
                if os.path.isdir(os.path.join(root_dir, dire))]
    data = {'filepath': [],
            'class': []}

    for dir_ in sorted(dirnames):
        clsname = dir_.split('.')[0]
        list_dir = os.listdir(os.path.join(root_dir, dir_))
        for fname in list_dir:
            fullpath = os.path.join(root_dir, dir_, fname)
            if not os.path.isfile(fullpath):
                continue
            data['filepath'].append(fullpath)
            data['class'].append(clsname)
    return pd.DataFrame(data)

def create_dir():
    # Create Train-Test Directory
    subdir  = 'train/'

    labeldirs = ['CT_COVID', 'CT_NonCOVID']
    for labldir in labeldirs:
        train_dir = os.path.join(FLAGS.data_dir, subdir, labldir)
        os.makedirs(train_dir, exist_ok=True)

    subdir  = 'test/'

    labeldirs = ['CT_COVID', 'CT_NonCOVID']
    for labldir in labeldirs:
        test_dir = os.path.join(FLAGS.data_dir, subdir, labldir)
        os.makedirs(test_dir, exist_ok=True)

    return train_dir, test_dir

def split_dataset(data, labels):
    sss = StratifiedShuffleSplit(
        n_splits=1, 
        test_size=FLAGS.test_size, 
        random_state=FLAGS.seed)

    splitted_list = list(sss.split(data, labels))
    train_index = splitted_list[0][0]
    test_index = splitted_list[0][1]

    logging.info("Full data : {} images".format(len(data)))
    logging.info("Train index : {} images".format(len(train_index)))
    logging.info("Test index : {} iamges".format(len(test_index)))

    logging.info("Copying images from {0} to {1}".format(
        FLAGS.raw_data_dir, FLAGS.data_dir
    ))

    # Copy Images to test set

    list_of_random_files = []
    test_dir = os.path.join(FLAGS.data_dir, 'test/')
    for i in test_index:
        list_of_random_files.append([data[i], labels[i]])

    for f,l in list_of_random_files:
        shutil.copy2(f, test_dir + l)

    # Copy Images to train set
    list_of_random_files = []
    train_dir = os.path.join(FLAGS.data_dir, 'train/')
    for i in train_index:
        list_of_random_files.append([data[i], labels[i]])
        
    for f,l in list_of_random_files:
        shutil.copy2(f, train_dir + l)


    total_train_covid = len(os.listdir(
        os.path.join(FLAGS.data_dir, 'train', CT_COVID)))
    total_train_noncovid = len(os.listdir(
        os.path.join(FLAGS.data_dir, 'train', CT_NonCOVID)))
    total_test_covid = len(os.listdir(
        os.path.join(FLAGS.data_dir, 'test', CT_COVID)))
    total_test_noncovid = len(os.listdir(
        os.path.join(FLAGS.data_dir, 'test', CT_NonCOVID)))

    logging.info("Train sets images COVID: {}"\
        .format(total_train_covid))
    logging.info("Train sets images Non COVID: {}"\
        .format(total_train_noncovid))
    logging.info("Test sets images COVID: {}"\
        .format(total_test_covid))
    logging.info("Test sets images Non COVID: {}"
        .format(total_test_noncovid))

    return train_index, test_index


def main(args):
    path_positive_cases = os.path.join(FLAGS.raw_data_dir, 'CT_COVID')
    path_negative_cases = os.path.join(FLAGS.raw_data_dir,'CT_NonCOVID')

    # List CT dataset
    positive_images_ls = glob(os.path.join(path_positive_cases,"*.png"))

    negative_images_ls = glob(os.path.join(path_negative_cases,"*.png"))
    negative_images_ls.extend(
        glob(os.path.join(path_negative_cases,"*.jpg")))

    total_positive_covid = len(positive_images_ls)
    total_negative_covid = len(negative_images_ls)

    logging.info("Total Positive Cases Covid19 images: {}"\
        .format(total_positive_covid))
    logging.info("Total Negative Cases Covid19 images: {}"\
        .format(total_negative_covid))

    covid = {'class': 'CT_COVID',
         'path': path_positive_cases,
         'images': positive_images_ls}

    non_covid = {'class': 'CT_NonCOVID',
             'path': path_negative_cases,
             'images': negative_images_ls}

    data_full=[]
    labels_full=[]
    data_full = covid["images"].copy()
    data_full.extend(non_covid["images"].copy())
    labels_full = [covid["class"]] * len(covid["images"])
    labels_full.extend([non_covid["class"]] * len(non_covid["images"]))

    _, _ = create_dir()
    train_index, test_index = split_dataset(data_full, labels_full)

    

if __name__ == '__main__':
  app.run(main)