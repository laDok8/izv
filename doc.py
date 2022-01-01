#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot(filename: str = "accidents.pkl.gz", fig_location: str = "fig.png") -> pd.DataFrame:
    """
    Plot alcohol based accidents information
    :param filename: name of file with data
    :param fig_location: name of file to store plot
    """
    df = pd.read_pickle(filename)[['p11', 'p6', 'region', 'p2a']]
    before = df.shape[0]
    print('datovy rozsah:', df['p2a'].min(), ' -- ', df['p2a'].max())

    # pouze s alkoholem a odstraneni neznamych druhu nehod
    df = df.loc[~df['p11'].isin([2, 0])]
    print('nehod pod vlivem latek:', df.shape[0])
    print(f'podil daných nehod z celku: {df.shape[0] * 100 / before:2.2f} %')
    df = df.loc[~df['p6'].isin([0])]
    print('dobře zformovaná data:', df.shape[0])

    # druh nehody
    df["p6"] = df["p6"].replace({
        1: "vozidlo",
        2: 'statická překážka',
        3: 'statická překážka',
        4: "živé objekty",
        5: "živé objekty",
        6: "živé objekty",
        7: "vozidlo",
        8: "vozidlo",
        9: "havárie"
    })
    df["p11"] = df["p11"].replace({
        1: "<0,24 ‰",
        3: "0,24 ‰ - 0,5 ‰",
        4: "drogy",
        5: "alkohol + drogy",
        6: "0,5 ‰ - 0,8 ‰",
        7: "0,8 ‰ - 1,0 ‰",
        8: "1,0 ‰ - 1,5 ‰",
        9: ">1,5 ‰"
    })

    df1 = df.groupby(['region']).agg('count').reset_index().rename(columns={'p11': 'počet nehod'})[
        ['region', 'počet nehod']].rename(columns={'region': 'kraj'})
    print(f'podil kraje s největším/nejmenším poctem nehod: {df1["počet nehod"].max() / df1["počet nehod"].min():2.1f}')

    df2 = df.groupby(['p11', 'p6']).agg('count').reset_index().rename(
        columns={'p6': 'druh nehody', 'p11': 'ovlivnění', 'region': 'počet nehod'})
    nehody_alk = df2.loc[~df2["ovlivnění"].isin(["drogy"])]["počet nehod"].sum() * 100
    print(f'nehod s alkoholem: {nehody_alk / df2["počet nehod"].sum():2.2f} %')

    # plot
    sns.set_theme(style="ticks", rc={"axes.spines.right": False, "axes.spines.top": False})
    g = sns.catplot(kind='bar', data=df2, y='ovlivnění', x='počet nehod', hue='druh nehody')
    g.fig.suptitle('Cíl srážky v opilosti')
    g.legend.set_bbox_to_anchor([0.9, 0.7])
    g.fig.tight_layout()
    # g.fig.show()
    plt.savefig(fig_location)

    # print data
    nehody_static = df2.loc[~df2["druh nehody"].isin(["statická překážka"])]["počet nehod"].sum() * 100
    print(f'podil statických překážek: {nehody_static / df2["počet nehod"].sum():2.2f} %')
    print('nehod vůči živým bytostem:', df2.loc[df2["druh nehody"].isin(["živé objekty"])]["počet nehod"].sum())
    nehody_ovliv = df2.loc[df2["ovlivnění"].isin([">1,5 ‰"])]["počet nehod"].sum() * 100
    print(f'podil nehod pod vlivem >1,5 ‰: {nehody_ovliv / df.shape[0]:2.2f} %')

    print("\ncsv data:")
    df1 = df1.append({'kraj': 'celkem', 'počet nehod': df1["počet nehod"].sum()}, ignore_index=True)
    print(df1.to_csv(index=False, sep="\t"))


if __name__ == "__main__":
    plot()
