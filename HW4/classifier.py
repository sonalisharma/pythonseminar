from os import listdir
import os 
from multiprocessing import Pool, cpu_count
from pylab import imread
from time import time
import scipy as sp
import numpy as np
from skimage.filter import sobel
import pickle
from collections import defaultdict
from sklearn import preprocessing

def extract_features(image_path_list):
    feature_list = []
    for image_path in image_path_list:
        image_array = imread(image_path)
        img_size = image_array.size
        red_channel_mean= image_array[...,0].mean()
        green_channel_mean= image_array[...,1].mean()
        blue_channel_mean= image_array[...,2].mean()
        red_channel_sd= image_array[...,0].std()
        green_channel_sd= image_array[...,1].std()
        blue_channel_sd= image_array[...,2].std()

        #Calculating grayscale value
        imgarray1_gray = sp.inner(image_array, [299, 587, 114])
        #Location x and y treated as different features
        max_gray_x_loc = np.argwhere(imgarray1_gray.max() == imgarray1_gray)[...,0].mean()
        max_gray_y_loc = np.argwhere(imgarray1_gray.max() == imgarray1_gray)[...,1].mean()
        min_gray_x_loc = np.argwhere(imgarray1_gray.min() == imgarray1_gray)[...,0].mean()
        min_gray_y_loc = np.argwhere(imgarray1_gray.min() == imgarray1_gray)[...,1].mean()
        min_gray_x_loc_std = np.argwhere(imgarray1_gray.min() == imgarray1_gray)[...,0].std()
        min_gray_y_loc_std = np.argwhere(imgarray1_gray.min() == imgarray1_gray)[...,1].std()
        max_gray_x_loc_std = np.argwhere(imgarray1_gray.max() == imgarray1_gray)[...,0].std()
        max_gray_y_loc_std = np.argwhere(imgarray1_gray.max() == imgarray1_gray)[...,1].std()
        
        imgarray1_gray = np.array(imgarray1_gray, dtype=np.float64)
        edges = sobel(imgarray1_gray)
        edges_height = edges.shape[0]
        edges_width = edges.shape[1]
        
        
        feature_list.append([image_path.split("/")[-2],image_path.split("/")[-1], 
                             img_size,
                             red_channel_mean,
                             green_channel_mean,
                             blue_channel_mean,
                             red_channel_sd,
                             green_channel_sd,
                             blue_channel_sd,
                             max_gray_x_loc,
                             max_gray_y_loc,
                             min_gray_x_loc,
                             min_gray_y_loc,
                             max_gray_x_loc_std,
                             max_gray_y_loc_std,
                             min_gray_x_loc_std,
                             min_gray_y_loc_std,
                             edges_height,
                             edges_width                              
                             ])
    return feature_list

def run_final_classifier(path,classifier):
    filepaths = []
    results = defaultdict(list)
    pkl_file = open(classifier, 'rb')
    clf2 = pickle.load(pkl_file)
    for files in listdir(path):
        filepaths.append(path+"/"+files)
    feature =  extract_features(filepaths)
    X = [c[2:] for c in feature]
    X_scaled = preprocessing.scale(X)
    preds = clf2.predict(X_scaled)
    for i in range(len(preds)):
        results[X_scaled[i][1]]=preds[i]
        print feature[i][1]+"----->"+preds[i]