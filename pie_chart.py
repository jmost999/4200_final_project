import pandas as pd
import altair as alt

df = pd.read_csv("df_clean.csv")
df_always_vote = df[df["Q26"] == 1].copy()

party_map = {1: "Republican", 2: "Democrat", 3: "Independent", 4: "Other", 5: "None"}
gender_map = {True: "Male", False: "Female"}

df_always_vote["gender"] = df_always_vote["Is_male?"].map(gender_map)
df_always_vote["income"] = df_always_vote["income_cat"]
df_always_vote["party"] = df_always_vote["Q30"].map(party_map)

pie_df = df_always_vote.groupby(["gender", "income", "party"]).size().reset_index(name="count")

gender_select = alt.binding_select(options=["All", "Male", "Female"], name="Gender: ")
gender_param = alt.param(bind=gender_select, value="All", name="gender_val")

income_select = alt.binding_select(options=["All", "$125k or more", "$75-125k", "$40-75k", "Less than $40k"], name="Income: ")
income_param = alt.param(bind=income_select, value="All", name="income_val")

chart = alt.Chart(pie_df).mark_arc().encode(
    theta=alt.Theta("count:Q", stack=True),
    color=alt.Color("party:N", scale=alt.Scale(
    domain=["Republican", "Democrat", "Independent", "Other", "None"],
    range=["Red", "Blue", "Green", "Yellow", "Black"]),legend=alt.Legend(title="Party by Color"))
).add_params(
    gender_param, income_param
).transform_filter("(gender_val === 'All') || (datum.gender === gender_val)"
).transform_filter("(income_val === 'All') || (datum.income === income_val)"
).properties(
    title="Always Voters by Party",
    width=670,
    height=670
)

chart.save("pie_chart.html")