from ctbangkit.data_loader.enet_base_data_loader import EnetBaseDataLoaderCV
from ctbangkit.models.enet_base_model import EnetBaseModelCV
from ctbangkit.trainers.enet_base_trainer import EnetBaseTrainerCV
from ctbangkit.utils.dirs import create_dirs

import tensorflow as tf
import numpy as np

from absl import flags
from absl import logging

def main(args):
    # capture the config path from the run arguments
    # then process the json configuration file

    df_train = extract_dir_to_df(FLAGS.train_dir)
    folds = KFold(n_splits=5, shuffle=True, random_state=3)\
        .split(df_train['filepath'], df_train['class'])

    cv_history = []
    for cv_iter, (train_idx, val_idx) in enumerate(folds):
        logging.info("Starting cross-validation iteration {}"\
            .format(cv_iter))

        logging.info('Create the data generator...')
        data_loader = EnetBaseDataLoaderCV(train_idx, val_idx)

        logging.info('Create the model...')
        model = EnetBaseModelCV()

        logging.info('Create the trainer...')
        trainer = EnetBaseTrainerCV(
                model.model, 
                (data_loader.get_train_data(),
                    data_loader.get_val_data()),
                cv_iter
            )

        logging.info('Start training the model...')
        trainer.train()
        trainer_history = [trainer.loss, trainer.accuracy, trainer.val_loss, trainer.val_accuracy]
        cv_history.append(trainer_history)


    cv_history_dir = os.path.join(FLAGS.log_dir,
        time.strftime("%Y-%m-%d/",time.localtime()),
        FLAGS.name,
        "history/")
    
    create_dir([cv_history_dir])
    cv_history_np = np.array(cv_history)
    cv_history_filename = os.path.join(cv_history_dir, 'cv_history.np')
    np.save(cv_history_filename, cv_history_np)

    cv_history_mean = np.mean(np.array(cv_history), axis=0)
    cv_history_filename = os.path.join(cv_history_dir, 
                                    'cv_history_mean.np')
    np.save(cv_history_filename, cv_history_mean)
    
if __name__ == '__main__':
  app.run(main)