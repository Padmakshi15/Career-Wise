import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

def get_layout(df):
    # Top hiring companies
    top_hiring_companies = df["company"].value_counts().head(10)
    hiring_fig = px.bar(
        x=top_hiring_companies.values,
        y=top_hiring_companies.index,
        orientation="h",
        title="Top 10 Companies Hiring the Most",
        labels={"x": "Number of Job Postings", "y": "Company"},
        color=top_hiring_companies.values,
        color_continuous_scale="Blues"
    )

    hiring_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI, sans-serif", size=14),
        margin=dict(l=60, r=20, t=60, b=40),
    )

    # Netflix-style role cards
    job_trend = df.groupby("role").size().reset_index(name="Job Count").sort_values(by="Job Count", ascending=False).head(10)

    role_cards = []
    for i, row in job_trend.iterrows():
        role_cards.append(
            html.Div([
                html.Div(f"{i+1}", style={
                    "fontSize": "40px",
                    "fontWeight": "bold",
                    "color": "#ff4b5c",
                    "marginBottom": "10px"
                }),
                html.Div(row["role"], style={
                    "fontSize": "18px",
                    "fontWeight": "600",
                    "textAlign": "center",
                    "color": "#333"
                }),
                html.Div(f"{row['Job Count']} jobs", style={
                    "fontSize": "16px",
                    "color": "#666",
                    "marginTop": "5px"
                }),
            ], style={
                "backgroundColor": "#ffffff",
                "borderRadius": "15px",
                "padding": "20px",
                "margin": "10px",
                "width": "180px",
                "boxShadow": "0px 4px 10px rgba(0,0,0,0.1)",
                "textAlign": "center",
                "display": "inline-block",
                "verticalAlign": "top"
            })
        )

    # Company-wise job role breakdown
    top_companies = df["company"].value_counts().head(10).index.tolist()
    df_filtered = df[df["company"].isin(top_companies)]

    # --- Get Top 8 roles for each company ---
    breakdown_list = []
    for company in top_companies:
        company_df = df_filtered[df_filtered["company"] == company]
        top_roles = company_df["role"].value_counts().head(8).index.tolist()
        temp = company_df[company_df["role"].isin(top_roles)]
        breakdown_list.append(temp)

    breakdown_df = pd.concat(breakdown_list)
    breakdown = breakdown_df.groupby(["company", "role", "location"]).size().reset_index(name="Job Postings")

    breakdown_fig = px.bar(
        breakdown,
        x="Job Postings",
        y="company",
        color="role",
        orientation="h",
        title="Company-wise Job Role Distribution",
        labels={"company": "Company", "role": "Role", "location": "Location", "Job Postings": "Count"},
        hover_data={"role": True, "location": True}
    )

    breakdown_fig.update_traces(
        hovertemplate="<b>Company:</b> %{y}<br>" +
                      "<b>Role:</b> %{customdata[0]}<br>" +
                      "<b>Location:</b> %{customdata[1]}<br>" +
                      "<b>Count:</b> %{x}<extra></extra>",
        customdata=breakdown[["role", "location"]],
    )

    breakdown_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI, sans-serif", size=14),
        margin=dict(l=60, r=20, t=60, b=40),
    )

    return html.Div([
        html.H1("📈 Job Market Insights", style={
            "textAlign": "center",
            "marginTop": "20px",
            "fontFamily": "Segoe UI, sans-serif",
            "color": "#333"
        }),

        html.Div([
            html.H3("🏢 Top 10 Companies Hiring", style={"textAlign": "center", "marginBottom": "10px"}),
            dcc.Graph(figure=hiring_fig)
        ], style={
            "backgroundColor": "#f9f9f9",
            "padding": "20px",
            "borderRadius": "12px",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.05)",
            "marginBottom": "30px"
        }),

        html.Div([
            html.H3("🏢 Company-wise Job Role Distribution", style={"textAlign": "center", "marginBottom": "20px"}),
            dcc.Graph(figure=breakdown_fig)
        ], style={
            "backgroundColor": "#f7f7f7",
            "padding": "30px",
            "borderRadius": "12px",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.05)"
        }),

        html.Div([
            html.H3("🚀 Top 10 Fastest Growing Job Roles", style={"textAlign": "center", "marginBottom": "20px"}),
            html.Div(role_cards, style={
                "display": "flex",
                "flexWrap": "wrap",
                "justifyContent": "center"
            })
        ], style={
            "backgroundColor": "#fdfdfd",
            "padding": "30px",
            "borderRadius": "12px",
            "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.05)",
            "marginBottom": "30px"
        }),
    ])
