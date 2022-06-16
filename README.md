# canada-train-station-list
A quick and dirty aggregation of all ~2500 heavy-rail train stations in Canada

## Purpose
In 2022-06, https://railway-stations.org didn't support Canadian train stations. To fix this problem, I scraped together all Canadian train stations to be imported into their system. This repo aims to capture the quick data transformation procedure/Python script.

The data source used is: https://ftp.maps.canada.ca/pub/nrcan_rncan/vector/geobase_nrwn_rfn/

## Procedure
The procedure involves downloading and unzipping a bunch of files. Then, a Python script combines those files into a single CSV.

1. Download the complete data source for all provinces by running the following bash commands.
```bash
mkdir data_download/
cd data_download/
wget -np -r -e robots=off https://ftp.maps.canada.ca/pub/nrcan_rncan/vector/geobase_nrwn_rfn/
cd ..
```

2. Copy all data applicable shapefile zips to a folder, and then unzip them.
```bash
mkdir data_shp/
cp data_download/**/*shp*en*.zip data_shp/
```

3. Unzip each shapefile.
```bash
cd data_shp/
unzip "*.zip"
cd ..
```

4. Run the Python script.
```bash
python3 -m pip install -r requirements.txt
python3 make_station_list.py
```

5. See the generated `station_list.csv`. Note that this UTF-8 CSV file, generated on 2022-06-15, is also included in this repo for your convenience.
