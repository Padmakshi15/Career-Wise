import dash
from dash import dcc, html, dash_table, callback, Input, Output, State
import plotly.express as px
from collections import Counter
import pandas as pd

# Global variable to store skill-role mapping
skill_role_global_df = pd.DataFrame()

def get_layout(df):
    global skill_role_global_df

    # Preprocess Skills and Roles
    skill_role_data = []
    for _, row in df.dropna(subset=["skills", "role"]).iterrows():
        skills = [s.strip() for s in row["skills"].split(",")]
        for skill in skills:
            skill_role_data.append((skill, row["role"]))

    skill_role_df = pd.DataFrame(skill_role_data, columns=["Skill", "Role"])
    grouped_df = skill_role_df.groupby(["Skill", "Role"]).size().reset_index(name="Opportunities")
    skill_role_global_df = grouped_df.copy()

    top_skills = grouped_df.groupby("Skill")["Opportunities"].sum().nlargest(15).reset_index()

    return html.Div([
        html.H2("Top Skills and Their Related Roles", style={"textAlign": "center", "marginTop": "20px"}),

        dash_table.DataTable(
            id="skill-table",
            columns=[
                {"name": "Skill", "id": "Skill"},
                {"name": "Total Opportunities", "id": "Opportunities"}
            ],
            data=top_skills.to_dict("records"),
            style_cell={
                "textAlign": "left", "padding": "12px", "fontFamily": "Arial", "fontSize": "16px",
                "whiteSpace": "normal", "height": "auto", "minWidth": "200px", "maxWidth": "500px",
            },
            style_header={
                "backgroundColor": "#1f77b4", "color": "white", "fontWeight": "bold", "textAlign": "center"
            },
            style_table={
                "width": "80%", "margin": "auto", "marginTop": "30px", "border": "1px solid #ccc",
                "borderRadius": "10px", "overflowX": "auto"
            },
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "#f9f9f9"}
            ],
            cell_selectable=True
        ),

        html.Div(id="skill-role-graph", style={"marginTop": "40px", "width": "85%", "margin": "auto"})
    ])

# Callback: Make entire row clickable and show graph for related roles
@callback(
    Output("skill-role-graph", "children"),
    Input("skill-table", "active_cell"),
    State("skill-table", "data")
)
def display_roles_for_selected_skill(active_cell, table_data):
    if active_cell is None or active_cell.get("row") is None:
        return None

    selected_index = active_cell["row"]
    selected_skill = table_data[selected_index]["Skill"]
    filtered_df = skill_role_global_df[skill_role_global_df["Skill"] == selected_skill]

    fig = px.bar(
        filtered_df, x="Opportunities", y="Role", orientation="h",
        title=f"Roles requiring {selected_skill}", color="Role"
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial", size=14)
    )

    return dcc.Graph(figure=fig)
