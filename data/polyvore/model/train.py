# import SiamNet and implement the lightning module

# Path: data/polyvore/model/train.py
# Compare this snippet from data/polyvore/model/train.py:
import torch
import pytorch_lightning as pl
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger
from torch.utils.data import DataLoader
from torch.utils.data import random_split

from data.polyvore.model.model import CompatibilityModel
from data.polyvore.model.dataloader import CompatibilityDataset


class SiamNetModule(pl.LightningModule):
    def __init__(self, learning_rate=0.0001, batch_size=8):
        super().__init__()
        self.model = CompatibilityModel()
        self.loss = torch.nn.BCEWithLogitsLoss()
        self.val_loss = torch.nn.L1Loss()
        self.learning_rate = learning_rate
        self.batch_size = batch_size

    def training_step(self, batch):
        top, bottom, y = batch['top_image'], batch['bottom_image'], batch['y']
        y_hat = self.model(top, bottom)
        loss = self.loss(y_hat.float().flatten(), y.float())
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        top, bottom, y = batch['top_image'], batch['bottom_image'], batch['y']
        y_hat = self.model(top, bottom)
        loss = self.val_loss(y_hat.float().flatten(), y.float())
        self.log('val_loss', loss)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer


# train the model

# Path: data/polyvore/model/train.py

if __name__ == '__main__':
    logger = TensorBoardLogger('lightning_logs', name='siamnet')
    dataset = CompatibilityDataset()
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=16, num_workers=4, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16, num_workers=4, shuffle=False)

    trainer = Trainer(
        accelerator='mps',
        max_epochs=10,
        logger=logger,
        auto_lr_find=True,
    )
    model = SiamNetModule(learning_rate=0.1, batch_size=16)

    # for param in model.model.resnet.parameters():
    #     param.requires_grad = False

    trainer.fit(model,
                train_dataloaders=train_loader,
                val_dataloaders=val_loader, )

    model.save('siamnet.pt')