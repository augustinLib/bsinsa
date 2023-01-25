import os
import torch
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader


class CompatibilityDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(
            self,
            csv_file='../processed_data/combined_data.csv',
            root_dir='../images',
    ):
        """
        Args:
            csv_file (string): csv 파일의 경로
            root_dir (string): 모든 이미지가 존재하는 디렉토리 경로
            transform (callable, optional): 샘플에 적용될 Optional transform
        """
        self.data = pd.read_csv(csv_file).sample(frac=1).reset_index(drop=True)
        self.root_dir = root_dir
        self.output_size = (224, 224)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_row = self.data.iloc[idx]
        top_set_index, top_item_index = data_row['top_index'].split('_')
        bottom_set_index, bottom_item_index = data_row['bottom_index'].split('_')
        top_categoryid = data_row['top_categoryid']
        bottom_categoryid = data_row['bottom_categoryid']
        y = data_row['label']
        top_image = Image.open(os.path.join(self.root_dir, top_set_index, top_item_index + '.jpg'))
        bottom_image = Image.open(os.path.join(self.root_dir, bottom_set_index, bottom_item_index + '.jpg'))

        sample = {'top_image': top_image,
                  'bottom_image': bottom_image,
                  'y': y,
                  'top_categoryid': top_categoryid,
                  'bottom_categoryid': bottom_categoryid}

        sample = self.transform(sample)
        return sample

    def transform(self, sample):
        top_image, bottom_image, y = sample['top_image'], sample['bottom_image'], sample['y']

        new_h, new_w = self.output_size

        top_image = top_image.resize((new_h, new_w))
        bottom_image = bottom_image.resize((new_h, new_w))

        if top_image.mode != 'RGB':
            top_image = top_image.convert('RGB')
        if bottom_image.mode != 'RGB':
            bottom_image = bottom_image.convert('RGB')

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        top_image = torch.from_numpy(np.array(top_image) / 255).permute(2, 0, 1).float()
        bottom_image = torch.from_numpy(np.array(bottom_image) / 255).permute(2, 0, 1).float()
        return {'top_image': top_image,
                'bottom_image': bottom_image,
                'y': torch.tensor(y).long(),
                'top_categoryid': torch.tensor(sample['top_categoryid']),
                'bottom_categoryid': torch.tensor(sample['bottom_categoryid'])}
# transform into size of 224x224 using torchvision transform and transpose and totensor


if __name__ == '__main__':
    compatibility_dataset = CompatibilityDataset()
    dataloader = DataLoader(compatibility_dataset,
                            batch_size=4,
                            shuffle=True)
    dataiter = next(iter(dataloader))
    print(dataiter['top_image'].shape)
