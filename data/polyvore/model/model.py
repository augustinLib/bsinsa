# torch pretrained resnet

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models


class ResNet(nn.Module):
    def __init__(self, embedding=256):
        super(ResNet, self).__init__()
        self.resnet = models.resnet18(pretrained=True)
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, 8 * embedding)

    def forward(self, x):
        return self.resnet(x)


class SiamNet(nn.Module):
    def __init__(self, embedding=256):
        super(SiamNet, self).__init__()
        self.resnet = ResNet(embedding)
        self.fc1 = nn.Linear(16 * embedding, 4 * embedding)
        self.fc2 = nn.Linear(4 * embedding, embedding)
        self.fc3 = nn.Linear(embedding, 2)

    def forward(self, top, bottom):
        top_out = self.resnet(top)
        bottom_out = self.resnet(bottom)
        x = torch.cat((top_out, bottom_out), dim=1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = torch.sigmoid(x)
        return x
        