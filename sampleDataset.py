import pandas as pd
import os 
DATASET_TO_SAMPLE_PATH = "DATASET/train.tsv"
DATASET_TO_WRITE_PATH = "SampledDataset/SampledDataset.tsv"

CLEANED_DATASET_PATH = "SampledDataset/CleanedTrainDataset.tsv"

def clean_dataset(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The input path {input_path} does not exist.")

    if os.path.exists(output_path):
        os.remove(output_path)

    df = pd.read_csv(input_path, sep="\t")
    bSomethingRemoved = False
    for label in df["label"]:
        # If label is not in the list remove the entry from the dataset
        if label not in ["true", "false", "mixture", "unproven"]:
            # remove the NaN entries from the dataset
            df = df.dropna(subset=["label"])
            # remove the error-entry from the dataset
            df = df[df["label"] != "snopes"]
            bSomethingRemoved = True

    # write the cleaned dataset to the same path
    if bSomethingRemoved:
        df.to_csv(output_path, sep="\t", index=False)
        print("Dataset is cleaned :)")
    else :
        print("Dataset is already clean :)")



def sample_dataset(input_path, output_path, sample_size=100):
    """
    Samples a dataset from the input path and writes it to the output path.
    """

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The input path {input_path} does not exist.")
    # if file already exists, remove it
    if os.path.exists(output_path):
        os.remove(output_path)

    # read csv
    df = pd.read_csv(input_path, sep="\t")
    lTrueClaim = []
    lFalseClaim = []
    lMixtureClaim = []
    lUnprovenClaim = []
    # we want to find for each label ("true" and "false" "mixture" and "unproven") 25 claims and sample them into output
    for label in df["label"]:
        # The label is not in the list of labels we want to sample, so we skip it -> it must be an error in the dataset
        if label not in ["true", "false", "mixture", "unproven"]:
            raise ValueError(f"Label {label} is not in the list of labels we want to sample.")
            
        if label == "true":
            lTrueClaim.append(label)
        elif label == "false":
            lFalseClaim.append(label)
        elif label == "mixture":
            lMixtureClaim.append(label)
        elif label == "unproven":
            lUnprovenClaim.append(label)

    # sample 25 claims for each label
    lTrueClaim = df[df["label"] == "true"].sample(n=25, random_state=42)
    lFalseClaim = df[df["label"] == "false"].sample(n=25, random_state=42)
    lMixtureClaim = df[df["label"] == "mixture"].sample(n=25, random_state=42)
    lUnprovenClaim = df[df["label"] == "unproven"].sample(n=25, random_state=42)

    # concatenate the sampled claims into a single dataframe
    sampled_df = pd.concat([lTrueClaim, lFalseClaim, lMixtureClaim, lUnprovenClaim])

    # write the sampled dataframe to the output path

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    sampled_df.to_csv(output_path, sep="\t", index=False)

def main():
    clean_dataset(DATASET_TO_SAMPLE_PATH,CLEANED_DATASET_PATH)
    sample_dataset(CLEANED_DATASET_PATH, DATASET_TO_WRITE_PATH, sample_size=100)


if __name__ == "__main__":
    main()
