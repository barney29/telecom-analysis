"""
This module focus on wrapping a column it extends from the dataframe wrapper class
the purpose is to focus and specific analysis based on the requirement
"""
import pandas as pd
import sys

sys.path.append('../src/')

from dataframewrapper import DataFrameWrapper


class ColumnWrapper(DataFrameWrapper):
    """
    Specialized columns and basic statistics
    """

    def __init__(self, columns, df=None):
        """
        @columns: required to filter the columns
        """
        if df is not None:
            print(f"DataFrame is given it is to be assumed clean dataframe\nif not try clean_data method")
            self.df = df
            self.flt_data = [col for col in columns if col in self.df.columns]
        else:
            # df is not given calling the parent
            super().__init__()  # Call the parent constructor
            # cleaning the data
            self.clean_data()

            # filter the data
            # self.flt_data = self.df.loc[:, self.df.columns.isin(columns)]
            self.flt_data = [col for col in columns if col in self.df.columns]
    
    def get_flt_data(self):
        return self.flt_data
