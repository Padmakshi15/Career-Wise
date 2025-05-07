import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

def get_layout(df):
    if "company" in df.columns:
        top_hiring = df["company"].value_counts().head(10)

        fig = px.bar(x=top_hiring.values, y=top_hiring.index, 
                     title="Top Hiring Companies", labels={'x': "Job Postings", 'y': "Company"}, 
                     orientation='h')

        return html.Div([
            html.H1("Reports"),
            dcc.Graph(figure=fig)
        ])
    else:
        return html.Div([
            html.H1("Reports"),
            html.P("Column 'Company' is missing in the dataset. Please check the dataset.")
        ])
