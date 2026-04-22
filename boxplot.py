import altair as alt
import pandas as pd

df = pd.read_csv("nonvoters_clean.csv")

cols = ["Q2_1","Q2_2","Q2_3","Q2_4","Q2_5",
        "Q2_6","Q2_7","Q2_8","Q2_9","Q2_10"]

label_map = {
    "Q2_1": "Vote",
    "Q2_2": "Be in a Jury",
    "Q2_3": "Follow the News",
    "Q2_4": "Display a Flag",
    "Q2_5": "Participate in Census",
    "Q2_6": "Know the Pledge",
    "Q2_7": "Support the Military",
    "Q2_8": "Respect Disagreements",
    "Q2_9": "Believe in God",
    "Q2_10": "Protest"
}

party_map = {1: "Republican", 2: "Democrat", 3: "Independent", 4: "Other", 5: "None"}

df["party"] = df["Q30"].map(party_map)

long_df = df[["party"] + cols].melt(id_vars="party", var_name="question", value_name="score")
long_df["question"] = long_df["question"].map(label_map)
long_df = long_df.dropna(subset=["score", "party"])

party_select = alt.binding_select(
    options=["All", "Republican", "Democrat", "Independent", "Other", "None"],
    name="Party: "
)
party_param = alt.param(bind=party_select, value="All", name="party_val")

chart = alt.Chart(long_df).mark_boxplot(
    extent="min-max",
    size=30,
    outliers=alt.MarkConfig(size=15, opacity=0.4)
).encode(
    x=alt.X("question:N", axis=alt.Axis(labelAngle=-30, title="Civic Duty"), sort=list(label_map.values())),
    y=alt.Y("score:Q", axis=alt.Axis(title="Score (1 = Very Important)"), scale=alt.Scale(domain=[0, 8])),
    color=alt.Color(
        "party:N",
        scale=alt.Scale(
            domain=["Republican", "Democrat", "Independent", "Other", "None"],
            range=["#C0392B", "#2471A3", "#27AE60", "#D4AC0D", "#717D7E"]
        ),
        legend=alt.Legend(title="Party")
    ),
    tooltip=[
        alt.Tooltip("question:N", title="Question"),
        alt.Tooltip("party:N", title="Party"),
        alt.Tooltip("score:Q", title="Score")
    ]
).add_params(
    party_param
).transform_filter(
    "(party_val === 'All') || (datum.party === party_val)"
).properties(
    width=1100,
    height=850,
    title="How Important Is It To... — Distribution by Party"
)

chart.save("boxplot_q2.html")