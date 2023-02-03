# torch pretrained resnet

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models


class ResNet(nn.Module):
    def __init__(self, embedding=256):
        super(ResNet, self).__init__()
        self.embedding = embedding
        self.resnet = models.resnet50()
        self.resnet.fc = nn.Identity()

    def forward(self, x):
        return self.resnet(x)


class CompatibilityModel(nn.Module):
    def __init__(self, embedding=2048, hidden_dim=512):
        super(CompatibilityModel, self).__init__()
        self.resnet = ResNet(embedding)  # output=2048
        self.lstm = nn.LSTM(embedding, hidden_dim, batch_first=True, bidirectional=True, dropout=0.7)
        self.fc = nn.Linear(hidden_dim * 2 * 2, 1)

    def forward(self, top, bottom):
        top_out = self.resnet(top)
        bottom_out = self.resnet(bottom)
        top_out = top_out.reshape(top_out.shape[0], 1, top_out.shape[1])
        bottom_out = bottom_out.reshape(bottom_out.shape[0], 1, bottom_out.shape[1])
        x = torch.cat((top_out, bottom_out), dim=1)
        lstm_out, _ = self.lstm(x)
        lstm_out = lstm_out.reshape(lstm_out.shape[0], lstm_out.shape[1] * lstm_out.shape[2])
        x = self.fc(lstm_out)
        x = torch.sigmoid(x)
        return x
        