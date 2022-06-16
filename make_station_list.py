#!/usr/bin/env python3

# MIT License

# Copyright (c) 2022 DeflateAwning

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import dbfread # install with `python3 -m pip install dbfread`
import shapefile # install with `python3 -m pip install pyshp`
import pandas as pd # install with `python3 -m pip install pandas`

import glob
from typing import List


def read_dbfs() -> pd.DataFrame:
	df_list: List[pd.DataFrame] = []
	for filename in glob.glob('./data_shp/*STATION*.dbf'):
		data_list: List[dict] = dbfread.DBF(filename, load=True) # load=True allows for random access by loading entire file to memory
		this_data_df: pd.DataFrame = pd.DataFrame(data_list)

		df_list.append(this_data_df)

	df = pd.concat(df_list)

	print(f"Reading DBFs done. Found/combined {len(df_list)} files. Total rows: {len(df)}.")
	#df.to_csv('station_list_dbfs.csv', index=False)
	return df

def read_shps() -> pd.DataFrame:
	df_list: List[pd.DataFrame] = []
	for filename in glob.glob('./data_shp/*STATION*.shp'):
		shpfile = shapefile.Reader(filename, encoding = "ISO8859-1") # weird encoding; whatever though
		
		this_data_df: pd.DataFrame = pd.DataFrame({
			'NID': [i.record[0] for i in shpfile.shapeRecords()],
			'Latitude': [i.shape.__geo_interface__['coordinates'][1] for i in shpfile.shapeRecords()],
			'Longitude': [i.shape.__geo_interface__['coordinates'][0] for i in shpfile.shapeRecords()],
			'ShapeType': [i.shape.__geo_interface__['type'] for i in shpfile.shapeRecords()]
		})

		df_list.append(this_data_df)

	df = pd.concat(df_list)

	print(f"Reading SHPs done. Found/combined {len(df_list)} files. Total rows: {len(df)}.")

	if len(set(df['ShapeType'].to_list())) != 1:
		print(f"Warning! More than 1 ShapeType was found in the Shapefiles. All ShapeTypes found: {set(df['ShapeType'].to_list())}.")

	#df.to_csv('station_list_shps.csv', index=False)
	return df

def do_it():
	df_dbf = read_dbfs()
	df_shp = read_shps()

	df = df_dbf.merge(df_shp, how='outer', on='NID', validate='one_to_one')
	
	print(f"Merging done. Total rows: {len(df)}.")
	df.to_csv('station_list.csv', index=False)

if __name__ == '__main__':
	do_it()
