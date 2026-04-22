import pandas as pd
import altair as alt

df = pd.read_csv("nonvoters_clean.csv")

ease_map  = {1: "Very easy", 2: "Somewhat easy", 3: "Somewhat difficult", 4: "Very difficult"}
voter_map = {"always": "Always", "sporadic": "Sporadic", "rarely/never": "Rarely/Never"}
party_map = {1: "Republican", 2: "Democrat", 3: "Independent", 4: "Other", 5: "None"}

df["ease_label"]  = df["Q16"].map(ease_map)
df["voter_label"] = df["voter_category"].map(voter_map)
df["party_label"] = df["Q30"].map(party_map)

ease_order  = ["Very easy", "Somewhat easy", "Somewhat difficult", "Very difficult"]
voter_order = ["Always", "Sporadic", "Rarely/Never"]
party_order = ["Republican", "Democrat", "Independent", "Other", "None"]

heat_df = (
    df.dropna(subset=["ease_label", "voter_label", "party_label"])
    .groupby(["ease_label", "voter_label", "party_label"])
    .size()
    .reset_index(name="count")
)

party_select = alt.binding_select(options=["All"] + party_order, name="Party: ")
party_param  = alt.param(name="party", value="All", bind=party_select)

chart = (
    alt.Chart(heat_df)
    .mark_rect()
    .encode(
        x=alt.X("ease_label:N", sort=ease_order, title="Perceived Ease of Voting",
                axis=alt.Axis(labelAngle=-15)),
        y=alt.Y("voter_label:N", sort=voter_order, title="Voter Frequency"),
        color=alt.Color("count:Q",
                        scale=alt.Scale(scheme="blues"),
                        title="Respondents"),
        tooltip=[
            alt.Tooltip("party_label:N",  title="Party"),
            alt.Tooltip("ease_label:N",   title="Ease of Voting"),
            alt.Tooltip("voter_label:N",  title="Voter Frequency"),
            alt.Tooltip("count:Q",        title="Respondents"),
        ]
    )
    .transform_filter(
        "(party === 'All') || (datum.party_label === party)"
    )
    .add_params(party_param)
    .properties(width=300, height=300, title="Ease of Voting vs. Voter Frequency")
)

chart.save("heatmap_ease_of_voting.html")