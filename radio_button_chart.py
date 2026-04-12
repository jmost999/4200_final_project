import altair as alt
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('df_clean.csv')


voting = df.groupby("Q30")["Q2_1"].mean().tolist()
jury = df.groupby("Q30")["Q2_2"].mean().tolist()
news_follow = df.groupby("Q30")["Q2_3"].mean().tolist()
flag = df.groupby("Q30")["Q2_4"].mean().tolist()
census = df.groupby("Q30")["Q2_5"].mean().tolist()
know_pledge = df.groupby("Q30")["Q2_6"].mean().tolist()
military = df.groupby("Q30")["Q2_7"].mean().tolist()
respect_disagreements = df.groupby("Q30")["Q2_8"].mean().tolist()
god = df.groupby("Q30")["Q2_9"].mean().tolist()
protest = df.groupby("Q30")["Q2_10"].mean().tolist()

unique_choices = ['Republican', 'Democrat', 'Independent', 'Other', 'None']

cols = ["Q2_1","Q2_2","Q2_3","Q2_4","Q2_5",
        "Q2_6","Q2_7","Q2_8","Q2_9","Q2_10"]

result = df.groupby("Q30")[cols].mean().reset_index()
result.columns = ["party","vote","be in a jury","follow the news","display a flag","participate in the census",
                  "know the pledge","support the military","respect disagreements","believe in god","protest"]

result["party"] = unique_choices
long_df = result.melt(id_vars="party", var_name="question", value_name="mean_score")

chart_type = alt.param(
    name="ChartType",
    bind=alt.binding_radio(options=["Grouped Bar","Line Chart"], name="Select Chart Type: "),
    value="Grouped Bar"
)

line_parties = alt.Chart(long_df).mark_line(point=True).encode(
    x=alt.X("question:N"),
    y="mean_score:Q",
    color=alt.Color("party:N", scale=alt.Scale(
    domain=["Republican", "Democrat", "Independent", "Other", "None"],
    range=["Red", "Blue", "Green", "Yellow", "Black"]),legend=alt.Legend(title="Party by Color")),
    tooltip = [alt.Tooltip('mean_score:Q', title='Mean Score:', format='.2f'),
                alt.Tooltip('party:N', title='Political Party:')]

).properties(width=800, height=600, title = "Line chart- How important is it to... (1 being very important)").transform_filter(
    chart_type == "Line Chart"
)

bar_plot = alt.Chart(long_df).mark_bar().encode(
    x=alt.X("question:N", axis=alt.Axis(labelAngle=-30),
            scale=alt.Scale(paddingInner=0.4)),  # space between groups (0–1)
    y="mean_score:Q",
    color=alt.Color("party:N", scale=alt.Scale(
    domain=["Republican", "Democrat", "Independent", "Other", "None"],
    range=["Red", "Blue", "Green", "Yellow", "Black"]),legend=alt.Legend(title="Party by Color")),
    xOffset=alt.XOffset("party:N", scale=alt.Scale(paddingInner=0.1)),
    tooltip=[alt.Tooltip('mean_score:Q', title='Mean Score:', format='.2f'),
             alt.Tooltip('party:N', title='Political Party:')]


).properties(width=800, height=600, title = "Line chart- How important is it to... (1 being very important)").transform_filter(
    chart_type == "Grouped Bar"
)

final_chart = (line_parties + bar_plot).add_params(chart_type)
final_chart.save("radio_button_q2.html")









