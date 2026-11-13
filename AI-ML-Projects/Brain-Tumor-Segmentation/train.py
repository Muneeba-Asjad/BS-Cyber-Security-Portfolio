import torch
import os
from torch.utils.data import DataLoader, Subset
from torch import nn, optim
from model import UNet
from dataset import BrainDataset

# ----------------------------
# Device
# ----------------------------

device = torch.device("cpu")
print("Using device:", device)

# ----------------------------
# Dataset
# ----------------------------

dataset = BrainDataset("dataset/kaggle_3m")

# Sirf pehli 300 images use hongi
dataset = Subset(dataset, range(300))

loader = DataLoader(
    dataset,
    batch_size=8,
    shuffle=True,
    num_workers=0
)

print("Training Images:", len(dataset))

# ----------------------------
# Model
# ----------------------------

model = UNet().to(device)

# ----------------------------
# Loss
# ----------------------------

bce_loss = nn.BCELoss()


def dice_loss(pred, target):
    smooth = 1

    intersection = (pred * target).sum()

    dice = (
        2 * intersection + smooth
    ) / (
        pred.sum() + target.sum() + smooth
    )

    return 1 - dice


# ----------------------------
# Optimizer
# ----------------------------

optimizer = optim.Adam(
    model.parameters(),
    lr=0.0001
)

# ----------------------------
# Training
# ----------------------------

epochs = 3

for epoch in range(epochs):

    model.train()

    total_loss = 0

    for batch, (images, masks) in enumerate(loader):

        images = images.to(device)
        masks = masks.to(device)

        predictions = model(images)

        loss = (
            bce_loss(predictions, masks)
            + dice_loss(predictions, masks)
        )

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        if batch % 10 == 0:
            print(
                f"Epoch {epoch+1}/{epochs} "
                f"Batch {batch}/{len(loader)} "
                f"Loss: {loss.item():.4f}"
            )

    avg_loss = total_loss / len(loader)

    print(
        f"\nEpoch {epoch+1} completed "
        f"Average Loss: {avg_loss:.4f}\n"
    )

    # Har epoch ke baad model save hoga
    os.makedirs("models", exist_ok=True)

    torch.save(
        model.state_dict(),
        "models/unet_model.pth"
    )

    print(f"✅ Model saved after Epoch {epoch+1}")

print("\n================================")
print("Training Completed Successfully")
print("Model saved: models/unet_model.pth")
print("================================")