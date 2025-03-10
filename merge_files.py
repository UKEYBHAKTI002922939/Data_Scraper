#import pandas module
import pandas as pd
#read the csv file into a dataframe
df_sample1 = pd.read_csv("output_second_final.csv")
print(df_sample1)
df_sample2 = pd.read_csv("output_second_final_1.csv")
print(df_sample2)
list = ["name","title","description","images"]
df_master = df_sample1.merge(df_sample2,
                   on = list, 
                   how = 'outer')
print(df_master)
