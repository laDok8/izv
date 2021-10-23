#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib import cm
import os
# povolene jsou pouze zakladni knihovny (os, sys) a knihovny numpy, matplotlib a argparse

from download import DataDownloader


def plot_stat(data_source,
              fig_location=None,
              show_figure=False):
    """
    Create accident graph on given dataset
    :param data_source: input dataset
    :param fig_location: location to store plot
    :param show_figure: True/False parameter to show window with plot
    """
    if fig_location:
        os.makedirs(fig_location, exist_ok=True)
    # TODO switch regs
    y_labels = ["Přerušovaná žlutá", "Semafor mimo provoz", "Dopravní značky", "Přenosné dopravní značky",
                "Nevyznačená", "Žádná úprava"]
    occurrences = np.empty((6, 0))
    # get region list
    regs = np.unique(data_source["region"])
    for reg in regs:
        pha_index = np.argwhere(data_source['region'] == reg)
        pha = np.reshape(data_source["p24"][pha_index], -1)
        pha_occur = np.bincount(pha.astype(int))
        occurrences = np.append(occurrences, np.transpose([pha_occur]), axis=1)
    occurrences[occurrences == 0] = np.nan

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(2, 1, 1)
    ax.set_title("Absolutně")
    ax.set_xticks(np.arange(len(regs)))
    ax.set_xticklabels(regs)
    ax.set_yticks(np.arange(len(y_labels)))
    ax.set_yticklabels(y_labels)
    i = ax.imshow(occurrences, norm=matplotlib.colors.LogNorm())
    cb = fig.colorbar(i)
    cb.set_label('Počet nehod', rotation=90)

    sum_cause = np.nansum(occurrences, axis=1, keepdims=True)
    sum_cause[sum_cause == 0] = 1
    normalized = (occurrences / sum_cause) * 100
    ax = fig.add_subplot(2, 1, 2)
    ax.set_title("Relativně vůči příčíně")
    ax.set_xticks(np.arange(len(regs)))
    ax.set_xticklabels(regs)
    ax.set_yticks(np.arange(len(y_labels)))
    ax.set_yticklabels(y_labels)
    i = ax.imshow(normalized, cmap=cm.plasma)
    cb = fig.colorbar(i)
    cb.set_label('Podíl nehod pro danou příčinu [%]', rotation=90)

    if fig_location:
        plt.savefig(os.path.join(fig_location, "stat.png"))

    if show_figure:
        plt.show()
        plt.close()


if __name__ == "__main__":
    """Parse accidents in regions by default without showing/storing graph
    to save data fig_location or show_figure cli parameters must be specified
    """
    # parse cli
    parser = argparse.ArgumentParser()
    parser.add_argument('--fig_location', type=str)
    parser.add_argument('--show_figure', type=bool, default=False)
    args = parser.parse_args()
    # get data & plot statistics
    source = DataDownloader()
    data_source = source.get_dict()
    plot_stat(data_source, args.fig_location, args.show_figure)
