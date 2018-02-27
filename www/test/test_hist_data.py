import tushare as ts

#df = ts.get_hist_data('600848', start='2015-01-05', end='2015-01-09')
print ts.get_hist_data('600848', start='2016-11-01', end='2016-11-03')

#df = ts.get_today_all()
#print df
#print df.to_json('today_all.json', orient='values')

