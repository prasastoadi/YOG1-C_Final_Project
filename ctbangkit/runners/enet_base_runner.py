from ctbangkit.data_loader.enet_base_data_loader import EnetBaseDataLoader
from ctbangkit.models.enet_base_model import EnetBaseModel
from ctbangkit.trainers.enet_base_trainer import EnetBaseTrainer
from ctbangkit.utils.dirs import create_dirs

import tensorflow as tf
import numpy as np
import tempfile
import time
import os

from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS

flags.DEFINE_string('name', None, 'Experiment name')
flags.DEFINE_integer('batch_size', None, 'Batch size')
flags.DEFINE_integer('epochs', None, 'Number of epochs')
flags.DEFINE_integer('img_height', 224, 'Height of image for model')
flags.DEFINE_integer('img_width', 224, 'Width of image for model')
flags.DEFINE_string('train_dir', None, 'Train dataset directory')
flags.DEFINE_string('test_dir', None, 'Test dataset directory')
flags.DEFINE_string('logging_dir', None, 'Log directory')
flags.DEFINE_boolean('verbose', False, 'Training verbose')
flags.DEFINE_integer('seed', None, 'Random seed')

def main(args):
    # capture the config path from the run arguments
    # then process the json configuration file

    cv_history = []
    
    logging.info('Create the data generator...')
    data_loader = EnetBaseDataLoader()

    logging.info('Create the model...')
    model = EnetBaseModel()

    logging.info('Create the trainer...')
    trainer = EnetBaseTrainer(
            model.model, 
            (data_loader.get_train_data(),
                data_loader.get_test_data())
        )

    logging.info('Start training the model...')
    trainer.train()
    trainer_history = [trainer.loss, trainer.accuracy]
    cv_history.append(trainer_history)


    cv_history_dir = os.path.join(FLAGS.logging_dir,
        time.strftime("%Y-%m-%d/",time.localtime()),
        FLAGS.name,
        "history/")

    keras_model_dir = os.path.join(FLAGS.logging_dir,
        time.strftime("%Y-%m-%d/",time.localtime()),
        FLAGS.name,
        "keras_model/")    
    create_dirs([cv_history_dir, keras_model_dir])

    cv_history_np = np.array(cv_history)
    cv_history_filename = os.path.join(cv_history_dir, 'cv_history.np')
    np.save(cv_history_filename, cv_history_np)

    keras_file = os.path.join(keras_model_dir, 
                            '{}.h5'.format(FLAGS.name))
    trainer.model.save(keras_file, 
                        include_optimizer=True,
                        save_format='h5')
    logging.info('Saved final model to: {}'.format(keras_file))


if __name__ == '__main__':
  app.run(main)