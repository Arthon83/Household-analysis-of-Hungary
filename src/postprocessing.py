#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Postprocess of pivot and data files to prepare for Power BI
import pandas as pd
import numpy as np


# In[11]:


output_name_pivot = 'data_pivotxx.csv'
output_name_data = 'res3xx.csv'


# In[40]:


# Set Columns list
col_list = ['HT_TYPE_old', 'AGE_CAT_old', 'NEM_old', 'JOG_old', 'HT_TYPE_new']
col_list_ext = col_list + ['PID']


# In[41]:


# Set csv-s
csv_files = ['2022_pivot.csv','2023_pivot.csv','2024_pivot.csv']

# Read and concat pivot outputs
dfs_p = [pd.read_csv(file, dtype = {'KOD_old':'str'}) for file in csv_files]
result_pivot = pd.concat(dfs_p, ignore_index = True)

result_pivot.set_index('HT_TYPE_old').to_csv(output_name_pivot)


# In[42]:


csv_files = ['2022_data.csv','2023_data.csv','2024_data.csv']
dfs = [pd.read_csv(file, dtype = {'KOD_old':'str','JOG_old':'str'}) for file in csv_files]

result = pd.concat(dfs, ignore_index = True)

#float to str
result['JOG_old'] = result['JOG_old'].astype(str).str[0]
# Drop not useful data
result = result[result['HT_TYPE_new'] != 'TOTAL']
result.to_csv('result_telep.csv', index = False)

result2 = result.pivot(index = col_list, columns = ['YEAR'], values = 'Probability').reset_index()

# merge 'PID'
result3 = result2.merge(result[result['YEAR'] == 2024][col_list_ext], how = 'left', on = col_list)


# In[43]:


result3['2023-2022'] = (result3[2023] - result3[2022])*100
result3['2024-2023'] = (result3[2024] - result3[2023])*100


# In[44]:


result3.to_csv('res3xx.csv', index = False)

