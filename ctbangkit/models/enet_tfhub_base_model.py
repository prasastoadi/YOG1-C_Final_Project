from ctbangkit.base.base_model import BaseModel

from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

from absl import flags
from absl import logging

FLAGS = flags.FLAGS

import tensorflow_hub as hub

class EnetTFHubBaseModel(BaseModel):
    def __init__(self):
        super(EnetTFHubBaseModel, self).__init__()
        self.build_model()

    def build_model(self):
        url = "https://tfhub.dev/tensorflow/efficientnet/b0/classification/1"
        self.enet = hub.KerasLayer(url, input_shape=(FLAGS.img_height, FLAGS.img_width, 3), trainable=True)
        self.base_model=self.enet

        self.x=self.base_model
        self.x=GlobalAveragePooling2D()(self.x)
        self.x=Dense(512, activation='relu')(self.x)
        self.x=Dropout(rate=0.2)(self.x)
        self.x=Dense(128, activation='relu')(self.x)
        self.x=Dropout(rate=0.2)(self.x)
        self.preds=Dense(1,activation='sigmoid')(self.x)

        self.model=Model(inputs=self.base_model.input,outputs=self.preds)

        self.model.compile(optimizer='adam',
                            loss='binary_crossentropy',
                            metrics=['accuracy'])