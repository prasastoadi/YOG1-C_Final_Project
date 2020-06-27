# Bangkit YOG-1 C Final Project

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
5-Fold Cross-Validation  
Best Epoch at 464th  

Average Loss : 0.007767  
Average Accuracy 0.996875  
Average Val_loss 0.404840  
Average Val_accuracy 0.940625  

Full training  
Testing Loss : 0.4822  
Testing Accuracy: 0.9107  
 


### 5. Documentation
#### How to reproduce our project?

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


#### DATA PROCESSING
Normalization
Make the pixel range between 0 and 1.

### 6. Propose/Ideate
To help government 
