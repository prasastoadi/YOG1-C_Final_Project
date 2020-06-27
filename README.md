# Bangkit YOG-1 C Final Project

### How to reproduce our project?

1. Clone the dataset from this repo https://github.com/UCSD-AI4H/COVID-CT

2. Extract the dataset to a folder. For example:  
`unzip "COVID-CT/Images-processed/CT_NonCOVID.zip" -d "raw_dataset/"`  
`unzip "COVID-CT/Images-processed/CT_COVID.zip" -d "raw_dataset/"`

3. Clone our repository  
`git clone https://github.com/phitonthel/YOG1-C_Final_Project`

4. Rename our project directory to 'ctbangkit'  
`mv YOG1-C_Final_Project ctbangkit`

5. Install our repo as an editable package  
`pip install -e ctbangkit`

6. Build the dataset into train and test split  
```
python ctbangkit/build_dataset.py \  
--raw_data_dir="raw_dataset" \  
--data_dir="dataset" \  
--test_size=0.15 \  
--kfold=5 \  
--seed=3
```
Configure the arguments to fit your needs.

7. Configure the **data loader**, **model**, **trainer**, and **runner**  

8. Execute **runner** file with the arguments. For example:  
```
python ctbangkit/ctbangkit/runners/enet_base_runner.py \
--name='enet_base' \
--batch_size=32 \
--epochs=500 \
--img_height=224 \
--img_width=224 \
--train_dir=dataset/train \
--test_dir=dataset/test \
--verbose=True \
--logging_dir=experiments \
--seed=3
```

## Classifying COVID-19 and Non-COVID-19 Lungs From CT Scan Using CNN

### 0. Dataset
What Dataset Did We Choose?  

We choose [COVID-19 Lung CT Scans](https://www.kaggle.com/luisblanche/covidct) dataset for our final project. This dataset is a collection of COVID-19 related papers from medRxiv, NEJM, JAMA, Lancet, etc. Total images in this collection is 746 CT scan images. It consists of 349 COVID positive images and 397 COVID negative images.

### 1. Reason
Why Did We Choose the Dataset?  

1. We choose COVID-19 CT scans dataset due to the current situation, COVID-19 pandemic outbreak.  
2. [COVID-19 Lung CT Scans](https://www.kaggle.com/luisblanche/covidct) is easy to understand and has some public kernels. Public kernels are useful to gain insight and compare our work with the others.  

### 2. Result
Baseline CNN Implementation  

### 3. Reason
Why Did We Choose the Specific Improvement?  


### 4. Result
Improvement  


### 5. Documentation

#### ARCHIVE CONTENTS
CT_NonCOVID.zip: Contains non covid lungs ct scan images.
CT_COVID.zip: Contains covid lungs ct scan images.

#### HARDWARE: (The following specs were used to create the original solution)
We are using google colab’s facility with GPU Hardware accelerator.

#### SOFTWARE:
Python 3.6.9
EfficientNet 1.1.0
Tensorflow 2.2.0
Numpy 1.18.5
Pandas 1.0.4
Sklearn 0.22.2.post1
OpenCV 4.1.2
Matplotlib 3.2.1

#### DATA SETUP
!git clone https://github.com/UCSD-AI4H/COVID-CT.git
!unzip "COVID-CT/Images-processed/CT_NonCOVID.zip" -d "dataset/"
!unzip "COVID-CT/Images-processed/CT_COVID.zip" -d "dataset/"

#### DATA PROCESSING
Normalization
Make the pixel range between 0 and 1.
Reshape
224x224

#### MODEL BUILD:
Call Efficientnetb0BaseModel(config_json) class.

### 6. Propose/Ideate
Local (Indonesia) implementation of the project you've done  
