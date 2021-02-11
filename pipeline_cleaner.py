import numpy as np
import re
# Locator
def locator(column, iterator):
    for i in iterator:
        if i in column:
            return i.strip().capitalize()


# Outlier Detector
def outlier(df, column):
    q25, q75 = np.percentile(df[column], 25), np.percentile(df[column], 75)
    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off
    outliers = [x for x in df[column] if x < lower or x > upper]
    index = df.loc[df[column].isin(outliers)].index

    return index


# Building Data Cleaning Pipeline
def cleaner(data, location, purchase_type):
    # Converting string to lower case
    data['Property'] = [x.lower() for x in data['Property']]
    data['Location'] = [x.lower() for x in data['Location']]
    data['Description'] = [x.lower() if type(x) != float else x for x in data['Description']]
    data['Features'] = [x.lower() if type(x) != float else x for x in data['Features']]

    # Dropping off Duplicates
    data.drop_duplicates(inplace=True)

    # Getting Numeric values of Bed, Bath, Toilet
    data.loc[:, 'Bath'] = data['Bath'].apply(
        lambda x: re.findall('\d+', str(x))[0].strip() if len(re.findall('\d+', str(x))) != 0 else None)
    data.loc[:, 'Bed'] = data['Bed'].apply(
        lambda x: re.findall('\d+', str(x))[0].strip() if len(re.findall('\d+', str(x))) != 0 else None)
    data.loc[:, 'Toilet'] = data['Toilet'].apply(
        lambda x: re.findall('\d+', str(x))[0].strip() if len(re.findall('\d+', str(x))) != 0 else None)
    data.loc[:, 'Price'] = data['Price'].apply(
        lambda x: float(''.join(re.findall('\d+', str(x)))) if len(re.findall('\d+', str(x))) != 0 else None)

    # Getting bed values from houses property info with 0 bed columns
    if len(data[(data['Bed'] == 0) & (data['Description'].str.contains('bedroom'))]) != 0:
        d1 = data[(data['Bed'] == 0) & (data['Description'].str.contains('bedroom'))]
        mylist = [int(re.findall('\d+', (re.findall('\d+bedroom', x.replace(' ', '')))[0])[0]) if len(
            re.findall('\d+bedroom', x.replace(' ', ''))) > 0 else 0
                  for x in d1['Description']]

        # Assigning values from mylist to d1
        d1.loc[:, 'Bed'] = mylist
        d1.loc[:, 'Bath'] = mylist
        d1.loc[:, 'Toilet'] = [y + 1 if y != 0 else y for y in mylist]

        # Assigning these values to the original Dataframe
        data[(data['Bed'] == 0) & (data['Description'].str.contains('bedroom'))].loc[:, 'Bed'] = d1

    else:
        data = data

    #     List of property type, purchase type and location we wish to locate
    property_type = ['semi detached bungalow', 'semi detached duplex', 'detached bungalow', 'self contain',
                     'mini flat', 'detached duplex', 'terraced bungalow', 'terraced duplex', 'penthouse flat',
                     'massionette house', 'blocks of flats', 'flat / apartment']
    location = location.lower()

    # Finding Property Type and dropping none values in the column
    data['Property Type'] = data['Property'].apply(lambda x: locator(x, property_type))
    data.dropna(subset=['Property Type'], inplace=True)

    # Finding property location and dropping none values in the column
    data['Area'] = location
    #     data.dropna(subset=['Area'], inplace=True)

    # Finding property purchase type and dropping none values in the column
    data['Purchase Type'] = purchase_type

    #     Finding Key Features
    data['Parking Space'] = np.where(
        ((data.Description.str.contains('parking space')) | (data.Features.str.contains('parking space'))), 1, 0)
    data['Security'] = np.where(
        ((data.Description.str.contains('security')) | (data.Features.str.contains('security'))), 1, 0)
    data['Electricity'] = np.where(
        ((data.Description.str.contains('electricity')) | (data.Features.str.contains('electricity'))), 1, 0)
    data['Furnished'] = np.where(
        ((data.Description.str.contains('furnished')) | (data.Features.str.contains('furnished'))), 1, 0)
    data['Security Doors'] = np.where(
        ((data.Description.str.contains('security doors')) | (data.Features.str.contains('security doors'))), 1, 0)
    data['CCTV'] = np.where(((data.Description.str.contains('cctv')) | (data.Features.str.contains('cctv'))), 1, 0)

    # Dropping lands, office and commercial properties
    data.drop(data[(data['Property'].str.contains('land')) | (data['Property'].str.contains('office')) | (
        data['Property'].str.contains('commercial'))].index, inplace=True)

    # Dropping rows with price less than 150000
    data.drop(data[data.Price < 150000].index, inplace=True)

    # Dropping rows with price as None
    data.drop(data[data['Price'].isna()].index, inplace=True)

    # Dropping price outiers
    odd_price = outlier(data, 'Price')
    data.drop(odd_price, inplace=True)

    #     Location is dependent on where you choose to save.
    data.to_csv(fr'C:\Users\HP\Desktop\Data Jedi\new\data_cleaned/{location}_{purchase_type}_clean.csv')