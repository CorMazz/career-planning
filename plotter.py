import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def round_to_nearest_thousand(series: pd.Series) -> pd.Series:
    return (series / 1000).round().astype(int)


def plot_total_wealth_progression(df: pd.DataFrame) -> go.Figure:
    """
    Creates a line chart showing total wealth progression over time for each career path.
    
    Args:
        df (pd.DataFrame): DataFrame containing wealth progression data
    
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    # Get unique career paths
    career_paths = df.index.get_level_values('Career Path').unique()
    
    # Add line for each career path
    for path in career_paths:
        path_data = df.xs(path, level='Career Path')
        fig.add_trace(
            go.Scatter(
                x=path_data.index,
                y=round_to_nearest_thousand(path_data['Total Earned Wealth']),
                name=path,
                mode='lines+markers',
                hovertemplate= "<b>%{data.name}</b><br>"
                            "Total Wealth: $%{y:,.0f}K<br>" +
                             "<extra></extra>"
            )
        )
    
    fig.update_layout(
        title="Total Wealth Progression by Career Path",
        hovermode='x',
        plot_bgcolor='white',
        yaxis=dict(
            title="Total Wealth ($)",
            tickprefix="$",
            ticksuffix="K",
            tickformat=",.0f",
            gridcolor='lightgrey',
            showgrid=True,
        ),
        xaxis=dict(
            title="Year",
            gridcolor='lightgrey',
            showgrid=True,
            dtick=1,
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.9)",  # Semi-transparent white background
            bordercolor="rgba(0, 0, 0, 0.3)",    # Light border
            borderwidth=1,
            font=dict(size=14),                  # Reduce font size if needed
            itemsizing='constant',               # Makes legend items consistent size
            itemwidth=30,                        # Adjust width of legend items
            tracegroupgap=0                      # Reduces gap between legend groups
        )
    )
    
    return fig

def plot_annual_compensation(df: pd.DataFrame) -> go.Figure:
    """
    Creates a stacked bar chart showing compensation breakdown by year,
    with career paths side by side within each year.
    """
    fig = go.Figure()
    
    # Get unique years and career paths
    years = sorted(df.index.get_level_values('Year').unique())
    career_paths = df.index.get_level_values('Career Path').unique()
    n_paths = len(career_paths)
    
    # Adjust spacing based on number of paths
    total_width_per_year = 0.8  # Leave some space between years
    bar_width = total_width_per_year / (n_paths + 1)  # Add 1 for some padding
    spacing = bar_width * 0.2  # 20% of bar width for spacing
    
    # Colors for components
    colors = {
        'Net Salary': 'rgb(66, 133, 244)',      # Blue
        'Net Bonus': 'rgb(52, 168, 83)',        # Green
        'Net RSUs': 'rgb(251, 188, 4)',         # Yellow
        'Retirement Match': 'rgb(234, 67, 53)',  # Red
        'Income Adjustment': 'rgb(156, 39, 176)' # Purple
    }
    
    # Add career path labels
    for year in years:
        for i, path in enumerate(career_paths):
            # Center the group of bars for each year
            x_pos = year + (i - (n_paths-1)/2) * (bar_width + spacing)
            
            fig.add_annotation(
                x=x_pos,
                y=-58,
                text=path,
                showarrow=False,
                textangle=-65,
                font=dict(size=14),  # Reduced font size
                xanchor='right',
                yanchor='top'
            )
    
    # Create bars for each career path
    for i, path in enumerate(career_paths):
        path_data = df.xs(path, level='Career Path')
        # Center the group of bars for each year
        x_positions = [year + (i - (n_paths-1)/2) * (bar_width + spacing) for year in years]
        
        components = ['Net Salary', 'Net Bonus', 'Net RSUs', "Retirement Match", "Income Adjustment"]
        
        base_hover_template = (
            f"<b>Career Path: {path}</b><br>" +
            "Year: %{x:.0f}<br>" +
            "<b>%{customdata[0]}: $%{y:,.0f}K</b><br>" +
            "Net Income: $%{customdata[1]:,.0f}K<br>" +
            "<extra></extra>"
        )
        
        # Add compensation components
        for component in components:
            fig.add_trace(go.Bar(
                name=component if i == 0 else f"{component} - {path}",
                x=x_positions,
                y=round_to_nearest_thousand(path_data[component]),
                width=bar_width,
                marker_color=colors[component],
                legendgroup=component,
                showlegend=i == 0,
                customdata=[[component, row] for row in round_to_nearest_thousand(path_data['Net Income'])],
                hovertemplate=base_hover_template
            ))

        # Add net income markers
        fig.add_trace(go.Scatter(
            name='Net Income' if i == 0 else f"Net Income - {path}",
            x=x_positions,
            y=round_to_nearest_thousand(path_data['Net Income']),
            mode='markers',
            marker=dict(
                symbol='star',
                size=14,  # Slightly reduced size
                color='black',
                line=dict(color='white', width=1)
            ),
            legendgroup='Net Income',
            showlegend=i == 0,
            hovertemplate=(
                f"<b>Career Path: {path}</b><br>" +
                "Year: %{x:.0f}<br>" +
                "Net Income: $%{y:,.0f}K<br>" +
                "<extra></extra>"
            )
        ))

    # Update layout
    fig.update_layout(
        title="Annual Compensation Breakdown by Career Path",
        xaxis=dict(
            side="top",
            tickmode='array',
            ticktext=years,
            tickvals=years,
            gridcolor='lightgrey',
            showgrid=True,
            tickfont=dict(size=16),
        ),
        yaxis=dict(
            tickfont=dict(size=16),
            titlefont=dict(size=16),
            title="Amount ($)",
            tickprefix="$",
            ticksuffix="K",
            tickformat=",.0f",
            range=(-59, 210),
            gridcolor='lightgrey',
            showgrid=True,
            tick0=0,
            dtick=30,
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2,
        ),
        barmode='relative',
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            xanchor='center',
            x=0.5,
            traceorder='normal'
        ),
        width=1700,
        height=1000,
        margin=dict(b=150)
    )
    
    return fig

def plot_tax_burden_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Creates a heatmap showing effective tax rates across years and career paths.
    
    Args:
        df (pd.DataFrame): DataFrame containing tax data
    
    Returns:
        go.Figure: Plotly figure object
    """
    # Pivot the data for the heatmap
    tax_data = df.pivot_table(
        index='Year',
        columns='Career Path',
        values='Effective Tax Rate'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=tax_data.values * 100,  # Convert to percentage
        x=tax_data.columns,
        y=tax_data.index,
        colorscale='RdYlBu_r',
        zmin=20,
        zmax=35,
        hoverongaps=False,
        hovertemplate="Year: %{y}<br>" +
                     "Career Path: %{x}<br>" +
                     "Tax Rate: %{z:.1f}%<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        title="Effective Tax Rates by Career Path",
        xaxis_title="Career Path",
        yaxis_title="Year",
        xaxis_tickangle=-45
    )
    
    return fig

def plot_comprehensive_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Creates a multi-panel figure comparing various metrics across career paths.
    
    Args:
        df (pd.DataFrame): DataFrame containing career path data
    
    Returns:
        go.Figure: Plotly figure object
    """
    career_paths = df.index.get_level_values('Career Path').unique()
    years = df.index.get_level_values('Year').unique()
    
    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Total Wealth Progression",
            "Net Income Comparison",
            "Effective Tax Rates",
            "Total Compensation Mix"
        )
    )
    
    # Plot 1: Total Wealth Progression
    for path in career_paths:
        path_data = df.xs(path, level='Career Path')
        fig.add_trace(
            go.Scatter(
                x=path_data.index,
                y=path_data['Total Earned Wealth'],
                name=f"{path} - Wealth",
                mode='lines+markers',
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Plot 2: Net Income Comparison
    for path in career_paths:
        path_data = df.xs(path, level='Career Path')
        fig.add_trace(
            go.Scatter(
                x=path_data.index,
                y=path_data['Net Income'],
                name=f"{path} - Income",
                mode='lines+markers',
                showlegend=True
            ),
            row=1, col=2
        )
    
    # Plot 3: Tax Rates
    for path in career_paths:
        path_data = df.xs(path, level='Career Path')
        fig.add_trace(
            go.Scatter(
                x=path_data.index,
                y=path_data['Effective Tax Rate'] * 100,
                name=f"{path} - Tax",
                mode='lines+markers',
                showlegend=True
            ),
            row=2, col=1
        )
    
    # Plot 4: Compensation Mix (Last Year)
    last_year = years[-1]
    comp_data = df.xs(last_year, level='Year')
    
    fig.add_trace(
        go.Bar(
            x=comp_data.index,
            y=comp_data['Net Salary'],
            name='Net Salary',
            showlegend=True
        ),
        row=2, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=comp_data.index,
            y=comp_data['Net Bonus'],
            name='Net Bonus',
            showlegend=True
        ),
        row=2, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=comp_data.index,
            y=comp_data['Net RSUs'],
            name='Net RSUs',
            showlegend=True
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=1000,
        width=1200,
        title_text="Comprehensive Career Path Comparison",
        showlegend=True,
        barmode='stack',
    )
    
    # Update axes labels and formatting
    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_xaxes(title_text="Year", row=1, col=2)
    fig.update_xaxes(title_text="Year", row=2, col=1)
    fig.update_xaxes(title_text="Career Path", row=2, col=2)
    
    fig.update_yaxes(title_text="Total Wealth ($)", tickprefix="$", tickformat=",", row=1, col=1)
    fig.update_yaxes(title_text="Net Income ($)", tickprefix="$", tickformat=",", row=1, col=2)
    fig.update_yaxes(title_text="Tax Rate (%)", ticksuffix="%", row=2, col=1)
    fig.update_yaxes(title_text="Amount ($)", tickprefix="$", tickformat=",", row=2, col=2)
    
    return fig

# Example usage:
if __name__ == "__main__":
    # Individual plots
    wealth_fig = plot_total_wealth_progression(df)
    comp_fig = plot_annual_compensation(df)
    tax_fig = plot_tax_burden_comparison(df)
    
    # Comprehensive comparison
    comp_fig = plot_comprehensive_comparison(df)
    
    # Display in notebook
    wealth_fig.show()
    comp_fig.show()
    tax_fig.show()
    comp_fig.show()