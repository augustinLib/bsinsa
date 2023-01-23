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
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from kor2vec import Kor2Vec # Kor2Vec import

embed_size_tune = 64
batch_size_tune = 64
seq_length = 20
drop_out_per = 0.5
learning_rate=0.001
epoch_time=5
model_dir = "/home/augustin/project/bitamin-conference/recsys/model/modelfile/"
kor_vec_name= "embedding_final_1"
kor2Vec_location=model_dir+kor_vec_name

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')



class Decoder(nn.Module):
    def __init__(self, output_dim, emb_dim, hid_dim, dropout):
        super().__init__()
        self.hid_dim = hid_dim
        self.output_dim = output_dim
        self.embedding = nn.Embedding(output_dim, emb_dim)
        self.rnn = nn.GRU(emb_dim + hid_dim, hid_dim)
        self.fc_out = nn.Linear(emb_dim + hid_dim * 2, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input, hidden, context):
        embedded = self.dropout(input)
        emb_con = torch.cat((embedded, context), dim = 2)
        output, hidden = self.rnn(emb_con, hidden)
        output = torch.cat((embedded.squeeze(0), hidden.squeeze(0), context.squeeze(0)), 
                           dim = 1)
        prediction = self.fc_out(output)
        return prediction.unsqueeze(0), hidden

class Net(nn.Module):
    def __init__(self, seq_len = seq_length, embedding_size = embed_size_tune, hidden_size = embed_size_tune):
        super(Net, self).__init__()
        self.seq_len = seq_len
        self.embedding_size = embedding_size
        self.hidden_size = hidden_size
        self.resnet = models.resnet18(pretrained=True)
        self.decoder = Decoder(embed_size_tune, self.embedding_size, self.hidden_size, drop_out_per)
        self.kor2vec = Kor2Vec.load(kor2Vec_location)

        # resNet의 모든 파라미터를 잠그고 마지막 레이어만 얼리지 않고 사용합니다.
        for param in self.resnet.parameters():
             param.requires_grad = False
        self.resnet.fc = nn.Linear(512, embed_size_tune) # 마지막 레이어만 다시 사용합니다.

        # kor2vec의 모든 파라미터를 얼립니다.
        for param in self.kor2vec.parameters():
             param.requires_grad = False
    def forward(self, x):
        batch_size = x.shape[0]
        x = self.resnet(x).reshape(1,batch_size,self.hidden_size) # resnet 통과 output: (batch, hidden) torch.Size([64, 1, 3, 224, 224])
        hidden = x # lstm의 초기 셀 값은 resNet의 출력입니다.
        outputs = torch.zeros(self.seq_len, batch_size, self.embedding_size).to(device) # sequence를 저장하기 위한 빈 배열

        # <sos> 를 시작 토큰으로 설정합니다.
        output = self.kor2vec.embedding('<sos>').unsqueeze(0).repeat(1, batch_size, 1).to(device)

        # seq 결과물을 lstm의 입력으로 사용하여 seq_len 만큼 반복하여 저장합니다.
        for t in range(0, self.seq_len):
            output, hidden = self.decoder(output, hidden, x ) 
            outputs[t] = output
        
        return outputs.reshape(batch_size, self.seq_len, self.embedding_size) # shape: (15, batch_size, 1000)


    def give_embedding(self, x):
        batch_size = x.shape[0]
        x = self.resnet(x).reshape(1,batch_size,self.hidden_size) # resnet 통과 output: (batch, hidden)[1,64,hidden]

        hidden = x # lstm의 초기 셀 값은 resNet의 출력입니다.
        outputs = torch.zeros(self.seq_len, batch_size, self.embedding_size).to(device) # sequence를 저장하기 위한 빈 배열

        # <sos> 를 시작 토큰으로 설정합니다.
        output = self.kor2vec.embedding('<sos>').unsqueeze(0).repeat(1, batch_size, 1).to(device)

        # seq 결과물을 lstm의 입력으로 사용하여 seq_len = 15 만큼 반복하여 저장합니다.
        output, hidden = self.decoder(output, hidden, x )  
        return hidden
  
    def give_resnet_embedding(self, x): 
        batch_size = x.shape[0]
        x = self.resnet(x).reshape(1,batch_size,self.hidden_size) # resnet 통과 output: (batch, hidden)

        hidden =x # lstm의 초기 셀 값은 resNet의 출력입니다.
        return hidden

  # model.train() 을 위해 메소드 오버라이딩
    def train(self, mode=True):  
        self.training = mode
        for module in self.children():
            if module != self.kor2vec:
                module.train(mode)
        return self

  # model.eval() 을 위한 설정
    def eval(self, mode=False): 
        for module in self.children():
            if module != self.kor2vec:
                module.train(mode)
        return self
