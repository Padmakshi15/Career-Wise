import dash
from dash import dcc, html, callback
import plotly.express as px
import pandas as pd
import re

# Common preprocessing

def preprocess_salary_data(df):
    if "job posting date" in df.columns and "Year" not in df.columns:
        df["job posting date"] = pd.to_datetime(df["job posting date"], errors="coerce", dayfirst=True)
        df["Year"] = df["job posting date"].dt.year

    def extract_salary(salary):
        try:
            salary = salary.replace("$", "").replace("K", "000").split("-")
            min_salary, max_salary = int(salary[0]), int(salary[1])
            return (min_salary + max_salary) / 2
        except:
            return None

    if "salary range" in df.columns and "Average Salary" not in df.columns:
        df["Average Salary"] = df["salary range"].astype(str).apply(extract_salary)

    return df.dropna(subset=["Year", "Average Salary", "experience"])

# === Page 1: Salary Growth ===
def salary_growth_layout(df):
    df = preprocess_salary_data(df)
    top_roles = df["job title"].value_counts().head(10).index.tolist()
    df = df[df["job title"].isin(top_roles)]

    grouped = df.groupby(["Year", "job title"])["Average Salary"].mean().reset_index()
    fig = px.line(
        grouped, x="Year", y="Average Salary", color="job title",
        title="\ud83d\udcc8 Salary Growth Over Time (Top 10 Roles)", markers=True
    )

    return html.Div([
        html.H2("\ud83d\udcc8 Salary Growth Over Time (Top Roles)"),
        dcc.Graph(figure=fig)
    ])

# === Page 2: Salary Distribution ===
def salary_distribution_layout(df):
    df = preprocess_salary_data(df)
    avg_salary_by_role = df.groupby("job title")["Average Salary"].mean().reset_index()
    avg_salary_by_role = avg_salary_by_role.sort_values(by="Average Salary", ascending=False).head(10)

    fig = px.bar(avg_salary_by_role, x="job title", y="Average Salary",
                 title="\ud83d\udcc8 Average Salary by Job Role (Top 10)", text="Average Salary")

    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    return html.Div([
        html.H2("\ud83d\udcc8 Job Roles vs Average Salary (Top 10 Roles)"),
        dcc.Graph(figure=fig)
    ])

# === Page 3: Experience vs Salary ===
def experience_vs_salary_layout(df):
    df = preprocess_salary_data(df)
    fig = px.scatter(
        df,
        x="experience",
        y="Average Salary",
        title="\ud83d\udc64 Experience vs Salary",
        color="Year",
        hover_data=["job title"] if "job title" in df.columns else None
    )
    return html.Div([
        html.H2("\ud83d\udc64 Experience vs Salary"),
        dcc.Graph(figure=fig)
    ])
