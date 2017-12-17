from gen_feature import get_feature
from load_data import write_csv_from_list_of_dict
from sklearn import svm
from sklearn.externals import joblib
from load_data import load_training_data
import logging

def get_training_file(f=None):
        f = f or '2014-12-15.csv'
	return f

def _save_model(model, model_name):
	logging.info('start saving model')
        joblib.dump(model, '{0}.m'.format(model_name))
        logging.info('complete saving model')

def _train_model(X, y, model):
	logging.info('start training model')
        model.fit(X,y)
        logging.info('complete training model')


#Multinomial Naive Bayes classifier
def naive_bayes(X, y, *args, **kwargs):
	from sklearn.naive_bayes import MultinomialNB
	alpha = kwargs.get('alpha') or 0.01
	by = MultinomialNB(alpha=alpha)
	_train_model(X, y, by)
        _save_model(by, 'nb1')


def svc(X, y, *args, **kwargs):
	gamma = kwargs.get('gamma') or 0.001
	C = kwargs.get('C') or 100
	clf = svm.SVC(gamma=0.001, C=100)
	_train_model(X, y, clf)
	_save_model(clf, 'svc')


#http://blog.csdn.net/bryan__/article/details/51288953

def get_training_data(file_name=None):
	file_name = file_name or get_training_file()
	df = load_training_data([file_name])[0]
	#print 'complte loading data...'
	#print df
	y = list(df['buy'])
	del df['buy']
	x = df.values.tolist()
	return x, y


def train_model(f='', model='svc', *args, **kwargs):
	f = f or '2014-12-15.csv'
	print 'start loading file..', f
	if not f:
		return None
	x, y = get_training_data(f)
	logging.info('complete loading data...')
	#model_map = {'svc':train_svc}
	naive_bayes(x,y,*args, **kwargs)
	#ret = model_map.get(model)(x, y, *args, **kwargs)
	return x,y

def test_model(file_name='', *args, **kwargs):
	x, y = get_training_data(file_name)
	tp, fp, tn, fn = [0] * 4
	model = joblib.load('svc.m')
	y1 = model.predict(x)
	for idx, val in enumerate(y):

		if val == y1[idx]:
			if val == 'y':
				tp += 1
			else:
				tn += 1
		elif val == 'y':
			fn += 1
		elif val == 'n':
			fp ++ 1
		else:
			print 'invalid result for y:y1',val,y1_val
	logging.info('tp:{0},fp:{1},tn:{2},fn:{3}'.format(tp,fp,tn,fn))

def get_result(f=''):
	f = '2014-12-13.csv'
	x, y = get_training_data(f)
	model = joblib.load('nb.m')
	y1 = model.predict(x)
	ret = []
	for idx, val in enumerate(y1):
		if val == 'y':
			uid, iid = x[idx][0], x[idx][1]
			ret.append({'user_id':uid,'item_id':iid})
	write_csv_from_list_of_dict(ret, ['user_id','item_id'],'tianchi_mobile_recommendation_predict.csv')
	return ret



