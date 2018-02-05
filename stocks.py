

import quandl, fbprophet
import pandas as pd, matplotlib.pyplot as plt, numpy as np

quandl.ApiConfig.api_key = "ZL6bU8BmT8BXSAzGLUbQ"
tesla = quandl.get('WIKI/TSLA')




plt.plot(tesla.index, tesla['Adj. Close'], 'r')
plt.title('Tesla Stock Price')
plt.ylabel('Price ($)');
plt.show();

tesla['Year'] = tesla.index.year
tesla.reset_index(level=0, inplace=True)

tesla = tesla.rename(columns={'Date': 'ds', 'Close': 'y'})  #The input to Prophet is always a dataframe with two columns: ds and y. The ds (datestamp) column must contain a date or datetime (either is fine). The y column must be numeric, and represents the measurement we wish to forecast.
tesla_prophet = fbprophet.Prophet(changepoint_prior_scale=0.12) #If the trend changes are being overfit or underfit, you can adjust the strength of the sparse prior using the input argument changepoint_prior_scale.
tesla_prophet.fit(tesla)
forecast = tesla_prophet.make_future_dataframe(periods=365, freq='D')
forecast = tesla_prophet.predict(forecast)
tesla_prophet.plot(forecast, xlabel = 'Date', ylabel = 'Stock prices (USD)')
plt.title('Stock prices of tesla');




from statsmodels.tsa.stattools import adfuller

X = tesla.y.values
result = adfuller(X, autolag='AIC')
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, val in result[4].items():
	print('\t%s: %.3f' % (key, val))
print



from statsmodels.tsa.seasonal import seasonal_decompose

ts_log = np.log(X)

decomposition = seasonal_decompose(ts_log, freq = 365)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(ts_log, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()







google = pd.read_csv('tesla_search_terms.csv',skiprows=2)
google.set_index('Month',inplace=True)
google.index=pd.to_datetime(google.index)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
google.rolling(3).mean().plot(ax=ax)
ii=tesla.rolling(3).y.mean().pct_change().abs()>0.05
crit_ptr = [str(date) for date in tesla[ii].ds]
ax.vlines(crit_ptr, ymin = 0, ymax= 100, colors = 'r', linewidth=0.6, linestyles = 'dashed', label = 'Critical points')

