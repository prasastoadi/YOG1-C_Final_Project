import os

from ctbangkit.base.base_train import BaseTrain
from ctbangkit.utils.dirs import create_dirs
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard

from absl import flags
from absl import logging

class EnetBaseTrainerCV(BaseTrain):
    def __init__(self, model, data, cv_iter):
        super(EnetBaseTrainerCV, self).__init__(model, data)
        self.callbacks = []
        self.loss = []
        self.accuracy = []
        self.val_loss = []
        self.val_accuracy = []
        self.init_callbacks()

        self.tensorboard_dir = os.path.join(FLAGS.log_dir,
            time.strftime("%Y-%m-%d/", time.localtime()),
            FLAGS.name,
            "logs_{}/".format(cv_iter))
        self.checkpoint_dir = os.path.join(FLAGS.log_dir,
            time.strftime("%Y-%m-%d/",time.localtime()),
            FLAGS.name,
            "checkpoints_{}/".format(cv_iter))
        
        create_dir([self.tensorboard_dir, self.checkpoint_dir])
        
        self.init_callbacks()
    def init_callbacks(self):
        #self.callbacks.append(
        #    ModelCheckpoint(
        #        filepath=os.path.join(self.config.callbacks.checkpoint_dir, '%s-{epoch:02d}-{val_loss:.2f}.hdf5' % self.config.exp.name),
        #        monitor=self.config.callbacks.checkpoint_monitor,
        #        mode=self.config.callbacks.checkpoint_mode,
        #        save_best_only=self.config.callbacks.checkpoint_save_best_only,
        #        save_weights_only=self.config.callbacks.checkpoint_save_weights_only,
        #        verbose=self.config.callbacks.checkpoint_verbose,
        #    )
        #)

        self.callbacks.append(
            TensorBoard(
                log_dir=self.tensorboard_dir,
            )
        )

    def train(self):
        train_generator, val_generator = self.data

        step_size_train=(train_generator.n//train_generator.batch_size)
        step_size_val=(val_generator.n//val_generator.batch_size)

        step_size_train += 1
        step_size_val += 1

        # Do not specify the batch_size if your data is in the form of datasets, generators, or 
        # keras.utils.Sequence instances (since they generate batches).
        history = self.model.fit(
            train_generator,
            epochs=FLAGS.epochs,
            steps_per_epoch=step_size_train,
            #batch_size=self.config.trainer.batch_size,
            verbose=FLAGS.verbose,
            validation_data=val_generator,
            validation_steps=step_size_val,
            callbacks=self.callbacks,
            )
        self.loss.extend(history.history['loss'])
        self.accuracy.extend(history.history['accuracy'])
        self.val_loss.extend(history.history['val_loss'])
        self.val_accuracy.extend(history.history['val_accuracy'])