import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from torchvision import transforms
import torchvision.datasets as datasets
import torchvision.models as models # 임베딩 모델
import torchvision
import torch.optim as optim
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from kor2vec import Kor2Vec # Kor2Vec import
from Preprocess import *
from Modeling import *
from Training import *

embedding_dir="review_embeddings_test.pickle" #이미지 임베딩


show_and_tell_model.load_state_dict(torch.load(model_dir+py_dir+model_name))
# 가장 유사한, 가장 유사하지 않은 것 비교 코드

if embedding_dir not in os.listdir(model_dir+py_dir):
    i_list = []
    #resnet_embed_list = []
    embed_list = []
    # 모든 이미지에 대한 임베딩 계산
    for i, data in enumerate(reveiw_train_data):
        show_and_tell_model.eval()
        img, label = data[0].to(device), data[1].to(device)
        img = img.unsqueeze(0)
        #resnet_embed = show_and_tell_model.give_resnet_embedding(img)[0].cpu().detach().numpy()[0][0]
        embed = show_and_tell_model.give_embedding(img).cpu().detach().numpy()

        i_list.append(i)
        embed_list.append(embed)
      #resnet_embed_list.append(resnet_embed)

        if i>= len(reveiw_train_data) - 1: break

        if i%100 == 0:
            print(f"image done : {i}")

    with open(model_dir+py_dir+embedding_dir, 'wb') as f:
        pickle.dump(embed_list, f, pickle.HIGHEST_PROTOCOL)

else:
    with open(model_dir+py_dir+embedding_dir, 'rb') as f:
        embed_list = pickle.load(f)
        
        