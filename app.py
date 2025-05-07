import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Importing pages
import pages.JobMarket.job_market as job_market
import pages.JobMarket.jobmarket_home as job_home
import pages.SalaryTrends.salary_trends as salary_trends
import pages.SalaryTrends.salarygraphs_divided as salary_graphs
import pages.skill_analysis as skill_analysis
import pages.Reports.reports as reports
import pages.home as home  # Home page

# Load dataset once to avoid reloading in each page
df = pd.read_csv(r"data/Enhanced_JD_Dataset (version 1).csv")

# Ensure required columns are formatted properly
df["job posting date"] = pd.to_datetime(df["job posting date"], errors="coerce")
df["Year"] = df["job posting date"].dt.year

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Required for deployment

# App layout
app.layout = html.Div([
    # Navigation Bar
    html.Div([
        html.A("🏠 Home", href="/", className='nav-link'),
        html.A("📈 Skill Analysis", href="/skill-analysis", className='nav-link'),
        
        html.Div([
            html.A("📊 Job Market Insights", href="/job-market", className='nav-link dropdown'),
            html.Div([
                html.A("📌 Job Trends", href="/job-market/job-trends", className='dropdown-item'),
                html.A("📌 Hiring Companies", href="/job-market/company-trends", className='dropdown-item'),
            ], className='dropdown-content')
        ], className='dropdown-container'),

        html.Div([
            html.A("💰 Salary Trends", href="/salary-trends", className='nav-link dropdown'),
            html.Div([
                html.A("📌 Salary Growth", href="/salary-trends/salary_growth_layout", className='dropdown-item'),
                html.A("📌 Salary Distribution", href="/salary-trends/salary_distribution_layout", className='dropdown-item'),
                html.A("📌 Experience vs Salary", href="/salary-trends/experience_vs_salary_layout", className='dropdown-item'),
            ], className='dropdown-content')
        ], className='dropdown-container'),
        # html.A("📑 Reports", href="/reports", className='nav-link'),
    ], className='navbar'),

    # Page Content
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# Callback to handle page navigation
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/" or pathname == "":
        return home.get_layout()
    elif pathname == "/job-market":
        return job_home.get_layout(df)
    elif pathname == "/job-market/job-trends":
        return job_market.job_trends_layout(df)
    elif pathname == "/job-market/company-trends":
        return job_market.company_trends_layout(df)
    elif pathname == "/salary-trends":
        return salary_trends.render_salary_trends_layout(df)
    elif pathname == "/salary-trends/experience_vs_salary_layout":
        return salary_graphs.experience_vs_salary_layout(df)
    elif pathname == "/salary-trends/salary_growth_layout":
        return salary_graphs.salary_growth_layout(df)
    elif pathname == "/salary-trends/salary_distribution_layout":
        return salary_graphs.salary_distribution_layout(df)
    elif pathname == "/skill-analysis":
        return skill_analysis.get_layout(df)
    # elif pathname == "/reports":
    #     return reports.get_layout(df)
    else:
        return html.Div([
            html.H2("404 - Page Not Found"),
            html.P("The page you’re looking for doesn’t exist.")
        ])

# Optional callback (example — only use if you have 'company-bar' and 'company-info' in layout)
@app.callback(
    Output("company-info", "children"),
    Input("company-bar", "clickData"),
    prevent_initial_call=True
)
def display_company_details(clickData):
    if clickData:
        company = clickData["points"][0]["y"]
        return f"You clicked on: {company}"
    return "Click on a bar to see more details."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
