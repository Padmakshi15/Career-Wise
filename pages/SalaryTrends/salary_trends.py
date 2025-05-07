from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import re

# === Layout ===   
def render_salary_trends_layout(df):
    def extract_salary(salary):
        try:   
            salary = salary.replace("$", "").replace("K", "000").split("-")
            min_salary, max_salary = int(salary[0]), int(salary[1])
            return (min_salary + max_salary) / 2
        except:      
            return None    

    def extract_experience(exp):
        try:
            numbers = re.findall(r'\d+', str(exp))
            return float(numbers[0]) if numbers else None
        except:
            return None

    if "salary range" in df.columns and "Average Salary" not in df.columns:
        df["Average Salary"] = df["salary range"].astype(str).apply(extract_salary)
    df["experience_clean"] = df["experience"].apply(extract_experience)

    df = df.dropna(subset=["Year", "Average Salary", "experience_clean"])

    min_exp = int(df["experience_clean"].min())
    max_exp = int(df["experience_clean"].max())
    top_roles = df["job title"].value_counts().head(10).index.tolist()

    return html.Div([
        html.H2("\ud83d\udcb0 Salary Trends", className="section-title"),

        html.Div([
            html.Div([
                html.Label("Select Year Range:"),
                dcc.RangeSlider(
                    id="year-range-slider",
                    min=df["Year"].min(),
                    max=df["Year"].max(),
                    step=1,
                    value=[df["Year"].min(), df["Year"].max()],
                    marks={str(year): str(year) for year in sorted(df["Year"].unique())}
                )
            ], style={"margin-bottom": "20px"}),

            html.Div([
                html.Label("Filter by Experience (Years):"),
                dcc.RangeSlider(
                    id="experience-slider",
                    min=min_exp,
                    max=max_exp,
                    step=1,
                    value=[min_exp, max_exp],
                    marks={str(i): str(i) for i in range(min_exp, max_exp + 1, 2)}
                )
            ], style={"margin-bottom": "20px"}),

            # html.Div([
            #     html.Label("Select Industry:"),
            #     dcc.Dropdown(
            #         id="industry-dropdown",
            #         options=[{"label": i, "value": i} for i in df["Company Industry"].dropna().unique()],
            #         multi=True,
            #         placeholder="Filter by industry"
            #     )
            # ], style={"margin-bottom": "20px"}),

            html.Div([
                html.Label("Select Job Roles:"),
                dcc.Dropdown(
                    id="role-dropdown",
                    options=[{"label": role, "value": role} for role in top_roles],
                    value=top_roles[:1],
                    multi=True
                )
            ])
        ], style={"margin-bottom": "40px"}),

        dcc.Graph(id="salary-growth-graph"),
        dcc.Graph(id="salary-distribution-graph"),
        dcc.Graph(id="experience-salary-graph")
    ])


@callback(
    Output("salary-growth-graph", "figure"),
    Output("salary-distribution-graph", "figure"),
    Output("experience-salary-graph", "figure"),
    Input("year-range-slider", "value"),
    Input("experience-slider", "value"),
    # Input("industry-dropdown", "value"),
    Input("role-dropdown", "value")
)
def update_salary_trend_graphs(year_range, exp_range, selected_roles):
    df = pd.read_csv("data/Enhanced_JD_Dataset (version 1).csv")
    df["job posting date"] = pd.to_datetime(df["job posting date"], errors="coerce")
    df["Year"] = df["job posting date"].dt.year

    def extract_salary(salary):
        try:
            salary = salary.replace("$", "").replace("K", "000").split("-")
            min_salary, max_salary = int(salary[0]), int(salary[1])
            return (min_salary + max_salary) / 2
        except:
            return None

    def extract_experience(exp):
        try:
            numbers = re.findall(r'\d+', str(exp))
            return float(numbers[0]) if numbers else None
        except:
            return None

    if "salary range" in df.columns and "Average Salary" not in df.columns:
        df["Average Salary"] = df["salary range"].astype(str).apply(extract_salary)
    df["experience_clean"] = df["experience"].apply(extract_experience)
    df = df.dropna(subset=["Year", "Average Salary", "experience_clean", "job title"])

    df = df[
        (df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1]) &
        (df["experience_clean"] >= exp_range[0]) & (df["experience_clean"] <= exp_range[1])
    ]
    # if selected_industries:
    #     df = df[df["Company Industry"].isin(selected_industries)]
    if selected_roles:
        df = df[df["job title"].isin(selected_roles)]

    growth_data = df.groupby(["Year", "job title"])["Average Salary"].mean().reset_index()
    growth_fig = px.line(growth_data, x="Year", y="Average Salary", color="job title", markers=True,
                         title="\ud83d\udcc8 Salary Growth Over Time by Role")

    df["Salary Bin"] = pd.cut(df["Average Salary"], bins=30)
    salary_counts = df["Salary Bin"].value_counts().sort_index().reset_index()
    salary_counts.columns = ["Salary Range", "Count"]
    salary_counts["Midpoint"] = salary_counts["Salary Range"].apply(lambda x: x.mid)
    dist_fig = px.scatter(salary_counts, x="Midpoint", y="Count",
                          title="\ud83d\udcc8 Salary Distribution (Filtered)",
                          labels={"Midpoint": "Salary", "Count": "Postings"})

    exp_fig = px.scatter(df, x="experience_clean", y="Average Salary",
                         title="\ud83d\udc64 Experience vs Salary",
                         color="job title")

    return growth_fig, dist_fig, exp_fig
