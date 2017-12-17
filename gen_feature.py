from pre_procession_data import DataProcessing
from load_data import write_csv_from_list_of_dict
import gc

def _buy_total_rate(*args, **kwargs):
	fourth_behavior = kwargs.get('fourth') or 0.0
	total_behavior = kwargs.get('total') or 1.0
	return float(fourth_behavior)/total_behavior

def _buy_cart_rate(*args, **kwargs):
	fourth_behavior = kwargs.get('fourth') or 0.0
	third_behavior = kwargs.get('third') or 1.0
	return 	fourth_behavior/third_behavior

def _total_behavior(*args, **kwargs):
	total_behavior = kwargs.get('total') or 0.0
	return total_behavior

def _total_buy(*args, **kwargs):
	fourth_behavior = kwargs.get('fourth') or 0.0
	return fourth_behavior


def init(df=None, test_date=''):
	#df = df.groupby(['user_id','item_id']).sum()
	#df = df.reset_index()
	ll = df.values.tolist()
	del df
	gc.collect()
	ret = {}
	tag_lst = []
	cnt, cnt1, cnt2 = 0, 0, 0
	print 'test date is', test_date
	for item in ll:
		cnt += 1
		k = '{0}_{1}'.format(item[0], item[1])
		curr_dict = ret.get(k)
		ts, bt = item[5], item[2]
		if test_date in ts:
			cnt1 += 1
			if bt == 4:
				cnt2 += 1
				tag_lst.append(k)
			continue

		if curr_dict:
			data = curr_dict.get('data')
			if data:
				data.append(item[2:])
			else:
				curr_dict.update({'data':[item[3:]]})
		else:
			ret.update({k:{'data':[item[2:]]}})

	del ll
	gc.collect()
	print cnt, len(ret.keys()), cnt1, cnt2
	return ret,tag_lst

def _get_user_feature(user_sum={}):
    if not user_sum:
        return {}
    ret = {}
    for k, v in user_sum.iteritems():
        tmp = {}
        total = sum(v) if isinstance(v, list) else 1.0
        if v[4] == 0:
            buy_total_rate, buy_cart_rate, buy_keep_rate ,buy_review_rate = [0.0]*4
        else:
            buy_total_rate = total/v[4]
            buy_cart_rate = v[3]/v[4]
            buy_keep_rate = v[2]/v[4]
            buy_review_rate = v[1]/v[4]
        tmp.update({'utotal_behavior':total,
                    'ubuy_behavior':v[4],
                    'ubuy_total_rate':buy_total_rate,
                    'ubuy_cart_rate':buy_cart_rate,
                    'ubuy_keep_rate':buy_keep_rate,
                    'ubuy_review_rate':buy_review_rate})


        ret.update({k:tmp})

    return ret
 def _get_item_feature(item_sum={}):
     if not item_sum:
         return {}
     ret = {}
     for k, v in item_sum.iteritems():
         total = sum(v) if isinstance(v, list) else 1.0
         tmp = {}
         if v[4] == 0:
             buy_total_rate,buy_cart_rate,buy_keep_rate,buy_review_rate  = [0.0]*4
         else:
             buy_total_rate = total/v[4]
             buy_cart_rate = v[3]/v[4]
             buy_keep_rate = v[2]/v[4]
             buy_review_rate = v[1]/v[4]
         tmp.update({'itotal_behavior':total,
                     'ibuy_behavior':v[4],
                     'ibuy_total_rate':buy_total_rate,
                     'ibuy_cart_rate':buy_cart_rate,
                     'ibuy_keep_rate':buy_keep_rate,
                     'ibuy_review_rate':buy_review_rate})
         ret.update({k:tmp})
     return ret
 
 feature_map = {
         'total_behavior':_total_behavior,
         'buy_behavior':_total_buy,
         'buy_total_rate':_buy_total_rate,
         'buy_cart_rate':_buy_cart_rate
 }


feature_map = {
	'total_behavior':_total_behavior,
	'buy_behavior':_total_buy,
	'buy_total_rate':_buy_total_rate,
	'buy_cart_rate':_buy_cart_rate
}


def get_feature(ui_features=[],*args, **kwargs):
	ui_features = ui_features or ['total_behavior','buy_behavior','buy_total_rate','buy_cart_rate']
	dp = DataProcessing('user.csv')
	#date range is not handled correctly, to be checked
	start_date = kwargs.get('start_date') or '2014-12-15'
	end_date = kwargs.get('end_date') or '2014-12-19'
	df = dp.filter_by_period(start_date=start_date, end_date=end_date)
	del dp.df
	gc.collect()
	#ret_dict:{'user_id_item_id':[behavior_type, user_geohash, item_category,time]}
	ret_dict, tag_lst = init(df, '2014-12-18')
	ret_feature = []
        user_sum = {}
        item_sum = {}
	for k, v in ret_dict.iteritems():
		data = v.get('data') or []
		total_behavior = len(data)
		behavior_sum = [0]*5
                user_id, item_id = k.split('_')
		for d in data:
			try:
				b = d[0]
				behavior_sum[b] +=1
                                if user_id not in user_sum:
                                    user_sum.update({user_id:[0]*5})
                                tmp = user_sum.get(user_id)
                                tmp[b] += 1
                                if item_id not in item_sum:
                                    item_sum.update({item_id:[0]*5})
                                tmp = item_sum.get(item_id)
                                tmp[b] += 1

                        except Exception,ex:
				print 'behavior missing for', k
		bhb_dict = dict(zip(['first','second','third','fourth'], behavior_sum[1:]))
		bhb_dict.update({'total':total_behavior})
		v.update(bhb_dict)
                #v.update({'user_sum':user_sum,'item_sum':item_sum})


		tag = 'y' if k in tag_lst else 'n'
		feature_dict = {'user_id':user_id, 'item_id':item_id,'buy':tag}
		for f in ui_features:
			feature_val = feature_map.get(f)(**v)
			feature_dict.update({f:feature_val})
		ret_feature.append(feature_dict)
        user_feature = _get_user_feature(user_sum)
        item_feature = _get_item_feature(item_sum)
        for item in ret_feature:
            tmp = user_feature.get(item.get('user_id'))
            item.update(tmp)

	keys = ['user_id','item_id','buy'] + ui_features+['utotal_behavior','ubuy_behavior','ubuy_total_rate','ubuy_cart_rate','ubuy_keep_rate','ubuy_review_rate']+['itotal_behavior','ibuy_behavior','ibuy_total_rate','ibuy_cart_rate','ibuy_keep_rate','ibuy_review_rate']

	write_csv_from_list_of_dict(ret_feature, keys, '{0}.csv'.format(start_date))
	return user_feature



#ret =  get_feature()
#k= ret.keys()
#print k, ret[k[0]]

