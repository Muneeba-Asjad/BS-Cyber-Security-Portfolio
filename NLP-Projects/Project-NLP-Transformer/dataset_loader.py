# dataset_loader.py

from datasets import load_dataset


def load_imdb_dataset():
    """
    Load the IMDB dataset.
    """

    print("Loading IMDB dataset...")

    dataset = load_dataset("imdb")

    print("\nDataset Loaded Successfully!\n")

    print(dataset)

    print("\nTraining Samples :", len(dataset["train"]))
    print("Testing Samples  :", len(dataset["test"]))

    return dataset


if __name__ == "__main__":
    load_imdb_dataset()