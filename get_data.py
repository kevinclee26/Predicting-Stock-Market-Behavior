# Download financial data from free online databases

import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt

# DEFINE DATE RANGE
start_date='1900-01-01'
end_date='2019-06-20'

# GET COMPLETE LIST OF SYMBOLS
# nasdaq_listed=pd.read_csv('nasdaqlisted.txt', sep='|')
# USE THIS
# nasdaq_traded=pd.read_csv('nasdaqtraded.txt', sep='|')
# other_listed=pd.read_csv('otherlisted.txt', sep='|')
# USE THIS
# nasdaq_symbol_list=list(nasdaq_traded['NASDAQ Symbol'])
# print(len(nasdaq_symbol_list))
# print(len(list(set(nasdaq_symbol_list))))
# print(other_listed['Exchange'].value_counts())
# print(nasdaq_traded['Nasdaq Traded'].value_counts())
# print(nasdaq_listed.shape)
# USE THIS
# tickers=nasdaq_symbol_list
# tickers=['AAPL', 'MSFT', '^GSPC']

nasdaq=pd.read_csv('NASDAQ_list.csv')
nyse=pd.read_csv('NYSE_list.csv')

tickers=nasdaq[nasdaq['MarketCap_Dollars']>5000000000]['Symbol'].tolist()+nyse[nyse['MarketCap_Dollars']>5000000000]['Symbol'].tolist()
tickers=list(set(tickers))

all_weekdays=pd.date_range(start=start_date, end=end_date, freq='B') 
all_volume_data=pd.DataFrame(index=all_weekdays)
all_high_data=pd.DataFrame(index=all_weekdays)
all_low_data=pd.DataFrame(index=all_weekdays)
all_close_data=pd.DataFrame(index=all_weekdays)
# all_close=all_close.reindex(all_weekdays)
count=0
issues=0
issues_list=[]

for each_ticker in tickers[count: ]: 
	try: 
		panel_data=data.DataReader(each_ticker, 'yahoo', start_date, end_date)
		# panel_data=data.DataReader('INPX', 'yahoo', start_date, end_date)
		volume_data=panel_data['Volume']
		all_volume_data[str(each_ticker)]=volume_data
		high_data=panel_data['High']
		all_high_data[str(each_ticker)]=high_data
		low_data=panel_data['Low']
		all_low_data[str(each_ticker)]=low_data
		close_data=panel_data['Close']
		all_close_data[str(each_ticker)]=close_data
	except:
		issues_list.append(each_ticker)
		issues+=1
		print('{} issues found'.format(issues))
		pass
	# print(panel_data.columns)

	count+=1
	print('{} - {} out of {} - {}%'.format(each_ticker, count, len(tickers), round(count/len(tickers),2 )))

	# if count%500==0:
	# 	file_text='{}_tickers_complete.csv'.format(count)
	# 	sheet_data.to_csv(file_text)
	# 	sheet_data=pd.DataFrame(index=all_weekdays)
	# 	print(issues_list)
volume_data.to_csv('all_{}_tickers_complete_volume.csv'.format(count))
high_data.to_csv('all_{}_tickers_complete_high.csv'.format(count))
low_data.to_csv('all_{}_tickers_complete_low.csv'.format(count))
close_data.to_csv('all_{}_tickers_complete_close.csv'.format(count))
