import numpy as np

def dice_score(pred, target):
    pred = pred.astype(np.float32)
    target = target.astype(np.float32)

    intersection = np.sum(pred * target)

    return (2 * intersection + 1e-7) / (np.sum(pred) + np.sum(target) + 1e-7)


def iou_score(pred, target):
    pred = pred.astype(np.float32)
    target = target.astype(np.float32)

    intersection = np.sum(pred * target)
    union = np.sum(pred) + np.sum(target) - intersection

    return (intersection + 1e-7) / (union + 1e-7)


def accuracy_score(pred, target):
    return np.mean(pred == target)