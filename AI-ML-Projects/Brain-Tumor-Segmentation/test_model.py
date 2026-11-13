import torch
from model import UNet

model = UNet()

x = torch.randn(1, 1, 256, 256)

y = model(x)

print("Input Shape :", x.shape)
print("Output Shape:", y.shape)