import dash
from dash import dcc, html

def get_layout():
    return html.Div([
        html.H1("Welcome to CAREER WISE Dashboard", className="home-title"),

        html.Div([
            # html.Img(src="/assets/background_image.jpg", className="home-image"),
            html.P(
                "This dashboard provides data-driven insights into the job market, helping job seekers, employers, "
                "and policymakers make informed decisions. Explore salary trends, job demand, required skills, and industry analysis.",
                className="home-description"
            )
        ], className="home-section intro-section background-image"),

        html.Div([
            html.H3("🔍 Key Features", className="home-subtitle"),
            html.Div([

                dcc.Link(
                    html.Div([
                        html.Img(src="/assets/skill_development.jpg", className="feature-icon"),
                        html.P("Skill Demand Trends")
                    ], className="feature-card"),
                    href="/skill-analysis",
                    style={"textDecoration": "none"}
                ),
                dcc.Link(
                    html.Div([
                        html.Img(src="/assets/salary_trend.jpg", className="feature-icon"),
                        html.P("Salary Trends Analysis")
                    ], className="feature-card"),
                    href="/salary-trends",
                    style={"textDecoration": "none"}
                ),
                

                dcc.Link(
                    html.Div([
                        html.Img(src="/assets/job_market.jpg", className="feature-icon"),
                        html.P("Job Market Insights")
                    ], className="feature-card"),
                    href="/job-market",
                    style={"textDecoration": "none"}
                ),



                # dcc.Link(
                #     html.Div([
                #         html.Img(src="/assets/industry_hiring.jpg", className="feature-icon"),
                #         html.P("Industry Hiring Trends")
                #     ], className="feature-card"),
                #     href="/reports",
                #     style={"textDecoration": "none"}
                # ),

                # dcc.Link(
                #     html.Div([
                #         html.Img(src="/assets/growth_future.jpg", className="feature-icon"),
                #         html.P("Growth & Future Projections")
                #     ], className="feature-card"),
                #     href="/reports",
                #     style={"textDecoration": "none"}
                # )
            ], className="feature-container")
        ], className="home-section feature-section"),

        html.Div([
            html.H3("🧭 Navigate Through", className="home-subtitle"),
            html.P(
                "Use the navigation bar at the top to explore different sections and uncover trends in the job market.",
                className="foot-description")
        ], className="home-section navigate-section center-text")
    ])