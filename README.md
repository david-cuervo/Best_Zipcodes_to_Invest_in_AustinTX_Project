# Module 4 Final Project 
By David Cuervo

## Background
Select the 5 best zipcodes in Austin to invest in.



## Contents of Repository

- Time folder containing original Zillow data
- Notebook containing the code used for preprocessing and modeling
- PDF of presentation

## Approach

- Used data from Zillow from 1996 to 2018
- Filtered the data for zipcodes in Austin, TX
- Changed the format of the date time data
- Reshaped the data from wide to long
- Used a function that would select the best parameters for the ARIMA model based on the mean squared errors
- Visualized the forecast of housing sale values for the next 3 years 
- Calculated the predicted return on investment
- Repeated for all 38 zipcodes in Austin
- Selected the top 5

## Conclusions

- Top 5 zipcodes with highest expected return on investment: 78751, 78758, 78722, 78702, 78741
- Any zipcode in Austin is increasing in value
