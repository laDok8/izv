#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
import io
import os
import csv
import pickle

import numpy as np
import zipfile
import re

import requests as r
from bs4 import BeautifulSoup


# Kromě vestavěných knihoven (os, sys, re, requests …) byste si měli vystačit s:
# gzip, pickle, csv, zipfile, numpy, matplotlib, BeautifulSoup.
# Další knihovny je možné použít po schválení opravujícím (např ve fóru WIS).


class DataDownloader:
    """
    downloader/parser for zip files with accidents.csv files with predetermined structure

    Attributes:
        headers     Nazvy hlavicek jednotlivych CSV souboru, tyto nazvy nemente!
        regions     Dictionary s nazvy kraju : nazev csv souboru
    """

    headers = ["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a",
               "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27",
               "p28",
               "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a",
               "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t",
               "p5a"]

    dataTypes = [np.str_, np.int8, np.int8, np.datetime64, np.int8, np.str_, np.int8, np.int8, np.int8, np.int8,
                 np.int8, np.int8, np.int16, np.int8, np.int8, np.int8, np.int16, np.int8, np.int8, np.int32,
                 np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8,
                 np.int8, np.int8, np.int8, np.int8, np.str_, np.int8, np.int8, np.int8, np.int8, np.int8,
                 np.int8, np.int16, np.int8, np.int8, np.int8, np.float64, np.float64, np.float64, np.float64,
                 np.float64, np.float64, np.str_, np.str_, np.str_, np.str_, np.str_, np.int32, np.str_, np.str_,
                 np.str_, np.int32, np.int32, np.str_, np.int8, np.str_]

    regions = {
        "PHA": "00",
        "STC": "01",
        "JHC": "02",
        "PLK": "03",
        "ULK": "04",
        "HKK": "05",
        "JHM": "06",
        "MSK": "07",
        "OLK": "14",
        "ZLK": "15",
        "VYS": "16",
        "PAK": "17",
        "LBK": "18",
        "KVK": "19",
    }

    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/", folder="data", cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = folder
        self.cache_filename = os.path.join(self.folder, cache_filename)
        self.cache = {}
        os.makedirs(folder, exist_ok=True)

    def download_data(self):
        """
        download zips with latest data into **folder**
        function assumes **url** contains table that has buttons sorted chronologically from left to right
        """
        rawHtml = r.get(self.url)
        rawHtml.raise_for_status()

        soup = BeautifulSoup(rawHtml.text, 'html.parser')
        htmlTable = soup.find("table")
        # check all rows in table for last existing button
        for rows in htmlTable.findAll('tr'):
            for button in reversed(rows.findAll('button')):
                filepath = button["onclick"].replace('download(\'', '')[:-2]
                fname = os.path.basename(filepath)
                # download if not present
                if not os.path.isfile(os.path.join(self.folder, fname)):
                    with r.get(self.url + filepath) as zips, open(os.path.join(self.folder, fname), 'wb') as fp:
                        fp.write(zips.content)
                # only need last month ( last button in row)
                break

    def parse_region_data(self, region):
        """
        download data ( if missing) and parse from all zip files
        :param region: region to parse
        :return: dataset of accidents over given region
        """
        _dict = {}
        for hdr in self.headers:
            _dict[hdr] = []

        self.download_data()
        files = [os.path.join(self.folder, f) for f in os.listdir(self.folder)]
        for zips in files:
            if not zipfile.is_zipfile(zips):
                continue
            with zipfile.ZipFile(zips) as zf:
                with zf.open(self.regions[region] + '.csv', 'r') as f:
                    reader = csv.reader(io.TextIOWrapper(f, 'cp1250'), delimiter=';', quotechar='"')
                    for row in reader:
                        for (i, hdr) in enumerate(self.headers):
                            _dict[hdr] += [row[i]]

        # convert to np array
        _dict = ({key: np.array(y) for (key, y) in _dict.items()})

        # convert types & replace commas with dot if neccesary
        for hd, typ in zip(self.headers, self.dataTypes):
            _dict[hd][_dict[hd] == ''] = -1
            try:
                if typ == np.float64:
                    _dict[hd] = np.char.replace(_dict[hd], ',', '.')
                _dict[hd] = _dict[hd].astype(typ)
            except (Exception,):
                pass

        # remove duplicities
        indices = np.unique(_dict[self.headers[0]], return_index=True)[1]
        mask = np.zeros(len(_dict[self.headers[0]]), dtype=bool)
        mask[indices] = True
        for (key, arr) in _dict.items():
            _dict[key] = arr[mask]

        # add region row
        _dict["region"] = np.repeat(str(region), len(_dict[self.headers[0]]))
        return _dict

    def get_dict(self, regions=None):
        """
        get accumulated data over given regions
        function stores cached data in **folder/cache_filename**
        :param regions: regions from self.regions, ALL if unspecified
        :return: accumulated dataset over all regions
        """
        regions = regions if regions else self.regions.keys()
        acc = {}
        for hdr, typ in zip(self.headers, self.dataTypes):
            acc[hdr] = np.array([], dtype=typ)
        acc['region'] = np.array([], dtype=np.str_)

        for reg in regions:
            fName = self.cache_filename
            if len(re.findall('{}', fName)) != 0:
                fName = re.sub('{}', reg, fName)
            else:
                fName += reg

            # is cached?
            if reg in self.cache.keys():
                _data = self.cache[reg]
            elif os.path.isfile(fName):
                with gzip.open(fName, "rb") as f:
                    _data = pickle.load(f)
            else:
                _data = self.parse_region_data(reg)

            # accumulate data
            for (k, v) in _data.items():
                acc[k] = np.append(acc[k], v)

            # cache
            if reg not in self.cache.keys():
                self.cache[reg] = _data
            if not os.path.isfile(fName):
                with gzip.open(fName, "wb", compresslevel=4) as f:
                    pickle.dump(_data, f)

        return acc


if __name__ == "__main__":
    """
    show function of DataDownloader with smaller dataset
    """
    source = DataDownloader()
    data = source.get_dict(["PHA", "JHM", "VYS"])
    print("number of records: " + str(data["p1"].size))
    print("columns: " + str([k for k in data.keys()]))
    print("regions in dataset: " + str(np.unique(data["region"])))
