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
# from Modeling import *
# from Training import *
# from Mobilenet_categories import *
# from Preprocess_categories import *

import argparse
from sklearn.metrics.pairwise import euclidean_distances

embedding_dir = "review_embeddings_test.pickle" #이미지 + 태그
location = '/home/augustin/project/bitamin-conference/recsys/'
concat_pickle= '/final_embeddings.pickle'
df = pd.read_csv(location+'dataframe/to_Dataloader.csv')


transform = transforms.Compose(
  [transforms.ToTensor(), # 텐서로 변형
    transforms.Resize(224), # 사이즈 조절
    transforms.CenterCrop(224), # 가로와 세로 중 안 맞는 곳 자르기
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


if concat_pickle not in os.listdir(location + 'model/modelfile'): #임베딩 파일 없을 경우 생성 후 저장
    with open(location + '/model/modelfile/embeddings_shuffle_epoch10.pickle', 'rb') as f:
        label_embed_list=pickle.load(f) #키테고리 임베딩
                
    with open(location + '/model/modelfile/' + embedding_dir, 'rb') as z:
        embed_list = pickle.load(z) #이미지 + 태그 임베딩


    label_numpy=np.squeeze(np.array(label_embed_list))
    review_numpy=np.squeeze(np.array(embed_list))
    final_embedding=np.concatenate((label_numpy,review_numpy), axis=1)

    with open(location + '/model/modelfile/'+concat_pickle, 'wb') as f:
        pickle.dump(final_embedding, f, pickle.HIGHEST_PROTOCOL)

# def classification():
#     model = SuperLightMobileNet(5).to(device)
#     model.load_state_dict(torch.load(location +'total_model_light6_0.001_10.pth', map_location=device))
#     model.eval()  
#     return model

# def caption():
#     model = Net()
#     model.to(device)
#     model.load_state_dict(torch.load(location+'model/modelfile/show_and_tell_final.pt', map_location=device))
#     return model

def image_plus(df,img_dir,img_name):
    if df["image_filename"].isin([img_name]).any():
        target_idx=df[df["image_filename"]==img_name].index.to_list()[0]
        with open(location + 'model/modelfile/final_embeddings.pickle', 'rb') as f:
            final_embeddings = pickle.load(f)

        dist_mtx = euclidean_distances(final_embeddings,final_embeddings)
        plt.imshow(Image.open(img_name))
        # plt.show()

        close_list = dist_mtx[target_idx].argsort()[1:6]
        # print(close_list)
        print("가장 가까운 이미지")
        print("======================")
            # target을 포함해 target과 가장 가까운 것 10개
        for i, idx in enumerate(close_list):
            img, rev = reveiw_train_data[idx]
            img = img
            plt.imshow(img)
            # plt.show()
            plt.savefig(f'savefig_default{i}.jpg')
            
            


            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='사진경로를 입력해주세요')
    parser.add_argument('--location', default ='/home/augustin/project/bitamin-conference/data/crawling/data/image/', type=str, help='사진 경로')
    parser.add_argument('--img_name',type=str, help='사진파일명')
    args = parser.parse_args()


    reveiw_train_data = CaptionDataset(img_dir, df, transform=None)
    # mobile_net_model = classification()
    # show_and_tell_model = caption()

    image_plus(df,args.location, args.img_name)

