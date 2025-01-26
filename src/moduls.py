#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import logging

class Loader:
    def __init__(self, data_file, cols=None, log_level=logging.INFO):
        """
        Initializes the Loader class.
        :param data_file: The name of the data file to be loaded.
        :param cols: Optional list of columns to load from the file.
        :param log_level: Logging level (default: logging.INFO).
        """
        self.data_file = data_file
        self.cols = cols
        self.df = None

        # Logging setup
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level = log_level,
            format = '%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger.info(f"Loader initialized for file: {data_file}")

    def AddAGE_CAT(self):
        """
        Adds a new "AGE_CAT" column to the dataframe to categorize age groups.
        """
        try:
            self.logger.info("Adding AGE_CAT column based on AGE.")
            label_ = ['00-04', '05-09', '10-14', '15-19', '20-24', '25-29', '30-34', 
                      '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', 
                      '65-69', '70-74', '75-79', '80+']
            self.df["AGE_CAT"] = pd.cut(
                x=self.df["AGE"],
                bins=[-1, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 200],
                labels=label_
            )
            self.logger.info("AGE_CAT column successfully added.")
        except KeyError as e:
            self.logger.error(f"AGE column is missing: {e}")
            raise

    def load(self):
        """
        Load and preprocess the dataset. Includes adding age categories and merging additional geographic data.
        """
        try:
            self.logger.info("Loading main dataset.")
            self.df = pd.read_csv(f'input/{self.data_file}', dtype={'KSHIR': 'str','NEM' : 'str'})[['PID', 'AGE', 'NEM', 'KSHIR', 'HT_TYPE']]
            self.logger.info(f"Dataset loaded: {self.data_file}")

            # HT_TYPE rövidítése
           
            self.df['HT_TYPE'] = self.df['HT_TYPE'].str[:4]

            # Korosztályok hozzáadása
            self.AddAGE_CAT()

            # Települési adatok betöltése
            
            telep = pd.read_csv('geolista3.csv', dtype={'KSHIR': 'str'})
            t2 = pd.read_csv('jaras2.csv', dtype={'KOD': 'str'})
            

            # Összefésülés
            
            telep = pd.merge(telep, t2, how = 'left', left_on = 'Járás', right_on = 'JARAS')
            self.df = pd.merge(
                self.df,
                telep[['KSHIR', 'JOG']],
                how = 'left',
                on = 'KSHIR'
            )[['PID', 'NEM', 'AGE_CAT', 'JOG', 'HT_TYPE']]
            

        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"KeyError: Missing expected columns in the dataset: {e}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

        return self.df
    
class Simulation:
    def __init__(self, df1, df2, _id, _dim, _attr, log_level = logging.INFO):
        """
        Initializes the Simulation class.
        
        :param df1: DataFrame for the earlier time period.
        :param df2: DataFrame for the actual time period.
        :param _id: Column name representing unique identifiers.
        :param _dim: List of column names for additional dimensions.
        :param _attr: Column name representing the attribute to track transitions.
        :param log_level: Logging level (default: logging.INFO).
        
        """
        self.early_df = df1
        self.later_df = df2
        self.id = _id
        self.dim = _dim
        self.attr = _attr

        # Set up logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level = log_level,
            format = '%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger.info("Simulation class initialized.")

    def preprocess(self, show_d = True):
        """
        Preprocesses the data by merging the early and later dataframes.
        Handles additional dimensions if provided.
        
        :param show_d: Whether to display the processing duration.
        
        :return: Merged DataFrame with '_old' and '_new' suffixes for attribute columns.
        """
        
        start = datetime.now()
        self.logger.info("Starting data preprocessing...")

        # Sort and set index by the ID and dimensions
        self.logger.debug("Sorting and indexing early and later DataFrames.")
        self.v_early = self.early_df.sort_values(self.id).set_index(self.id)
        self.v_later = self.later_df.sort_values(self.id).set_index(self.id)

        # Merge the dataframes on the ID and dimensions
        self.logger.debug("Merging DataFrames.")
        v_merged = pd.merge(
            self.v_early,
            self.v_later,
            how = 'outer',
            left_index = True,
            right_index = True,
            suffixes = ['_old', '_new']
        )

        # Handle missing values
        self.logger.debug("Filling missing values with default state 'HHHH'.")
        v_merged[f'{self.attr}_old'] = v_merged[f'{self.attr}_old'].fillna('HHHH')
        v_merged[f'{self.attr}_new'] = v_merged[f'{self.attr}_new'].fillna('HHHH')

        # Reset index for easier use
        v_merged.reset_index(inplace = True)
        v_merged = v_merged.rename(columns = {'index': self.id})

        if show_d:
            duration = datetime.now() - start
            self.logger.info(f"Preprocessing completed in {duration}.")
       
        v_merged['NEM_old'] = v_merged['NEM_old'].fillna(v_merged['NEM_new'])
        v_merged['AGE_CAT_old'] = v_merged['AGE_CAT_old'].fillna(v_merged['AGE_CAT_new'])
        v_merged['JOG_old'] = v_merged['JOG_old'].fillna(v_merged['JOG_new'])
        self.v_merged = v_merged
        return v_merged

    def get_transition_matrix(self, v_merged, percent=True, pivot_table=True):
        """
        Calculates the transition matrix with optional percentage and pivot table creation.
        
        :param v_merged: Merged DataFrame after preprocessing.
        :param percent: Whether to normalize values as percentages (default: True).
        :param pivot_table: Whether to use pivot_table or pivot for creating the matrix (default: True).
        
        :return: Transition matrix as a DataFrame.
        """
        self.logger.info("Calculating transition matrix.")
        
        # Define old dimensions and group list
        left_dim = [f'{x}_old' for x in self.dim]
        grouplist = [f'{self.attr}_old', f'{self.attr}_new'] + left_dim
        

        # Group by the specified dimensions and count occurrences
        self.logger.debug("Grouping data for transition matrix calculation.")
        v_grouped = v_merged.groupby(grouplist)['PID'].count().reset_index()

        # Debug information for grouped data
        self.logger.debug("Grouped DataFrame preview:")
        self.logger.debug(v_grouped.head())

        # Define the pivot table index
        grouplist2 = [f'{self.attr}_old'] + left_dim
        self.logger.debug(f"Group List2: {grouplist}")
        

        # Create pivot table or pivot
        if pivot_table:
            self.logger.debug("Creating pivot table.")
            out_pivot = v_grouped.pivot_table(index = grouplist2, columns = f'{self.attr}_new', values = 'PID', aggfunc = 'sum')
        else:
            self.logger.debug("Creating pivot using `pivot` method.")
            out_pivot = v_grouped.pivot(index = grouplist2, columns = f'{self.attr}_new', values = 'PID')

        # Add TOTAL column for row-wise sums
        self.logger.debug("Calculating total row sums.")
        out_pivot['TOTAL'] = out_pivot.sum(axis = 1)

        # Calculate percentages if required
        if percent:
            self.logger.debug("Calculating percentages for transition probabilities.")
            col_list = out_pivot.columns[:-1]  # Exclude 'TOTAL'
            
            for col in col_list:
                out_pivot[col] = out_pivot[col] / out_pivot['TOTAL']
            out_pivot.reset_index(inplace = True)
        
        # Add additional transition probability calculation
        self.logger.debug("Generating transition probabilities DataFrame.")
        trans_prob = pd.melt(out_pivot, id_vars = grouplist2, var_name = f'{self.attr}_new', value_name = 'Probability')
        self.logger.debug("Melted DataFrame preview:")
        self.logger.debug(trans_prob.head())
        self.tp1 = trans_prob
        people_count = self.v_merged.groupby(grouplist)['PID'].count().reset_index()
        self.logger.debug("Grouplist preview:")
        self.logger.debug(grouplist)
        self.logger.debug("People Count DataFrame preview:")
        self.logger.debug(people_count.head())
        
        self.pc1 = people_count
        
        trans_prob = pd.merge(trans_prob, people_count, how = 'left', on = grouplist)
        self.logger.debug("Transprob DataFrame preview:")
        self.logger.debug(trans_prob.head())

        self.logger.info("Transition matrix calculation completed.")
        return out_pivot, trans_prob

