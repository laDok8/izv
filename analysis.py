#!/usr/bin/env python3.9
# coding=utf-8
from matplotlib import pyplot as plt
from matplotlib import dates as mDates
import pandas as pd
import seaborn as sns
import os
import requests as r


def _download_accidents(url: str = "http://ehw.fit.vutbr.cz/izv/accidents.pkl.gz", fname: str = "accidents.pkl.gz"):
    """
    Download compressed data if missing
    """
    if not os.path.isfile(fname):
        with r.get(url) as zips, open(fname, 'wb') as fp:
            fp.write(zips.content)


def get_dataframe(filename: str = "accidents.pkl.gz", verbose: bool = False) -> pd.DataFrame:
    """
    Get data from compressed fie
    :param filename: name of file
    :param verbose: show file sizes before/after optimization
    """
    df = pd.read_pickle(filename)
    if verbose:
        mem = df.memory_usage(deep=True).sum() / (1024 ** 2)
        print(f"orig_size: {mem:.1f} MB")

    convertable = ["p36", "p37", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
                   "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27",
                   "p28",
                   "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53",
                   "p55a",
                   "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s",
                   "t",
                   "p5a"]
    df['p2a'] = df['p2a'].astype('datetime64')
    df.rename(columns={'p2a': 'date'}, inplace=True)
    df[convertable] = df[convertable].astype('category')

    if verbose:
        mem = df.memory_usage(deep=True).sum() / (1024 ** 2)
        print(f"new_size:  {mem:.1f} MB")
    return df


def plot_roadtype(df: pd.DataFrame, fig_location: str = None,
                  show_figure: bool = False):
    """
    Create plot of accidents in relation to road type
    :param df: dataframe
    :param fig_location: location to store plot
    :param show_figure: True to show visuals
    """
    _rename = {
        0: 'Ostatn?? komunikace',
        1: 'Dvoupruhov??',
        2: 'T????pruhov??',
        3: '??ty??pruhov??',
        4: '??ty??pruhov??',
        5: 'V??cepruhov??',
        6: 'Rychlostn?? komunikace',
    }
    df['hodnota'] = 1
    # make hard copy because of changing labels
    road_df = df.loc[:, ['region', 'p21', 'hodnota']]
    road_df['p21'].replace(_rename, inplace=True)
    road_df.rename(columns={'region': 'Kraj'}, inplace=True)
    road_df = pd.pivot_table(road_df, columns="Kraj", index='p21', values='hodnota', aggfunc='sum')
    road_df = road_df[['HKK', 'JHC', 'JHM', 'KVK']]
    road_df = road_df.stack().reset_index(name='Po??et nehod')

    # graphing
    sns.set_theme()
    sns.set_context("paper")
    fig = sns.FacetGrid(road_df, col='p21', sharex=False, sharey=False, col_wrap=3)
    fig.map(sns.barplot, 'Kraj', 'Po??et nehod', palette="deep")
    fig.set_titles('{col_name}')
    fig.fig.suptitle('Nehodovost podle druhu silnic')
    fig.tight_layout()

    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()
        plt.close()


def plot_animals(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """
    Create plot of accidents caused by animals
    :param df: dataframe
    :param fig_location: location to store plot
    :param show_figure: True to show visuals
    """
    df['hodnota'] = 1
    _rename = {
        1: '??idi??em',
        2: '??idi??em',
        4: 'Zv??????',
        0: 'Jin??', 3: 'Jin??', 5: 'Jin??', 6: 'Jin??', 7: 'Jin??',
    }

    animals_df = df[df['region'].isin(['HKK', 'JHC', 'JHM', 'KVK']) & (df['p58'] == 5)]
    animals_df = animals_df.loc[:, ['date', 'p10', 'hodnota', 'region']]
    animals_df['p10'].replace(_rename, inplace=True)
    # remove 2021
    animals_df = animals_df[animals_df['date'].dt.year != 2021]
    animals_df['month'] = animals_df['date'].dt.month
    # aggregate month&region&cause
    animals_df = animals_df.groupby(['region', 'month', 'p10']).agg('sum').reset_index()
    animals_df.rename(columns={'hodnota': 'Po??et nehod', 'month': 'M??s??c'}, inplace=True)

    # graphing
    sns.set_theme()
    sns.set_context("paper")
    fig = sns.FacetGrid(animals_df, col='region', sharex=False, sharey=False, col_wrap=2, height=4, aspect=1.5)
    fig.map_dataframe(sns.barplot, x='M??s??c', y='Po??et nehod', hue='p10', palette="deep", order=None)
    fig.set_titles('Kraj: {col_name}')
    fig.fig.suptitle('Nehodovost zavin??n?? zv??????')
    fig.add_legend()
    fig.tight_layout()

    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()
        plt.close()


def plot_conditions(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    """
    Create plot of accidents caused by weather
    :param df: dataframe
    :param fig_location: location to store plot
    :param show_figure: True to show visuals
    """
    df['hodnota'] = 1
    _rename = {
        1: 'nezt????en??',
        2: 'mlha',
        3: 'na po????tku de??t??',
        4: 'd??????',
        5: 'sn????en??',
        6: 'n??led??',
        7: 'n??razov?? v??tr',
    }

    wind_df = df[df['region'].isin(['HKK', 'JHC', 'JHM', 'KVK']) & (df['p18'] != 0)]
    wind_df = wind_df.loc[:, ['date', 'p18', 'hodnota', 'region']]
    wind_df['p18'].replace(_rename, inplace=True)
    wind_df = pd.pivot_table(wind_df, columns='p18', index=['region', 'date'], values='hodnota', aggfunc='sum')

    wind_df = wind_df.stack(level='p18').reset_index(name='Po??et nehod')
    wind_df = wind_df.groupby(['region', 'p18', pd.Grouper(freq='M', key='date')]).sum()
    wind_df = wind_df.reset_index()

    # remove >2021
    wind_df = wind_df[(wind_df['date'] < '2021') & (wind_df['date'] > '2015')]
    wind_df.rename(columns={'date': 'Datum'}, inplace=True)

    # graphing
    sns.set_theme()
    sns.set_context("paper")
    fig = sns.FacetGrid(wind_df, col='region', sharex=False, sharey=False, col_wrap=2, height=4, aspect=1.5)
    g = fig.map_dataframe(sns.lineplot, x='Datum', y='Po??et nehod', hue='p18', palette="deep")
    for ax in g.axes.flatten():
        ax.xaxis.set_major_formatter(mDates.DateFormatter('%m/%y'))
    fig.set_titles('Kraj: {col_name}')
    fig.fig.suptitle('Nehodovost vlivem pov??trnostn??ch podm??nek')
    fig.add_legend()
    fig.tight_layout()

    if fig_location:
        plt.savefig(fig_location)

    if show_figure:
        plt.show()
        plt.close()


if __name__ == "__main__":
    _download_accidents()
    df = get_dataframe("accidents.pkl.gz", verbose=True)
    plot_roadtype(df, fig_location="01_roadtype.png", )
    plot_animals(df, "02_animals.png", )
    plot_conditions(df, "03_conditions.png", )
