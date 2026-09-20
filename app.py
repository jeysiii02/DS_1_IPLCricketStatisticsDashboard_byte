# IPL Cricket Statistics Dashboard - Live Streamlit Application

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import kagglehub

from pathlib import Path


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="IPL Cricket Statistics Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Cricket Statistics Dashboard")

st.write(
    "Explore IPL match statistics, leading run-scorers, "
    "wicket-takers, and team win percentages."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():

    # Downloads the IPL dataset from Kaggle.
    dataset_path = kagglehub.dataset_download(
        "patrickb1912/ipl-complete-dataset-20082020"
    )

    matches_path = next(
        Path(dataset_path).rglob("matches.csv")
    )

    deliveries_path = next(
        Path(dataset_path).rglob("deliveries.csv")
    )

    matches = pd.read_csv(matches_path)

    deliveries = pd.read_csv(
        deliveries_path,
        encoding="latin1",
        engine="python",
        sep=None
    )

    # Creates working copies.
    matches_clean = matches.copy()
    deliveries_clean = deliveries.copy()

    # Converts match dates into datetime format.
    matches_clean["date"] = pd.to_datetime(
        matches_clean["date"]
    )

    # Standardizes historical franchise names.
    team_name_mapping = {
        "Delhi Daredevils": "Delhi Capitals",
        "Kings XI Punjab": "Punjab Kings",
        "Royal Challengers Bangalore":
            "Royal Challengers Bengaluru",
        "Rising Pune Supergiants":
            "Rising Pune Supergiant"
    }

    columns_to_replace = [
        "team1",
        "team2",
        "toss_winner",
        "winner"
    ]

    for column in columns_to_replace:
        matches_clean[column] = (
            matches_clean[column]
            .replace(team_name_mapping)
        )

    deliveries_clean["batting_team"] = (
        deliveries_clean["batting_team"]
        .replace(team_name_mapping)
    )

    deliveries_clean["bowling_team"] = (
        deliveries_clean["bowling_team"]
        .replace(team_name_mapping)
    )

    return matches_clean, deliveries_clean


matches_clean, deliveries_clean = load_data()


# ---------------------------------------------------------
# FILTER OPTIONS
# ---------------------------------------------------------

season_options = ["All Seasons"] + sorted(
    matches_clean["season"]
    .dropna()
    .unique()
    .tolist()
)

team_options = ["All Teams"] + sorted(
    set(matches_clean["team1"].dropna()) |
    set(matches_clean["team2"].dropna())
)


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("Dashboard Filters")

selected_season = st.sidebar.selectbox(
    "Select Season",
    season_options
)

selected_team = st.sidebar.selectbox(
    "Select Team",
    team_options
)


# ---------------------------------------------------------
# FILTER MATCH DATA
# ---------------------------------------------------------

filtered_matches = matches_clean.copy()

if selected_season != "All Seasons":
    filtered_matches = filtered_matches[
        filtered_matches["season"] == selected_season
    ]

if selected_team != "All Teams":
    filtered_matches = filtered_matches[
        (filtered_matches["team1"] == selected_team) |
        (filtered_matches["team2"] == selected_team)
    ]

selected_match_ids = filtered_matches["id"].tolist()

filtered_deliveries = deliveries_clean[
    deliveries_clean["match_id"].isin(
        selected_match_ids
    )
]


# Creates team-specific batting and bowling datasets.

if selected_team != "All Teams":

    batting_deliveries = filtered_deliveries[
        filtered_deliveries["batting_team"]
        == selected_team
    ]

    bowling_deliveries = filtered_deliveries[
        filtered_deliveries["bowling_team"]
        == selected_team
    ]

else:

    batting_deliveries = filtered_deliveries
    bowling_deliveries = filtered_deliveries


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

st.subheader(
    f"Season: {selected_season} | Team: {selected_team}"
)

st.metric(
    "Matches Included",
    len(filtered_matches)
)


# ---------------------------------------------------------
# CHART 1 - RUNS PER MATCH
# ---------------------------------------------------------

st.subheader("Runs per Match Over Time")

filtered_runs = (
    filtered_deliveries
    .groupby("match_id")["total_runs"]
    .sum()
    .reset_index()
)

filtered_runs = filtered_runs.merge(
    filtered_matches[
        ["id", "date", "season"]
    ],
    left_on="match_id",
    right_on="id",
    how="left"
)

filtered_runs = filtered_runs.sort_values("date")

fig1, ax1 = plt.subplots(figsize=(12, 5))

for season, season_data in filtered_runs.groupby(
    "season"
):

    season_data = (
        season_data
        .sort_values("date")
        .copy()
    )

    # Separates long breaks within a season.
    season_data["segment"] = (
        season_data["date"]
        .diff()
        .dt.days
        .gt(30)
        .cumsum()
    )

    for _, segment_data in season_data.groupby(
        "segment"
    ):

        ax1.plot(
            segment_data["date"],
            segment_data["total_runs"],
            linewidth=1.5
        )

ax1.set_xlabel("Match Date")
ax1.set_ylabel("Total Runs")
ax1.grid(alpha=0.3)

fig1.tight_layout()

st.pyplot(fig1)

plt.close(fig1)


# ---------------------------------------------------------
# TWO-COLUMN PLAYER STATISTICS
# ---------------------------------------------------------

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# CHART 2 - TOP 10 RUN-SCORERS
# ---------------------------------------------------------

with col1:

    st.subheader("Top 10 Run-Scorers")

    top_scorers = (
        batting_deliveries
        .groupby("batter")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    fig2, ax2 = plt.subplots(figsize=(7, 5))

    ax2.barh(
        top_scorers.index,
        top_scorers.values
    )

    ax2.set_xlabel("Total Runs")
    ax2.set_ylabel("Player")

    fig2.tight_layout()

    st.pyplot(fig2)

    plt.close(fig2)


# ---------------------------------------------------------
# CHART 3 - TOP 10 WICKET-TAKERS
# ---------------------------------------------------------

with col2:

    st.subheader("Top 10 Wicket-Takers")

    bowler_wicket_types = [
        "caught",
        "bowled",
        "lbw",
        "stumped",
        "caught and bowled",
        "hit wicket"
    ]

    filtered_wickets = bowling_deliveries[
        bowling_deliveries[
            "dismissal_kind"
        ].isin(bowler_wicket_types)
    ]

    top_wicket_takers = (
        filtered_wickets
        .groupby("bowler")
        .size()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    fig3, ax3 = plt.subplots(figsize=(7, 5))

    ax3.barh(
        top_wicket_takers.index,
        top_wicket_takers.values
    )

    ax3.set_xlabel("Total Wickets")
    ax3.set_ylabel("Player")

    fig3.tight_layout()

    st.pyplot(fig3)

    plt.close(fig3)


# ---------------------------------------------------------
# CHART 4 - TEAM WIN PERCENTAGE
# ---------------------------------------------------------

st.subheader("Team Win Percentage")

fig4, ax4 = plt.subplots(figsize=(12, 6))

if selected_team == "All Teams":

    matches_played = pd.concat([
        filtered_matches["team1"],
        filtered_matches["team2"]
    ]).value_counts()

    team_wins = (
        filtered_matches["winner"]
        .value_counts()
    )

    win_percentage = (
        team_wins
        .reindex(
            matches_played.index,
            fill_value=0
        )
        / matches_played
        * 100
    ).sort_values()

    ax4.barh(
        win_percentage.index,
        win_percentage.values
    )

else:

    matches_count = len(filtered_matches)

    wins_count = (
        filtered_matches["winner"]
        == selected_team
    ).sum()

    win_percentage = (
        wins_count / matches_count * 100
        if matches_count > 0
        else 0
    )

    ax4.barh(
        [selected_team],
        [win_percentage]
    )

    ax4.text(
        win_percentage + 1,
        0,
        f"{win_percentage:.2f}%",
        va="center"
    )

ax4.set_xlim(0, 100)
ax4.set_xlabel("Win Percentage (%)")
ax4.set_ylabel("Team")

fig4.tight_layout()

st.pyplot(fig4)

plt.close(fig4)


# ---------------------------------------------------------
# DATA SOURCE
# ---------------------------------------------------------

st.divider()

st.caption(
    "Data Source: IPL Complete Dataset on Kaggle | "
    "patrickb1912/ipl-complete-dataset-20082020 | "
    "Extraction Date: September 20, 2026"
)