import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from torchvision import transforms
import torchvision.datasets as datasets
import pickle
from PIL import Image
import os
import pandas as pd
from Mobilenet_categories import *
from Preprocess_categories import *

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

num_classes = 5
batch_size = 20
num_workers = 2
lr = 1e-3
total_epoch = 2
big_cls = 'total'

location = '/home/augustin/project/bitamin-conference/recsys/model/modelfile/'
img_dir = '/home/augustin/project/bitamin-conference/data/crawling/data/image'
dir_weight = '/home/augustin/project/bitamin-conference/recsys/model/modelfile/total_model_light6_0.001_10.pth'
df = pd.read_csv('/home/augustin/project/bitamin-conference/recsys/dataframe/to_Dataloader.csv')

embeddings = []

transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor()])

train_data = ImageDataset(img_dir, df, transform=transform)
train_data2 = ImageDataset(img_dir, df, transform=None)

train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=False)
train_loader1 = DataLoader(train_data, batch_size=1, shuffle=False)


# 학습된 cateogires 모델에서 categories와 image가 들어가 있는 embedding을 추출.

if __name__ == "__main__":
  model = SuperLightMobileNet(num_classes).to(device)
  model.load_state_dict(torch.load(dir_weight))
  model.eval()

  for itereation, (input, target) in enumerate(train_loader1):
    images = input.to(device)
    outputs = model.give_embedding(images).cpu().detach().numpy()
    embeddings.append(outputs)
    if itereation %100 ==0 :
      print('{}th img embedding'.format(itereation))

  with open(location+'embeddings_shuffle_epoch10.pickle', 'wb') as f:
    pickle.dump(embeddings, f, pickle.HIGHEST_PROTOCOL)