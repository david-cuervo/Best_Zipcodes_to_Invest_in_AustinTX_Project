def melt_zip(zipcode):
    
    '''
    Takes a zip code from Zillow dataset
    
    Returns a dataframe of the zip code's housing sale values and month in a long format
    '''
    
    df_atx_zip = melt_data(df_atx[df_atx['RegionName'] == zipcode])
    return df_atx_zip

def evaluate_arima_model(X, arima_order):
    '''
    Takes a dataframe and order of ARIMA parameters: p, d, q
    
    Returns the mean squared error for the ARIMA model
    '''
    # prepare training dataset
    train_size = int(len(X) * 0.66)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]
    # make predictions
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # calculate out of sample error
    error = mean_squared_error(test, predictions)
    return error

def evaluate_models(dataset, p_values, d_values, q_values):
    '''
    Takes a dataset and an array of ARIMA parameter values
    
    Returns the order of parameters that has the least mean squared error
    as well as the mean squared error
    '''
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p,d,q)
                try:
                    mse = evaluate_arima_model(dataset, order)
                    if mse < best_score:
                        best_score, best_cfg = mse, order
                    print('ARIMA%s MSE=%.3f' % (order,mse))
                except:
                    continue
    print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))

def interpret_model(zipcode, p, d, q):
    
    '''
    Takes a zip code from housing sales dataset and the parameters for an ARIMA model
    
    Returns a plot of the housing sales vs time and the projected sale values and confidence interval
    Prints a line stating the predicted percent return on the investment in that zip code
    '''

    # make forecast 
    model = ARIMA(melt_zip(zipcode), order=(p,d,q))
    model_fit = model.fit(disp=0)

    forecast = model_fit.forecast(36)

    actual_foreacst = forecast[0]
    forecast_conf_int = forecast[2]

    # make dataframe with forecast and 95% confidence interval 
    df_forecast = pd.DataFrame({'time': pd.date_range(start = '2018-05-01', end = '2021-04-01', freq = 'MS')})
    df_forecast['forecast'] = actual_foreacst
    df_forecast['lower_bound'] = forecast_conf_int[:, 0]
    df_forecast['upper_bound'] = forecast_conf_int[:, 1]
    df_forecast.set_index('time', inplace = True)

    # combine raw data dataframe and forecast dataframe
    df_new = pd.concat([melt_zip(zipcode), df_forecast])


    fig = plt.figure(figsize = (12, 8))

    plt.plot(df_new['value'], label = 'raw data')
    plt.plot(df_new['forecast'], label = 'forecast')
    plt.fill_between(df_new.index, df_new['lower_bound'], df_new['upper_bound'], color="k", alpha=.15,
                label = 'confidence interval')
    plt.legend(loc = 'upper left')
    plt.title('Forecast for %s' % zipcode)
    
    # forecasted price after 3 years
    forcast_3_years = df_new.loc['2021-04-01', 'forecast']
    forcast_lower = df_new.loc['2021-04-01', 'lower_bound']
    forcast_upper = df_new.loc['2021-04-01', 'upper_bound']
    
    last_price = melt_zip(zipcode).loc['2018-04-01', 'value']
    
    predicted_percent_change = (forcast_3_years - last_price) / last_price
    print(f' I would expect a {np.round(predicted_percent_change * 100, 4)}% return on my investment in {zipcode}')
