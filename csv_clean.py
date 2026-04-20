import pandas as pd
import numpy as np

file_path1 = "nonvoters_data (1).csv"
df = pd.read_csv(file_path1)


# drop columns that contain over 30% NA
df_clean = df.drop(columns=[
       "Q19_1", "Q19_2", "Q19_3", "Q19_4",
       "Q19_5", "Q19_6", "Q19_7", "Q19_8", "Q19_9", "Q19_10","Q22", "Q28_1", "Q28_2", "Q28_3", "Q28_4",
       "Q28_5", "Q28_6", "Q28_7", "Q28_8","Q29_1", "Q29_2", "Q29_3", "Q29_4",
       "Q29_5", "Q29_6", "Q29_7", "Q29_8", "Q29_9", "Q29_10","Q31","Q32","Q33"
   ])




df_clean["Q30_Rep"] = df_clean["Q30"] == 1
df_clean["Q30_Dem"] = df_clean["Q30"] == 2
df_clean["Q30_Ind"] = df_clean["Q30"] == 3
df_clean["Q30_Other"] = df_clean["Q30"] == 4
df_clean["Q30_None"] = df_clean["Q30"] == 5




df_clean["Over_54?"] = df_clean["ppage"] >= 54


df_clean["College_Graduate?"] = df_clean["educ"] == "College"


df_clean["Is_male?"] = df_clean["gender"] == "Male"


df_clean["Makes_over_75k?"] = df_clean["income_cat"].isin(["75-125k", "$125k or more"])


col_replace_list_t_f = ["Q30_Rep", "Q30_Dem", "Q30_Ind", "Q30_Other", "Q30_None", "Over_54?",
                            "College_Graduate?", "Is_male?", "Makes_over_75k?"]


df_clean.replace(-1, np.nan, inplace=True)
df_clean.dropna(inplace=True)
print(len(df_clean))
df_clean.to_csv('nonvoters_clean.csv', index=False)

