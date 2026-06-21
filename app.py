import streamlit as st
import streamlit as st
import pandas as pd

st.title("IPL Auction Intelligence Dashboard")
st.write("Welcome to the IPL Auction Dashboard!")


df = pd.read_csv("player_batting_stats.csv")
bowling_df = pd.read_csv("bowling_stats.csv")
match_df = pd.read_csv("match_stats.csv")
df["auction_score"] = (
df["runs"] * 0.5 +
df["strike_rate"] * 2
)
st.metric(
    "Total Batters",
    len(df)
)

st.metric(
    "Total Bowlers",
    len(bowling_df)
)

st.metric(
    "Total Matches",
    len(match_df)
)
page = st.sidebar.selectbox(
    "Choose Analysis",
    [   
        "Home",
        "Batting Analytics",
        "Bowling Analytics",
        "Match Analysis",
        "Auction Recommendations",
        "Auction Market Analysis"
    ]
)

if page == "Home":

    st.title("IPL Auction Intelligence Dashboard")

    st.markdown("""
    ### Project Objective

    This dashboard helps IPL franchises identify
    high-value players using batting, bowling,
    and match performance analytics.

    ### Features

    - Batting Analytics
    - Bowling Analytics
    - Match Analysis
    - Auction Recommendations
    - Player Comparison
    """)

if page == "Batting Analytics":
    st.header("Batting Analytics")
    st.title("IPL Auction Intelligence Dashboard")
    st.write("Welcome to the IPL Auction Dashboard!")

    df = pd.read_csv("player_batting_stats.csv")

    st.subheader("Player Batting Data")
    st.dataframe(df)
    

    st.subheader("Player Search")

    player = st.selectbox(
        "Select a Player",
        sorted(df["batter"].unique()),
        key="player_search"
    )

    st.write(df[df["batter"] == player])   

    #Top 10 Scores
    st.subheader("Top 10 Run Scorers")

    top_batters = df.sort_values("runs", ascending=False).head(10)

    st.bar_chart(
        top_batters.set_index("batter")["runs"]
    )
    csv = top_batters.to_csv(index=False)

    st.download_button(
    "Download Recommendations",
    csv,
    "recommendations.csv",
    "text/csv"
)

    #Top Strike Rates
    st.subheader("Top Strike Rate Players")

    top_sr = df.sort_values("strike_rate", ascending=False).head(10)

    st.bar_chart(
        top_sr.set_index("batter")["strike_rate"]
    )

    #Auction Intelligence Score
    df["auction_score"] = (
        df["runs"] * 0.6 +
        df["strike_rate"] * 10
    )

    #Top Auction Targets
    st.subheader("Top Auction Targets")

    top_targets = df.sort_values(
        "auction_score",
        ascending=False
    ).head(10)

    st.dataframe(
        top_targets[
            ["batter", "runs", "strike_rate", "auction_score"]
        ]
    )

    #Comparison
    player1 = st.selectbox(
        "Player 1",
        sorted(df["batter"].unique()),
        key="player1_alt"
    )

    player2 = st.selectbox(
        "Player 2",
        sorted(df["batter"].unique()),
        key="player2_alt"
    )
    comparison = df[df["batter"].isin([player1, player2])]
    st.dataframe(comparison)

    #Comparison Visualisation
    st.subheader("Player Comparison Chart")

    comparison_data = comparison.set_index("batter")[["runs", "strike_rate"]]

    st.bar_chart(comparison_data)

    #Top Auction Recommendations
    st.subheader("Top 5 Auction Recommendations")

    top5 = df.sort_values(
        "auction_score",
        ascending=False
    ).head(5)

    st.dataframe(top5)

elif page == "Bowling Analytics":
    st.header("Bowling Analytics")
    bowling_df = pd.read_csv("bowling_stats.csv")

    #Top Wickets
    st.subheader("Top Wicket Takers")

    top_wickets = bowling_df.sort_values(
    "Wickets",
    ascending=False
    ).head(10)

    st.dataframe(top_wickets)
    st.bar_chart(
    top_wickets.set_index("Player")["Wickets"]
)   
    csv = top_wickets.to_csv(index=False)

    st.download_button(
    "Download Recommendations",
    csv,
    "recommendations.csv",
    "text/csv"
    )
    #Best Economy
    st.subheader("Best Economy Bowlers")

    best_economy = bowling_df[
        bowling_df["Wickets"] >= 20
    ].sort_values(
        "Economy",
        ascending=True
    ).head(10)

    st.dataframe(best_economy)

    st.bar_chart(
        best_economy.set_index("Player")["Economy"]
    )

elif page == "Match Analysis":
    st.header("Match Analysis")
    match_df = pd.read_csv("match_stats.csv")

    #Most Successfull Team
    st.subheader("Most Successful Teams")

    team_wins = match_df["winner"].value_counts()

    st.bar_chart(team_wins)

    #Top Teams Table
    st.subheader("Team Wins")

    st.dataframe(
        team_wins.reset_index().rename(
            columns={
                "index": "Team",
                "winner": "Wins"
            }
        )
    )

    #Top Venues
    st.subheader("Most Used Venues")

    venue_count = match_df["venue"].value_counts().head(10)

    st.bar_chart(venue_count)

    #Matches by Year
    match_df["dates"] = pd.to_datetime(match_df["dates"])

    matches_per_year = match_df.groupby(
        match_df["dates"].dt.year
    ).size()

    st.subheader("Matches Per Year")

    st.line_chart(matches_per_year)

#Auction Recommendation
elif page == "Auction Recommendations":
    st.header("Auction Recommendations")

    role = st.selectbox(
    "Select Player Role",
    ["Batsman", "Bowler", "All-Rounder"]
    )
    #Batsman Recommendation
    if role == "Batsman":

        df["batting_score"] = (
            df["runs"] * 0.5 +
            df["strike_rate"] * 2
        )

        top_batsmen = df.sort_values(
            "batting_score",
            ascending=False
        ).head(5)

        st.subheader("Top Batting Targets")

        st.dataframe(top_batsmen)

    #Bowling Recommendation
    elif role == "Bowler":

        bowling_df["bowling_score"] = (
            bowling_df["Wickets"] * 10 -
            bowling_df["Economy"] * 5
        )

        top_bowlers = bowling_df.sort_values(
            "bowling_score",
            ascending=False
        ).head(5)

        st.subheader("Top Bowling Targets")

        st.dataframe(top_bowlers)

    #All Rounder Recommendation
    elif role == "All-Rounder":

        all_rounders = pd.merge(
            df,
            bowling_df,
            left_on="batter",
            right_on="Player",
            how="inner"
        )

        all_rounders["overall_score"] = (
            all_rounders["runs"] * 0.3 +
            all_rounders["strike_rate"] * 1.5 +
            all_rounders["Wickets"] * 8 -
            all_rounders["Economy"] * 3
        )

        top_all_rounders = all_rounders.sort_values(
            "overall_score",
            ascending=False
        ).head(5)

        st.subheader("Top All-Rounders")

        st.dataframe(
            top_all_rounders[
                [
                    "batter",
                    "runs",
                    "strike_rate",
                    "Wickets",
                    "Economy",
                    "overall_score"
                ]
            ]
        )

auction_df = pd.read_csv("ipl_2023_dataset.csv")
budget = st.slider(
    "Maximum Budget (Cr)",
    1,
    20,
    10
)

filtered = auction_df[
    auction_df["Cost in Rs. (CR)"] <= budget
]

st.dataframe(filtered)

role = st.selectbox(
    "Player Type",
    ["BATSMAN", "BOWLER", "WICKETKEEPER"]
)

filtered = auction_df[
    (auction_df["Type"] == role)
]