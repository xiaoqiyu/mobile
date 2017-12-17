from load_data import load_training_data

class DataProcessing:
	def __init__(self, file_name=None):
		files = [file_name] if file_name else ['item.csv']
		self.df = load_training_data(files)[0]
		self.columns = self.df.columns
		#self.indexes = self.df.indexes
	

	def filter_df(self, filter_condition={}):
		if not select_condition:
			return None
		#for k, v in filter_condition.iteritems():
		
	
	def filter_by_date(self, date=''):
		if not date:
			return None
		y, m, d = [int(x) for x in date.split('-')]
		time_start = '{0}-{1}-{2} 00'.format(y, m, d)
		time_end = '{0}-{1}-{2} 24'.format(y, m, d)
		df = self.df[(self.df.time >= time_start) & (self.df.time <= time_end)]
		return df

	def filter_by_period(self, start_date ='', end_date=''):
		if not start_date and not end_date:
			return None
		if not start_date:
			return self.filter_by_date(end_date)
		if not end_date:
			return self.filter_by_date(start_date)
		y, m, d = [int(x) for x in start_date.split('-')]
                time_start = '{0}-{1}-{2} 00'.format(y, m, d)
                
                y, m, d = [int(x) for x in end_date.split('-')]
                time_end = '{0}-{1}-{2} 00'.format(y, m, d)
               
		df = self.df[(self.df.time >= time_start) & (self.df.time <= time_end)]
		return df
		

#dp = DataProcessing('user.csv')
#print dp.df.columns
#print dp.filter_by_period(start_date='2014-12-13', end_date='2017-12-18')
#print dp.df
