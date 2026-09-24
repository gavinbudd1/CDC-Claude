"""Plotly figure builders. Each takes already-aggregated data and returns a Figure."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import MONTH_ORDER, PRIMARY_COLOR, SEQUENTIAL_SCALE, SEX_COLORS

_LABELS = {"births": "Births", "month": "Month", "state": "State", "sex": "Infant sex"}
_FONT = dict(family="sans-serif", size=13)


def _finish(fig: go.Figure, title: str, height: int = 420) -> go.Figure:
    """Shared layout: title, zero-based y axis where relevant, thousands separators."""
    fig.update_layout(title=dict(text=title, x=0), height=height, font=_FONT,
                      margin=dict(l=10, r=10, t=60, b=10), hoverlabel=dict(font_size=13),
                      legend=dict(orientation="h", y=-0.2, x=0))
    return fig


def monthly_trend(month_df: pd.DataFrame) -> go.Figure:
    fig = px.line(month_df, x="month", y="births", markers=True, labels=_LABELS,
                  category_orders={"month": MONTH_ORDER}, color_discrete_sequence=[PRIMARY_COLOR])
    fig.update_traces(hovertemplate="%{x}<br>Births: %{y:,}<extra></extra>")
    fig.update_yaxes(rangemode="tozero", tickformat=",", title="Births")
    fig.update_xaxes(title=None)
    return _finish(fig, "Monthly births (counts, 2025)", 380)


def sex_comparison(sex_month_df: pd.DataFrame) -> go.Figure:
    fig = px.bar(sex_month_df, x="month", y="births", color="sex", barmode="group",
                 labels=_LABELS, category_orders={"month": MONTH_ORDER, "sex": ["Female", "Male"]},
                 color_discrete_map=SEX_COLORS)
    fig.update_traces(hovertemplate="%{x} · %{fullData.name}<br>Births: %{y:,}<extra></extra>")
    fig.update_yaxes(rangemode="tozero", tickformat=",", title="Births")
    fig.update_xaxes(title=None)
    return _finish(fig, "Female vs. male births by month")


def sex_share(sex_df: pd.DataFrame) -> go.Figure:
    """Simple total-by-sex bars (zero baseline) instead of a pie chart."""
    fig = px.bar(sex_df, x="sex", y="births", color="sex", text="births", labels=_LABELS,
                 category_orders={"sex": ["Female", "Male"]}, color_discrete_map=SEX_COLORS)
    fig.update_traces(texttemplate="%{y:,}", hovertemplate="%{x}<br>Births: %{y:,}<extra></extra>")
    fig.update_yaxes(rangemode="tozero", tickformat=",", title="Births")
    fig.update_xaxes(title=None)
    fig.update_layout(showlegend=False)
    return _finish(fig, "Total births by infant sex", 380)


def state_ranking(totals: pd.DataFrame, n: int, title_suffix: str = "") -> go.Figure:
    data = totals.head(n).iloc[::-1]  # reverse so the largest bar is on top
    fig = px.bar(data, x="births", y="state", orientation="h", labels=_LABELS,
                 color_discrete_sequence=[PRIMARY_COLOR])
    fig.update_traces(hovertemplate="%{y}<br>Births: %{x:,}<extra></extra>")
    fig.update_xaxes(rangemode="tozero", tickformat=",", title="Births")
    fig.update_yaxes(title=None)
    return _finish(fig, f"Top {len(data)} geographies by births{title_suffix}",
                   max(360, 24 * len(data) + 120))


def choropleth(totals: pd.DataFrame) -> go.Figure:
    fig = px.choropleth(totals, locations="state_abbr", locationmode="USA-states",
                        color="births", scope="usa", hover_name="state",
                        hover_data={"state_abbr": False, "births": ":,"},
                        color_continuous_scale=SEQUENTIAL_SCALE, labels=_LABELS)
    fig.update_layout(coloraxis_colorbar=dict(title="Births", tickformat=","))
    return _finish(fig, "Births by state of residence (counts, not rates)", 460)


def state_month_heatmap(matrix: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Heatmap(
        z=matrix.values, x=[str(m) for m in matrix.columns], y=list(matrix.index),
        colorscale=SEQUENTIAL_SCALE, colorbar=dict(title="Births", tickformat=","),
        hovertemplate="%{y} · %{x}<br>Births: %{z:,}<extra></extra>",
    ))
    fig.update_yaxes(autorange="reversed", title=None)  # largest state at the top
    fig.update_xaxes(title=None, side="top")
    return _finish(fig, "Births by state and month (states sorted by total)",
                   max(420, 18 * len(matrix) + 120))


def top_bottom_chart(tb: pd.DataFrame) -> go.Figure:
    """Highest vs. lowest geographies on a shared x axis so bar lengths compare honestly."""
    fig = px.bar(tb, x="births", y="state", orientation="h", facet_col="group",
                 labels=_LABELS, color_discrete_sequence=[PRIMARY_COLOR])
    fig.update_traces(hovertemplate="%{y}<br>Births: %{x:,}<extra></extra>")
    fig.update_yaxes(matches=None, showticklabels=True, title=None,
                     categoryorder="total ascending")
    fig.update_xaxes(rangemode="tozero", tickformat=",", title="Births")
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return _finish(fig, "Highest vs. lowest geographies (same scale)", 420)
