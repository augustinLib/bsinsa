# 라이브러리 import
import pandas as pd
import os
from kor2vec import Kor2Vec # Kor2Vec import
import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from torchvision import transforms
import torchvision.datasets as datasets
from PIL import Image
import torchvision.models as models # 임베딩 모델
import torchvision
import torch.optim as optim
import matplotlib.pyplot as plt
import ast

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(device)

#경로 설정
total_df = pd.read_csv("/home/augustin/project/bitamin-conference/recsys/dataframe/to_Dataloader.csv", encoding="UTF-8")
img_dir= '/home/augustin/project/bitamin-conference/data/crawling/data/image/'
model_dir = "/home/augustin/project/bitamin-conference/recsys/model/modelfile/"
kor_vec_name= "embedding_final_1"

# kor2vec_hyperparameter 조정
embed_size_tune = 64
batch_size_tune = 64
seq_length = 20


#transform
transform = transforms.Compose(
    [transforms.ToTensor(), # 텐서로 변형
     transforms.Resize(224), # 사이즈 조절
     transforms.CenterCrop(224), # 가로와 세로 중 안 맞는 곳 자르기
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


class preprocess(Dataset):
    def to_list(x):
        return ast.literal_eval(x)
    
    def max_len(x):
        return len(x)

    def split_(x):
        return x.replace(',',' ')
    
    total_df['tag'] = total_df['tag'].apply(split_)

    
    if kor_vec_name not in os.listdir(model_dir):

    # 태그 데이터를 사용해 임베딩을 학습 실시

        rev = pd.Series("<sos> " + total_df['tag']+" <end>")
        rev.to_csv(model_dir+"summary_text_corpus.csv")

        # skip-gram 기반 임베딩 training
        kor2vec = Kor2Vec(embed_size=embed_size_tune) # embed_size : 임베딩 벡터의 2번째 차원(차원 수)
        kor2vec.train(model_dir+"summary_text_corpus.csv", 'model.kor2vec', batch_size=batch_size_tune) # 임베딩 실시 (학습)
        kor2vec.save(model_dir+ kor_vec_name)  # 임베딩 모델 저장

class CaptionDataset(Dataset):
    def __init__(self, img_dir, caption_df, transform=None):
        self.root_dir = img_dir
        self.transform = transform
        self.df = caption_df
        
        self.imgs = self.df['image_filename'] # 이미지 파일 경로
        self.captions = self.df["tag"] # 태그 데이터
        self.kor2vec = Kor2Vec.load(model_dir+ kor_vec_name) # Kor2Vec 로드
        
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self,idx):
        caption = self.captions[idx] # target caption
        img_name = self.imgs[idx] # 이미지 이름 파일 불러오기
        img_location = os.path.join(img_name) # 실제로 이미지 오픈
        img = Image.open(img_location).convert("RGB")
        
        if self.transform is not None:
            img = self.transform(img)
            caption = self.kor2vec.embedding(caption, seq_len=seq_length)

        return img, caption




reveiw_train_data = CaptionDataset(img_dir, total_df, transform=transform)

img, rev = reveiw_train_data[0]

print(f"img shape : {img.shape}") # ([1, 3, 224, 224]) - [배치, 채널, 가로, 세로]
print(f"rev : {rev.shape}") # ([20, 64])) - [seq_len, hidden_size]
review_train_dataloader = DataLoader(reveiw_train_data, batch_size=batch_size_tune, shuffle=True)