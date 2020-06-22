import os
os.environ['KAGGLE_CONFIG_DIR'] = "/content/"

# THESE CODES SHOW YOU HOW TO UPLOAD THE KAGGLE API IF YOU HAVEN'T
# Run this cell and select the kaggle.json file downloaded
# from the Kaggle account settings page.
from google.colab import files
files.upload()

# Let's make sure the kaggle.json file is present.
!ls -lha kaggle.json

# Let's make sure the kaggle.json file is present.
!ls -lha kaggle.json

# Next, install the Kaggle API client.
!pip install -q kaggle

# The Kaggle API client expects this file to be in ~/.kaggle,
# so move it there.
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/

# This permissions change avoids a warning on Kaggle tool startup.
!chmod 600 ~/.kaggle/kaggle.json

# List available datasets.
!kaggle datasets list


# NOW YOU GOTTA DOWNLOAD THE DATASER FROM KAGGLE
!kaggle datasets download -d luisblanche/covidct

import zipfile
base_dir = '/content'
data_dir = os.path.join(base_dir, 'data')
local_zip = os.path.join(base_dir, 'covidct.zip')
zip_ref = zipfile.ZipFile(local_zip, 'r')
os.mkdir(data_dir)
zip_ref.extractall(data_dir)
zip_ref.close()

train_dir = os.path.join(data_dir, 'train')
test_dir = os.path.join(data_dir, 'test')
os.mkdir(train_dir)
os.makedirs(os.path.join(test_dir, 'CT_COVID'))
os.mkdir(os.path.join(test_dir, 'CT_NonCOVID'))

splitter('CT_COVID')
splitter('CT_NonCOVID')

import tensorflow as tf
import keras_preprocessing
from keras_preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    )
     
test_datagen = ImageDataGenerator(
    rescale=1./255
    )

train_generator = train_datagen.flow_from_directory(
	train_dir,
	target_size=(150,150),
	class_mode='binary',
  batch_size= 61
)

test_generator = test_datagen.flow_from_directory(
	test_dir,
	target_size=(150,150),
	class_mode='binary',
  batch_size=25
)


# USING RESNET
base_model = tf.keras.applications.ResNet50(input_shape=(150, 150, 3),
                                               include_top=False,
                                               weights='imagenet')
					       
regularizer = tf.keras.regularizers.L1L2(
    l1=0.5, l2=0.5
)
for layer in base_model.layers:
  layer.trainable = False
  for attr in ['kernel_regularizer']:
    if hasattr(layer, attr):
      setattr(layer, attr, regularizer)
      
base_model.summary()

last_layer = base_model.get_layer('conv5_block3_out')
print('last layer output shape: ', last_layer.output_shape)
last_output = last_layer.output

from tensorflow.keras.optimizers import RMSprop

# Flatten the output layer to 1 dimension
x = tf.keras.layers.Flatten()(last_output)
# Add a fully connected layer with 1,024 hidden units and ReLU activation
x = tf.keras.layers.Dense(1024, activation='relu')(x)
# Add a dropout rate of 0.2
x = tf.keras.layers.Dropout(.2)(x)                  
# Add a final sigmoid layer for classification
x = tf.keras.layers.Dense(1, activation='sigmoid')(x)           

model = tf.keras.Model(base_model.input, x) 

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
    loss='binary_crossentropy', 
    metrics=['accuracy']
)

model.summary()



class AccCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if logs.get('accuracy') > .9:
      self.model.stop_training = True
      


history = model.fit(train_generator, epochs=40, steps_per_epoch=3, validation_data = test_generator, verbose = 1, validation_steps=3,
                    # callbacks=[AccCallback()]
                    )
                    
                    


import matplotlib.pyplot as plt
accuracy = history.history['accuracy']
val_accuracy = history.history['val_accuracy']
epochs = range(len(accuracy))
plt.plot(epochs, accuracy, 'r', label='Training Accuracy')
plt.plot(epochs, val_accuracy, 'b', label='Testing Accuracy')
plt.legend(loc=0)
plt.figure()
plt.show()





loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(accuracy))
plt.plot(epochs, loss, 'g', label='Loss Training')
plt.plot(epochs, val_loss, 'c', label='Loss Testing')
plt.legend(loc=0)
plt.figure()
plt.show()





# Save the entire model as a SavedModel.
!mkdir -p saved_model

saved_model_dir = 'saved_model/my_model'
model.save(saved_model_dir) 





converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
tflite_model = converter.convert()
open("converted_model.tflite", "wb").write(tflite_model)



model.export(export_dir='.')
