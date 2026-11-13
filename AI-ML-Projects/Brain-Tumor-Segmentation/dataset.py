import os
import cv2
import torch
from torch.utils.data import Dataset


class BrainDataset(Dataset):

    def __init__(self, root_dir):

        self.images = []

        for folder in os.listdir(root_dir):

            folder_path = os.path.join(root_dir, folder)

            if os.path.isdir(folder_path):

                for file in os.listdir(folder_path):

                    if file.endswith(".tif") and "mask" not in file:

                        image_path = os.path.join(folder_path,file)

                        mask_path = image_path.replace(
                            ".tif",
                            "_mask.tif"
                        )

                        if os.path.exists(mask_path):

                            self.images.append(
                                (image_path, mask_path)
                            )


        print("Total images found:",len(self.images))


    def __len__(self):
        return len(self.images)


    def __getitem__(self,index):

        image_path, mask_path = self.images[index]


        img=cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )


        mask=cv2.imread(
            mask_path,
            cv2.IMREAD_GRAYSCALE
        )


        img=cv2.resize(img,(256,256))
        mask=cv2.resize(mask,(256,256))


        img=img/255.0

        mask=mask/255.0


        img=torch.tensor(
            img,
            dtype=torch.float32
        ).unsqueeze(0)


        mask=torch.tensor(
            mask,
            dtype=torch.float32
        ).unsqueeze(0)


        return img,mask