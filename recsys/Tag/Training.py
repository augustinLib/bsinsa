import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from torchvision import transforms
import torchvision.datasets as datasets
from PIL import Image
import torchvision.models as models # 임베딩 모델
import torchvision
import torch.optim as optim
import pickle
import pandas as pd
import numpy as np
import os
from kor2vec import Kor2Vec # Kor2Vec import
from Preprocess import *
from Modeling import *


model_name="show_and_tell_final.pt"
py_dir = "modelfile/"
model_dir = "/home/augustin/project/bitamin-conference/recsys/model/"
kor_vec_name= "embedding_final_1"
kor2Vec_location=model_dir+py_dir+kor_vec_name
os.chdir(model_dir+py_dir)



show_and_tell_model = Net()
criterion = nn.SmoothL1Loss()
optimizer = optim.Adam(show_and_tell_model.parameters(), lr=learning_rate)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
show_and_tell_model.to(device)


if model_name not in os.listdir(model_dir+py_dir):

  # 신경망 학습
  for epoch in range(10): # 10에포크
    running_loss = 0.0

    for i, data in enumerate(review_train_dataloader):
      img, label = data[0].squeeze(1).to(device), data[1].to(device)
      optimizer.zero_grad()
      output = show_and_tell_model(img)

      loss = criterion(output.squeeze(1), label.to(device))
      loss.backward()
      optimizer.step()

      running_loss += loss.item()
      
      if i>= len(reveiw_train_data) - 1: break # 왜인지 모르겠으나 묵시적으로 enumerate가 종료되지 않아서 명시적으로 추가
      
      if (i % 10) == 0: # 매 1000번 미니배치마다 출력하기
              print('[%d, %5d] loss: %.3f' %
                    (epoch +1, i+1, running_loss / (i + 1)))
              running_loss =0.0



  torch.save(show_and_tell_model.state_dict(), model_dir+py_dir+model_name)



