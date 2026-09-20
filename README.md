# IPL Cricket Statistics Dashboard

## Project Overview

This project is an interactive IPL statistics dashboard created for Task 1 of the Arithmatrix Virtual Internship Program (AVIP) 2026 Data Science track.

The dashboard analyzes IPL match and ball-by-ball data and presents key statistics through visualizations and interactive filters.

## Dashboard Features

The project includes the following visualizations:

- Runs per Match over time
- Top 10 IPL Run-Scorers
- Top 10 IPL Wicket-Takers
- Team Win Percentages

The dashboard also includes interactive filters for:

- Season
- Team

When a specific team is selected, the run-scorer and wicket-taker charts only display players from that team.

## Dataset

Dataset: IPL Complete Dataset

Source: Kaggle  
Source URL: https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020  
Dataset Author: Patrick B  
Dataset Identifier: `patrickb1912/ipl-complete-dataset-20082020`

Files used:

- `matches.csv`
- `deliveries.csv`

Extraction Date: September 20, 2026

The dataset is downloaded directly through KaggleHub when the notebook is executed.

## Data Preparation

The following preparation steps were performed:

- Checked dataset dimensions and data types
- Inspected missing values
- Checked for duplicate rows
- Converted match dates into datetime format
- Standardized historical franchise names
- Preserved valid missing values related to dismissals and match information
- Filtered dismissal types so only wickets credited to bowlers are included in bowling statistics

Historical franchise names were standardized as follows:

- Delhi Daredevils → Delhi Capitals
- Kings XI Punjab → Punjab Kings
- Royal Challengers Bangalore → Royal Challengers Bengaluru
- Rising Pune Supergiants → Rising Pune Supergiant

## Brief Insights

- Virat Kohli is the leading run-scorer in the dataset with 8,014 runs, followed by Shikhar Dhawan and Rohit Sharma.
- Yuzvendra Chahal leads the wicket-taking rankings with 205 wickets, followed by Piyush Chawla and Dwayne Bravo.
- Gujarat Titans have the highest overall win percentage in the dataset at 62.22%.
- Total runs per match vary considerably across IPL seasons, with several matches recording more than 400 combined runs and some recent matches exceeding 500 runs.
- The Season and Team filters allow the dashboard to explore more specific performance patterns across different teams and seasons.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- ipywidgets
- KaggleHub
- Jupyter Notebook
- Visual Studio Code

## Project Structure

```text
DS_1_IPLCricketStatisticsDashboard_byte/
│
├── images/
│   ├── runs_per_match.png
│   ├── top_10_run_scorers.png
│   ├── top_10_wicket_takers.png
│   └── team_win_percentage.png
│
├── IPL_Cricket_Dashboard.ipynb
├── README.md
├── requirements.txt
└── .gitignore