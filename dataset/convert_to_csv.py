import pandas as pd
import numpy as np
import os


def parse_sparse_line(line):
    """Parse a single line of sparse vector format"""
    parts = line.strip().split()
    label = int(parts[0])  # First number is the label/class

    features = {}
    for part in parts[1:]:
        if ":" in part:
            idx, value = part.split(":")
            features[int(idx)] = float(value)

    return label, features


def convert_dat_to_csv(dat_file_path, csv_file_path):
    """Convert .dat file to CSV format"""
    print(f"Reading {dat_file_path}...")

    all_labels = []
    all_features = []
    max_feature_idx = 0

    # First pass: collect all data and find max feature index
    with open(dat_file_path, "r") as f:
        for line_num, line in enumerate(f, 1):
            if line.strip():
                try:
                    label, features = parse_sparse_line(line)
                    all_labels.append(label)
                    all_features.append(features)

                    if features:
                        max_feature_idx = max(max_feature_idx, max(features.keys()))

                except Exception as e:
                    print(f"Error parsing line {line_num}: {e}")
                    continue

    print(f"Found {len(all_labels)} samples with {max_feature_idx} features")

    # Create column names
    columns = ["label"] + [f"feature_{i}" for i in range(1, max_feature_idx + 1)]

    # Create the data matrix
    data = []
    for i, (label, features) in enumerate(zip(all_labels, all_features)):
        row = [label]  # Start with label

        # Add feature values (0 for missing features in sparse format)
        for feature_idx in range(1, max_feature_idx + 1):
            row.append(features.get(feature_idx, 0.0))

        data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Save to CSV
    df.to_csv(csv_file_path, index=False)
    print(f"Successfully converted to {csv_file_path}")
    print(f"Shape: {df.shape}")
    print(f"First few rows:")
    print(df.head())

    return df


def convert_all_dat_files():
    """Convert all .dat files in the Dataset folder"""
    dataset_folder = (
        r"c:\Users\Raghav\OneDrive\Desktop\project\coal mine project\Dataset"
    )

    dat_files = [
        f
        for f in os.listdir(dataset_folder)
        if f.endswith(".dat") and not f.endswith(".dat.json")
    ]

    for dat_file in dat_files:
        dat_path = os.path.join(dataset_folder, dat_file)
        csv_file = dat_file.replace(".dat", ".csv")
        csv_path = os.path.join(dataset_folder, csv_file)

        print(f"\n{'='*50}")
        print(f"Converting {dat_file} to {csv_file}")
        print(f"{'='*50}")

        try:
            convert_dat_to_csv(dat_path, csv_path)
        except Exception as e:
            print(f"Error converting {dat_file}: {e}")


if __name__ == "__main__":
    # Convert all .dat files to CSV
    convert_all_dat_files()

    print(f"\n{'='*50}")
    print("Conversion complete!")
    print("CSV files have been created in the Dataset folder.")
    print(f"{'='*50}")
