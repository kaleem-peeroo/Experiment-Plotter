import os
import sys
import click
import pandas as pd
import matplotlib.pyplot as plt

from InquirerPy import inquirer
from rich.pretty import pprint
from rich.console import Console

console = Console()

DATASET_PATHS = [
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

def get_column_name(df):
    choice = inquirer.fuzzy(
        message="Select a column name",
        choices=df.columns
    ).execute()

    return choice

def get_dataset_path():
    ds_index = click.prompt("Enter the index of the dataset you want to process: ", type=int, default=0)

    DATASET_PATH = DATASET_PATHS[ds_index]

    return pd.read_parquet(DATASET_PATH)

def get_experiment_name(experiment_names):
    choice = inquirer.fuzzy(
        message="Select an experiment name",
        choices=experiment_names
    ).execute()

    return choice

def main():
    for index, ds_path in enumerate(DATASET_PATHS):
        click.echo(f"{index}: {ds_path}")

    df = get_dataset_path()

    experiment_names = df['experiment_name'].unique()
    experiment_name = get_experiment_name(experiment_names)
    
    df = df[df['experiment_name'] == experiment_name]

    col_name = get_column_name(df)

    df = df[col_name]
    
    click.echo(f"Experiment Name: {experiment_name}")
    click.echo(f"Column Name: {col_name}")

    console.print(f"Number of rows: {df.shape[0]}")
    
    # Print how many nan values there are
    console.print(f"Number of NaN values: {df.isna().sum()}")

    # df = df.dropna(inplace=True)

    pprint(df.describe())
    pprint(df.head())
    pprint(df.tail())

    fig, ax = plt.subplots()
    ax.plot(df)
    ax.set_title(f"{experiment_name} - {col_name}")
    ax.set_xlabel("Increasing Time")
    ax.set_ylabel(col_name)

    # ax.set_yscale("log")

    os.makedirs("plots", exist_ok=True)
    plt.savefig(f"plots/{experiment_name}_{col_name}.png")
    console.print(f"Plot saved to plots/{experiment_name}_{col_name}.png")
    plt.close()

if __name__ == "__main__":
    main()
