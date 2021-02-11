import numpy as np
import pandas as pd
import re
# Importing Neccessary Libraries
from feature_engine.encoding import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os
import streamlit as st
from PIL import Image

pd.set_option('display.max_colwidth', None)

# path = os.getcwd()
# # Importing data
sale = pd.read_csv('cleaned_sale.csv')
rent = pd.read_csv('cleaned_rent.csv')
# Getting Image
logo = Image.open('Logo.jpg')

# Setting Title of App
st.title('Lagos state House Predictor')
st.subheader('An application to give you a rough estimate of price of houses in Lagos.')
# Setting Logo Image
st.image(logo, use_column_width=True)

# Word Converter
def word_convert(word):
    word_dict = {'yes': 1, 'no': 0}
    return word_dict[word.lower()]


def case_lower(word):
    return word.lower()


# Getting input data

purchase_type = case_lower(st.radio('What is your purchase type', ('Rent', 'Sale')))
# Condition to select dataset
if purchase_type == 'rent':
    data = rent
else:
    data = sale
# Option to view your data
check_data = st.checkbox('View Sample Data')
if check_data:
    st.write(data.head(3))
st.write('Now lets find out price estimate.')
property_type = st.selectbox('What is your purchase type', ('Mini flat', 'Terraced duplex', 'Detached bungalow',
                                                            'Blocks of flats', 'Semi detached duplex',
                                                            'Flat / apartment',
                                                            'Detached duplex', 'Massionette house',
                                                            'Semi detached bungalow',
                                                            'Self contain', 'Terraced bungalow', 'Penthouse flat'))
location = case_lower(st.selectbox('Where do you wish to stay ?',
                                   ('Ajah', 'Gbagada', 'Ikeja', 'Lekki', 'Ikoyi', 'Surulere', 'Ikorodu', 'Yaba')))
bedrooms = st.slider('Number of Bedrooms', int(data['Bed'].min()), int(data['Bed'].max()))
bathrooms = st.slider('Number of Bathrooms', 1, int(data['Bath'].max()))
toilets = st.slider('Number of Toilets', 1, int(data['Toilet'].max()))
parking_space = word_convert(st.selectbox('Do you need parking space ?', ('Yes', 'No')))
electricity = word_convert(st.selectbox('Do you need 24hrs Electricity ?', ('Yes', 'No')))
security = word_convert(st.selectbox('Do you need security guards ?', ('Yes', 'No')))
furnished = word_convert(st.selectbox('Do you want the house to be furnished ?', ('Yes', 'No')))
security_doors = word_convert(st.selectbox('Do you want security doors ?', ('Yes', 'No')))
cctv = word_convert(st.selectbox('Do you want CCTV surveillance ?', ('Yes', 'No')))
bq = word_convert(st.selectbox('Do you want Boys Quarters ?', ('Yes', 'No')))
gym = word_convert(st.selectbox('Do you need gym facilities ?', ('Yes', 'No')))
pool = word_convert(st.selectbox('Do you need swimming pool ?', ('Yes', 'No')))

# Modeling step

# Encoding Step
encode = OneHotEncoder()
target = data['Price']
features = data.drop('Price', 1)
encode.fit(features)
features = encode.transform(features)

# Getting the target and features variables

# print(data.head())

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=0)
# Creating the algorithm class
model = RandomForestRegressor()
# Creating algorithm object
model.fit(X_train, y_train)
# Predicted values
estimate = pd.DataFrame(
    {'Bed': bedrooms, 'Bath': bathrooms, 'Toilet': toilets, 'Property Type': property_type,
     'Area': location, 'Purchase Type': purchase_type, 'Parking Space': parking_space, 'Security': security,
     'Electricity': electricity,
     'Furnished': furnished, 'Security Doors': security_doors, 'CCTV': cctv, 'BQ': bq, 'Gym': gym, 'Pool': pool}, index=[0])
# estimate = [[bedrooms, bathrooms, toilets, built, property_type,
#              location, purchase_type, parking_space, security, electricity,
#              furnished, security_doors, cctv, bq, gym, pool]]
estimate = encode.transform(estimate)
predict = model.predict(estimate)[0].round()

# Checking Prediction

if st.button('Check Price Estimate'):
    st.header(f'The estimated price of house is ₦ {predict:,}')
