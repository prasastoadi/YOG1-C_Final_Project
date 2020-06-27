from ctbangkit.base.base_model import BaseModel

from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

from absl import flags
from absl import logging

FLAGS = flags.FLAGS

from efficientnet.tfkeras import EfficientNetB0

class EnetBaseModel(BaseModel):
    def __init__(self):
        super(EnetBaseModel, self).__init__()
        self.build_model()

    def build_model(self):
        self.base_model=EfficientNetB0(weights='noisy-student', include_top=False)
        self.base_model.trainable= True

        self.x=self.base_model.output
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