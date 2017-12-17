import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import logging
import csv
from sklearn import svm


DEFAULT = 0.0
DATA_HOME = '/home/kiki/program/data/'
APP_PATH = 'mobile/'
def load_training_data(file_names=[]):
	paths = map(lambda x:DATA_HOME+APP_PATH+x, file_names)
	if not paths:
		return []
	ret = []
	for p in paths:
		data_df = pd.read_csv(p)
		ret.append(data_df)
	return ret

def write_csv_from_list_of_dict(data_lst, keys, file_name):
	path = DATA_HOME+APP_PATH+file_name
	with open(path, 'wb') as f:
		dict_writer = csv.DictWriter(f, keys)
		dict_writer.writeheader()
		dict_writer.writerows(data_lst)

#print load_training_data(['tianchi_fresh_comp_train_item.csv'])[0]

















































































