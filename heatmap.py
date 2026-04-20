import altair as alt
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from narwhals import DataFrame

df = pd.read_csv("nonvoters_clean.csv")
df = pd.DataFrame(df)
df_clean_copy = df
trust_president = df_clean_copy.groupby("Q30")["Q8_1"].mean().tolist()
trust_congress = df_clean_copy.groupby("Q30")["Q8_2"].mean().tolist()
trust_supreme_court = df_clean_copy.groupby("Q30")["Q8_3"].mean().tolist()
trust_cdc = df_clean_copy.groupby("Q30")["Q8_4"].mean().tolist()
trust_election_officials = df_clean_copy.groupby("Q30")["Q8_5"].mean().tolist()
trust_fbi = df_clean_copy.groupby("Q30")["Q8_6"].mean().tolist()
trust_news = df_clean_copy.groupby("Q30")["Q8_7"].mean().tolist()
trust_police = df_clean_copy.groupby("Q30")["Q8_8"].mean().tolist()
trust_usps = df_clean_copy.groupby("Q30")["Q8_9"].mean().tolist()

if __name__ == "__main__":
    data=[trust_president,trust_congress,trust_supreme_court,trust_cdc,trust_election_officials,trust_fbi,trust_news,trust_police,trust_usps]
    fig = px.imshow(data,
                    labels=dict(x="Political Party", y="Question", color="Scale of 1-4"),
                    x=['Republican', 'Democrat', 'Independent','Other', 'None'],
                    y=['Trust President', 'Trust Congress', 'Trust Supreme Court','Trust CDC', 'Trust Election Officials','Trust FBI','Trust News','Trust Police','Trust USPS'],
                    color_continuous_scale = "reds_r",
                    title="Trust by Political Parties (lower values imply more trust)"
                   )


    fig.show()
    fig.write_html("heatmap.html")

