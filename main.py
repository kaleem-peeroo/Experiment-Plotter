import os
import sys
import click
import pandas as pd

from InquirerPy import inquirer

dataset_paths = [
    "/Users/kaleem/PhD/Datasets/3PI/ml_data_collection_6mbps.parquet",      # Truncate 25%
    "/Users/kaleem/PhD/Datasets/3PI/ml_data_collection_8mbps.parquet",      # Truncate 25%

    "/Users/kaleem/PhD/Datasets/3PI/mcast_exploration.parquet",             # Truncate 25%

    "/Users/kaleem/PhD/Datasets/5PI/2P_2S_QoS_Capture.parquet",             # Truncate 25%
    "/Users/kaleem/PhD/Datasets/5PI/3P_1S_QoS_Capture.parquet",             # Truncate 25%
    "/Users/kaleem/PhD/Datasets/5PI/1P_3S_QoS_Capture.parquet",             # Truncate 25%  

    "/Users/kaleem/PhD/Datasets/5PI/ml_data_collection_24mbps.parquet",     # Truncate 30%
    "/Users/kaleem/PhD/Datasets/5PI/ml_data_collection_71mbps.parquet",     # Truncate 25%

    "/Users/kaleem/PhD/Datasets/5PI/1P_3S_Multicast_Exploration.parquet",   # Truncate 25%
    "/Users/kaleem/PhD/Datasets/5PI/2P_2S_Multicast_Exploration.parquet"    # Truncate 10%
]

def main():
    for index, ds_path in enumerate(dataset_paths):
        click.echo(f"{index}: {ds_path}")

    ds_index = click.prompt("Enter the index of the dataset you want to process: ", type=int, default=0)

    DATASET_PATH = dataset_paths[ds_index]

    df = pd.read_parquet(DATASET_PATH)
    experiment_names = df['experiment_name'].unique()

    choice = inquirer.fuzzy(
        message="Select an experiment name",
        choices=experiment_names
    ).execute()

    experiment_name = choice
    df = df[df['experiment_name'] == experiment_name]

    col_names = df.columns

    choice = inquirer.fuzzy(
        message="Select a column name",
        choices=col_names
    ).execute()

    click.echo(f"Experiment Name: {experiment_name}")
    click.echo(f"Column Name: {choice}")

if __name__ == "__main__":
    main()
