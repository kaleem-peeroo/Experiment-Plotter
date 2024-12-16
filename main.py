import os
import sys
import click
import pandas as pd
# import matplotlib.pyplot as plt
import plotext as plt

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
    for index, ds_path in enumerate(DATASET_PATHS):
        click.echo(f"{index}: {ds_path}")

    ds_index = click.prompt("Enter the index of the dataset you want to process: ", type=int, default=0)

    DATASET_PATH = DATASET_PATHS[ds_index]

    return DATASET_PATH

def get_experiment_name(df):
    experiment_names = df['experiment_name'].unique()
    choice = inquirer.fuzzy(
        message="Select an experiment name",
        choices=experiment_names
    ).execute()

    return choice

def main():
    DEBUG_MODE = '--debug' in sys.argv
    
    if DEBUG_MODE:
        ds_path = DATASET_PATHS[0]
    else:
        ds_path = get_dataset_path()

    df = pd.read_parquet(ds_path)
    ds_name = "{} {}".format(
        os.path.basename(os.path.dirname(ds_path)),
        os.path.basename(ds_path).replace(".parquet", ""),
    )

    if DEBUG_MODE:
        experiment_name = "600SEC_1000B_1PUB_20SUB_REL_MC_0DUR_100LC"
    else:
        experiment_name = get_experiment_name(df)

    df = df[df['experiment_name'] == experiment_name]

    if DEBUG_MODE:
        col_name = "avg_mbps"
        # col_name = "latency_us"
    else:
        col_name = get_column_name(df)

    df = df[col_name].dropna()
    
    row_count = df.shape[0]
    
    plt.subplots(2, 1)
    plt.subplot(1, 1)
    plt.plot_size(100, 20)
    plt.plot(
        df,
        label=[         
            f"Mean: {int(df.mean())}",
            f"Median: {int(df.median())}",
            f"Min: {int(df.min())}",
            f"Max: {int(df.max())}",
        ]
    )
    plt.title(
        "{} - {} - {} ({} samples)".format(
            ds_name,
            experiment_name,
            col_name,
            row_count
        )
    )
    plt.xlabel("Increasing Time")
    plt.ylabel(col_name)
    plt.yscale("log")

    # Cut first 20% of the data
    df = df[int(row_count * 0.2):]
    row_count = df.shape[0]
    
    plt.subplot(2, 1)
    plt.plot(
        df,
        label=[         
            f"Mean: {int(df.mean())}",
            f"Median: {int(df.median())}",
            f"Min: {int(df.min())}",
            f"Max: {int(df.max())}",
        ]
    )
    plt.title(
        "{} - {} - {} ({} samples)".format(
            ds_name,
            experiment_name,
            col_name,
            row_count
        )
    )
    plt.xlabel("Increasing Time")
    plt.ylabel(col_name)
    plt.yscale("log")

    plt.show()

if __name__ == "__main__":
    main()
