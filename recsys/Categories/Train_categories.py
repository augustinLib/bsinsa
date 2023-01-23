import os
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from torch import nn
from torchvision import transforms
import torchvision.datasets as datasets
import os
from Preprocess_categories import *
from Mobilenet_categories import *

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


num_classes = 5
batch_size = 10
num_workers = 2
lr = 1e-3
total_epoch = 10
big_cls = 'total'

location = '/home/augustin/project/bitamin-conference/recsys/model/modelfile/'
dir_trn_tst ='/home/augustin/project/bitamin-conference/data/crawling/data/image'
train_dir = "./data/crawling/data/image"
test_dir = "./data/crawling/data/image"


train_dataset = datasets.ImageFolder(
    train_dir,
    transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor()
    ]))

train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=batch_size, shuffle=True,
    num_workers=num_workers, pin_memory=True, drop_last=False)

test_dataset = datasets.ImageFolder(test_dir, transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor()]))

test_loader = torch.utils.data.DataLoader(
    test_dataset,
    batch_size=batch_size, shuffle=False,
    num_workers=num_workers, pin_memory=True)

if __name__ == "__main__":
  # [1/540, 1/649, 1/616, 1/679, 1/174]
  weights = [0.0004, 0.0004, 0.0004, 0.0004, 0.0005] #[ 1 / number of instances for each class]
  class_weights = torch.FloatTensor(weights) # .cuda()

  model = SuperLightMobileNet(num_classes).to(device)
  CEloss = nn.CrossEntropyLoss(weight=class_weights).cuda()
  optimizer = torch.optim.Adam(model.parameters(), lr=lr)

  total_iteration_per_epoch = int(np.ceil(len(train_dataset)/batch_size))

  for epoch in range(1, total_epoch + 1):
      model.train()
      for itereation, (input, target) in enumerate(train_loader):
          images = input.to(device)
          labels = target.to(device)

          # Forward pass
          outputs = model(images)
          loss = CEloss(outputs, labels)

          # Backward and optimize
          optimizer.zero_grad()
          loss.backward()
          optimizer.step()
          
          if itereation % 100 ==0:
              print('Epoch [{}/{}], Iteration [{}/{}] Loss: {:.4f}'.format(epoch, total_epoch, itereation+1, total_iteration_per_epoch, loss.item()))
    
      if epoch % 3 == 0:
        torch.save(model.state_dict(), os.path.join(location, big_cls+ '_'+'model_light' + str(epoch) + '_' + str(lr) + '_' + str(batch_size) +'.pth'))
      model.eval()
      
      # 클래스별 정확도
      pred_grid = [[0 for _ in range(5)] for _ in range(5)]
      class_correct = list(0 for i in range(5))
      class_total = list(0 for i in range(5))

      with torch.no_grad():
        for data in test_loader:  
            images, labels = data # 배치 한개의 이미지와 레이블들
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            c = (predicted==labels).squeeze()
            
            for i in range(labels.shape[0]):
                label = labels[i]
                pred_grid[label][predicted[i]] += 1
                class_correct[label] += c[i].item()
                class_total[label] += 1

      classes = list(train_dataset.class_to_idx.keys())
      for i in range(5):
        if class_total[i] ==0:
            continue
        print('Accuracy of {} : {}%'.format(classes[i], 100*class_correct[i]/class_total[i]))
        print('Total Accuracy : {}'.format(100*sum(class_correct)/sum(class_total)))
        for i in pred_grid:
            print(i)



