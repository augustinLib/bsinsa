
# 라이브러리 import
import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from torchvision import transforms
import torchvision.datasets as datasets
from PIL import Image
import os
import pandas as pd

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class ImageDataset(Dataset):
    """
    root_dir : 이미지 파일이 있는 경로
    transform : 이미지를 텐서로 변환할 때 transform (optional)
    """
    def __init__(self, img_dir, df, transform=None):
        self.root_dir = img_dir
        self.transform = transform
        self.df = df
        
        self.imgs = self.df['image_filename'] # 이미지 파일 경로
        self.categories = self.df["categories"] # 카테고리 데이터
    
    def __len__(self):
        return len(self.df)
    
    # 이미지, 텍스트를 불러 오는 메소드
    # transform을 선언하면 임베딩 벡터와 1개 배치로 반환하며, 선언하지 않으면 이미지와 스트링 형태의 캡션을 반환합니다.
    def __getitem__(self,idx):
        categories = self.categories[idx] # target caption
        img_name = self.imgs[idx] # 이미지 이름 파일 불러오기
        img_location = os.path.join(self.root_dir,img_name) # 실제로 이미지 오픈
        img = Image.open(img_location).convert("RGB")
        
        # transform이 있다면 실시 후 배치화(1 차원 추가)
        if self.transform is not None:
          img = self.transform(img)

        return img, categories
