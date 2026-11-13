from dataset import BrainTumorDataset

dataset = BrainTumorDataset("dataset/kaggle_3m")

print("Total Images :", len(dataset))

image, mask = dataset[0]

print("Image Shape :", image.shape)
print("Mask Shape :", mask.shape)