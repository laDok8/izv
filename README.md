Hodnoceni prvni casti projektu: 
================================================================================
```
+2 delky vsech datovych sloupcu jsou stejne (az 2 bodu)
+2 stahlo se 95_835 zaznamu (az 2 bodu)
+2 uspesne se stahl Plzensky kraj (s chybou v textu) (az 2 bodu)
+1 stahl se Karlovarsky kraj bez duplikatu (az 1 bodu)
+1 podarilo se vytvorit pandas.DataFrame (az 1 bodu)
+0 rozumne rozlozeni datovych typu (az 1 bodu)
+0 souradnice jsou spravne jako floaty i s desetinnymi misty (az 1 bodu)
+0 neni mozne hodnotit cas 1.29 s, jelikoz t1, t4 a t5 neprosly (az 2 bodu)
+1 obrazky se ulozily spravne (a.png, ./b.png, t/c.png) (az 1 bodu)
+3.00 kvalita kodu downloader.py (az 3 bodu)
+3.00 kvalita kodu get_stat.py (az 3 bodu)
+1.00 graf z get_stat.py (az 2 bodu)
+0 bonus (az 0 bodu)
CELKEM: 16.0 bodu
```

Komentar k hodnoceni
================================================================================
v poradku, ale cbary by mely mit oznacene krajove hodnoty (0 a 10**5)

Hodnoceni druhe casti projektu: 
================================================================================
```
+1.00 pouzite kategoricke typy (>=2) (az 1 bodu)
+0.00 ostatni typy jsou korektni (ints>30 & floats>=6) (az 1 bodu)
+1.00 vhodne vyuziti pameti (< 500 MB) (az 1 bodu)
+1.00 spravne konvertovane datum (rok 2016 - 2021) (az 1 bodu)
+0.12 funkce get_dataframe ma spravne docstring (PEP257) (az 0.125 bodu)
+0.12 funkce plot_roadtype ma spravne docstring (PEP257) (az 0.125 bodu)
+0.12 funkce plot_animals ma spravne docstring (PEP257) (az 0.125 bodu)
+0.12 funkce plot_conditions ma spravne docstring (PEP257) (az 0.125 bodu)
+0.50 funkce plot_conditions trva do 1500 ms (az 0.5 bodu)
+2.00 kvalita kodu funkce plot_conditions (az 2 bodu)
+2.00 vizualni dojem z grafu plot_conditions (az 2 bodu)
+0.50 funkce plot_animals trva do 1200 ms (az 0.5 bodu)
+2.00 kvalita kodu funkce plot_animals (az 2 bodu)
+2.00 vizualni dojem z grafu plot_animals (az 2 bodu)
+0.50 funkce plot_roadtype trva do 1000 ms (az 0.5 bodu)
+2.00 kvalita kodu funkce plot_roadtype (az 2 bodu)
+2.00 vizualni dojem z grafu plot_roadtype (az 2 bodu)
+2.00 kvalita kodu dle PEP8 (0 kritickych, 0 E2.., 0 E7..)) (az 2 bodu)
```
CELKEM: 19.0 bodu

Komentar k hodnoceni (zejmena k vizualizacim)
================================================================================
pekne

Vystup testu
================================================================================
```
#df_types ints=0;floats=0;cats=62;dt=1
#df_memory=262.12MB
#df_date_year 2016 2021
#get_dataframe_docstring  ok
#plot_roadtype_docstring  ok
#plot_animals_docstring  ok
#plot_conditions_docstring  ok
#plot_roadtype_done 714.76 ms
#plot_animals_done 973.71 ms
#plot_conditions_done 1212.03 ms
```
Hodnoceni treti casti projektu: 
================================================================================
Geograficka data
--------------------------------------------------------------------------------
```
+1.00 spravne CRS (5514, 3857) (az 1 b)
+2.00 spravne rozsah (viz FAQ) (az 2 b)
+2.00 pocet radku 571225 > 10 000 (az 2 b)
+2.00 bez NaN v souradnicich (az 2 b)
+3.00 plot_geo: prehlednost, vzhled (az 3 b)
+2.00 plot_geo: zobrazeni ve WebMercator (a ne v S-JTSK) (az 2 b)
+2.00 plot_cluster: prehlednost, vzhled (az 2 b)
+3.00 plot_cluster: clustering (az 3 b)
+1.00 funkce make_geo ma spravne docstring (PEP257) (az 1 b)
+0.50 funkce plot_geo ma spravne docstring (PEP257) (az 0.5 b)
+0.50 funkce plot_cluster ma spravne docstring (PEP257) (az 0.5 b)
+1.00 kvalita kodu dle PEP8 (0 kritickych, 0 E2.., 0 E7..)) (az 1 b)
```

Overeni hypotezy
--------------------------------------------------------------------------------
```
+1.00 #1: kontingencni tabulka (az 1 b)
+2.00 #1: vypocet chi2 testu (az 2 b)
+0.00 #1: zaver: dochazi k silnemu ovlivneni (az 2 b)
+1.00 #2 filtrace (az 1 b)
+4.00 #2 vypocet a zaver (az 4 b)
```

Vlastni analyza
--------------------------------------------------------------------------------
```
+3.00 tabulka: prehlednost, vzhled (az 5 b)
+4.00 graf: popis, vzhled (az 4 b)
+4.00 graf: vhodna velikost, citelnost (az 4 b)
+0.00 graf: pouziti vektoroveho formatu (az 2 b)
+2.00 textovy popis (az 3 b)
+4.00 statisticka smysluplnost analyzy (az 4 b)
+3.00 dalsi ciselne hodnoty v textu (az 3 b)
+3.00 generovani hodnot skriptem (az 3 b)
+2.00 kvalita kodu dle PEP8 (0 kritickych, 0 E2.., 0 E7..)) (az 2 b)
```
CELKEM: 53.0 bodu

Komentar k hodnoceni (zejmena k vizualizacim)
================================================================================

hypo1: v zaveru zaměněná silnice 1. třídy a dálnice (počty -> na 1. třídě jich je 911)
hypo2: ok
doc: tabulka zarovnani, formátování (jiný font, čísla), obrázek není
moc v textu popsaný

