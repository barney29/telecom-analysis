"""
The module focus on wrapping the pandas dataframe to work for telecom dataset
"""
import pandas as pd
import sys
sys.path.append('../src/')

from utils import find_outliers, ms_to_s
from dbconn import DbDriver


class DataFrameWrapper:
    """
    A class used to wrap and clean the necessary data
    """

    def __init__(self, df=None):
        # if dataframe is given
        if df is not None:
            self.df = df
        else:
            driver = DbDriver()
            self.df = driver.query_excute("SELECT * FROM public.xdr_data")
            # close connection
            driver.close_connection()

    def clean_data(self):
        """
        To clean the data: missing value and outliers
        """
        # Replacing missing value with mean
        print(f"################Replacing missing value with mean################")
        for column in self.df.columns:
            if self.df[column].dtype in ['int64', 'float64']:
                print(f"Column: {column} : Mean: {self.df[column].mean()}")
                self.df[column].fillna(self.df[column].mean(), inplace=True)
            else:
                print(f"Column: {column} : Mode: {self.df[column].mode()[0]}")
                most_frequent = self.df[column].mode()[0]
                self.df[column].fillna(most_frequent, inplace=True)

        # Replacing outliers with mean
        print(f"\n\n=========== Replacing outlier with mean ====================")
        for column in self.df.columns:
            if self.df[column].dtype in ['int64', 'float64']:
                outliers = find_outliers(self.df[column])
                if outliers.any():
                    print(f'Outliers detected in column {column}')

                mean_value = self.df[column].mean()
                self.df.loc[outliers, column] = mean_value

    # describe data
    def describe(self):
        return self.df.describe()

    def info(self):
        return self.df.info()

    # Basic user overview

    def top_handset(self, num=10):
        return self.df['Handset Type'].value_counts().head(num)

    # top 3 handset manufacturer

    def top_handset_manufacturer(self, num=3):
        return self.df['Handset Manufacturer'].value_counts().head(num)

    # top handset type based on top specified number manufacturer
    def top_handset_type_per_top_manufacturer(self, handset=5, man=3):
        top_manufacturer = self.top_handset_manufacturer(man)
        # converting series to dataframe
        manufacturers = pd.DataFrame(top_manufacturer)

        # Filter based on the top manufacturers
        filtered_df = self.df[self.df['Handset Manufacturer'].isin(manufacturers.index)]

        # Get the top handset types
        top_handset_types = filtered_df['Handset Type'].value_counts().head(handset)

        return top_handset_types
    
    def ms_to_s(self):
        self.df['Dur. (ms)'].apply(ms_to_s)
    def get_df(self):
        return self.df
