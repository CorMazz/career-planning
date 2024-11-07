from wealth_calculator import WealthCalculator, CompensationPackage, TaxManager
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid, Tab, Page, Timeline
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.globals import ThemeType
import pandas as pd


#########################################################################################################################################
#########################################################################################################################################
# Dashboard Function
#########################################################################################################################################
#########################################################################################################################################

def create_career_dashboard(career_path_results):
    """Create dashboard with fixed formatting and working plots."""
    # Prepare data
    data = []
    for path_name, calculator in career_path_results.items():
        for hist in calculator.yearly_history:
            data.append({
                'Career Path': path_name,
                'Year': hist['year'],
                'Total Wealth': float(hist['total_wealth']),
                'Net Salary': float(hist['net_salary']),
                'Net Bonus': float(hist['net_bonus']),
                'Net RSUs': float(hist['net_rsus']),
                'Net Retirement Match': float(hist['net_retirement_match']),
                'Net Worth Penalty': float(-hist['net_worth_penalty'])  # Made negative for visual display
            })
    
    df = pd.DataFrame(data)
    years = sorted(df['Year'].unique().tolist())
    career_paths = df['Career Path'].unique().tolist()
    
    # 1. Total Wealth Growth chart remains the same
    wealth_line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1200px", height="600px"))
        .add_xaxis(years)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Total Wealth Growth",
                pos_left="center",
                padding=[10, 0, 0, 0]
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(
                pos_right="5%",
                feature={
                    "saveAsImage": {},
                    "restore": {},
                    "dataView": {},
                }
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                name="Year",
                name_location="center",
                name_gap=35,
                boundary_gap=False
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="Total Wealth ($)",
                name_location="center",
                name_gap=50,
                axislabel_opts=opts.LabelOpts(
                    formatter=JsCode(
                        "function(value) {return '$' + (value/1000).toFixed(0) + 'K';}"
                    )
                )
            ),
            legend_opts=opts.LegendOpts(
                type_="scroll",
                pos_bottom="0%",
                pos_left="center",
                orient="horizontal"
            )
        )
    )
    
    # Add each career path to wealth line chart
    for path in career_paths:
        path_data = df[df['Career Path'] == path]
        wealth_values = path_data['Total Wealth'].tolist()
        wealth_line.add_yaxis(
            series_name=path,
            y_axis=wealth_values,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=8,
            linestyle_opts=opts.LineStyleOpts(width=3)
        )
    
    # 2. Updated Compensation Breakdown with Net Worth Penalty
    comp_bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1200px", height="600px"))
        .add_xaxis(years)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Annual Compensation Breakdown by Career Path",
                pos_left="center",
                padding=[10, 0, 0, 0]
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter=JsCode(
                    """function(params) {
                        let value = params.value;
                        let formattedValue = Math.abs(value).toLocaleString();
                        if (params.seriesName === 'Net Worth Penalty') {
                            formattedValue = '-$' + formattedValue;
                        } else {
                            formattedValue = '$' + formattedValue;
                        }
                        return params.data.career_path + '<br/>' +
                               'Year: ' + params.name + '<br/>' +
                               params.seriesName + ': ' + formattedValue;
                    }"""
                )
            ),
            xaxis_opts=opts.AxisOpts(
                name="Year",
                name_location="center",
                name_gap=35
            ),
            yaxis_opts=opts.AxisOpts(
                name="Amount ($)",
                name_location="center",
                name_gap=50,
                axislabel_opts=opts.LabelOpts(
                    formatter=JsCode(
                        "function(value) {return '$' + (value/1000).toFixed(0) + 'K';}"
                    )
                )
            ),
            legend_opts=opts.LegendOpts(
                is_show=True,
                type_="scroll",
                pos_bottom="0%",
                pos_left="center",
                orient="horizontal"
            )
        )
    )
    
    # Updated compensation components with Net Worth Penalty
    comp_types = {
        'Net Salary': '#4B69FF',
        'Net Bonus': '#50C878',
        'Net RSUs': '#FFD700',
        'Net Retirement Match': '#FF6B6B',
        'Net Worth Penalty': '#FF0000'  # Red color for penalties
    }
    
    # Add bars for each career path with stacked components
    for path in career_paths:
        path_data = df[df['Career Path'] == path]
        for comp_type, color in comp_types.items():
            comp_bar.add_yaxis(
                series_name=f"{comp_type}",
                y_axis=[dict(value=val, career_path=path) for val in path_data[comp_type].tolist()],
                stack=path,
                category_gap="50%",
                gap="20%",
                label_opts=opts.LabelOpts(is_show=False),
                itemstyle_opts=opts.ItemStyleOpts(color=color),
            )
    
    # Create page with fixed-width charts
    page = Page(layout=Page.SimplePageLayout)
    page.add(wealth_line, comp_bar)
    
    return page

#########################################################################################################################################
#########################################################################################################################################
# Tax Management
#########################################################################################################################################
#########################################################################################################################################

def get_federal_tax_rate(income):
    """Calculate effective federal tax rate based on 2024 tax brackets"""
    brackets = [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (609350, 0.35),
        (float('inf'), 0.37)
    ]
    
    total_tax = 0
    prev_bracket = 0
    remaining_income = income
    
    for bracket, rate in brackets:
        taxable_in_bracket = min(remaining_income, bracket - prev_bracket)
        if taxable_in_bracket <= 0:
            break
        total_tax += taxable_in_bracket * rate
        remaining_income -= taxable_in_bracket
        prev_bracket = bracket
    
    return total_tax / income if income > 0 else 0

def get_sc_state_tax_rate(income):
    """Calculate effective SC state tax rate based on 2024 brackets"""
    brackets = [
        (3200, 0.00),
        (6410, 0.03),
        (9620, 0.04),
        (12820, 0.05),
        (16040, 0.06),
        (float('inf'), 0.07)
    ]
    
    total_tax = 0
    prev_bracket = 0
    remaining_income = income
    
    for bracket, rate in brackets:
        taxable_in_bracket = min(remaining_income, bracket - prev_bracket)
        if taxable_in_bracket <= 0:
            break
        total_tax += taxable_in_bracket * rate
        remaining_income -= taxable_in_bracket
        prev_bracket = bracket
    
    return total_tax / income if income > 0 else 0

def get_ny_state_tax_rate(income):
    """Calculate effective NY state tax rate based on 2024 brackets"""
    brackets = [
        (8500, 0.04),
        (11700, 0.045),
        (13900, 0.0525),
        (80650, 0.055),
        (215400, 0.06),
        (1077550, 0.0685),
        (float('inf'), 0.0882)
    ]
    
    total_tax = 0
    prev_bracket = 0
    remaining_income = income
    
    for bracket, rate in brackets:
        taxable_in_bracket = min(remaining_income, bracket - prev_bracket)
        if taxable_in_bracket <= 0:
            break
        total_tax += taxable_in_bracket * rate
        remaining_income -= taxable_in_bracket
        prev_bracket = bracket
    
    return total_tax / income if income > 0 else 0

def get_nyc_local_tax_rate(income):
    """Calculate effective NYC local tax rate based on 2024 brackets"""
    brackets = [
        (12000, 0.0297),
        (25000, 0.0351),
        (50000, 0.0369),
        (float('inf'), 0.0396)
    ]
    
    total_tax = 0
    prev_bracket = 0
    remaining_income = income
    
    for bracket, rate in brackets:
        taxable_in_bracket = min(remaining_income, bracket - prev_bracket)
        if taxable_in_bracket <= 0:
            break
        total_tax += taxable_in_bracket * rate
        remaining_income -= taxable_in_bracket
        prev_bracket = bracket
    
    return total_tax / income if income > 0 else 0

def get_capital_gains_rate(income):
    """Calculate capital gains tax rate based on 2024 income thresholds"""
    if income <= 44625:  # Single filer threshold for 0% rate
        return 0.0
    elif income <= 492300:  # Single filer threshold for 15% rate
        return 0.15
    else:
        return 0.20

# Updated tax managers with more accurate calculations
tax_managers = {
    (tax_location := "sc"): TaxManager(
        tax_location=tax_location,
        income_tax_rate_calculator=lambda income: get_federal_tax_rate(income) + get_sc_state_tax_rate(income),
        capital_gains_tax_rate_calculator=lambda income: get_capital_gains_rate(income) + get_sc_state_tax_rate(income) * 0.5  # State taxes often apply at reduced rates to capital gains
    ),
    (tax_location := "ny"): TaxManager(
        tax_location=tax_location,
        income_tax_rate_calculator=lambda income: get_federal_tax_rate(income) + get_ny_state_tax_rate(income),
        capital_gains_tax_rate_calculator=lambda income: get_capital_gains_rate(income) + get_ny_state_tax_rate(income)
    ),
    (tax_location := "nyc"): TaxManager(
        tax_location=tax_location,
        income_tax_rate_calculator=lambda income: get_federal_tax_rate(income) + get_ny_state_tax_rate(income) + get_nyc_local_tax_rate(income),
        capital_gains_tax_rate_calculator=lambda income: get_capital_gains_rate(income) + get_ny_state_tax_rate(income) + get_nyc_local_tax_rate(income)
    ),
}

#########################################################################################################################################
#########################################################################################################################################
# Career Path Definitions
#########################################################################################################################################
#########################################################################################################################################

career_paths = {
    "GE in SC": [
        # 2025
        CompensationPackage(
            company="GE",
            title="PB Engineer",
            salary=(salary := 95000),
            bonus=salary * 0.05,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["sc"],
        ),
        # 2026
        CompensationPackage(
            company="GE",
            title="LPB Engineer",
            salary=(salary := 102000),
            bonus=salary * 0.10,
            rsu_grant=0,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["sc"],
        ),
        # 2027
        CompensationPackage(
            company="GE",
            title="LPB Engineer",
            salary=(salary := 105000),
            bonus=salary * 0.10,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["sc"],
        ),
        # 2028
        CompensationPackage(
            company="GE",
            title="LPB Engineer",
            salary=(salary := 108000),
            bonus=salary * 0.10,
            rsu_grant=0,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["sc"],
        ),
        # 2029
        CompensationPackage(
            company="GE",
            title="Senior Engineer",
            salary=(salary := 120000),
            bonus=salary * 0.15,
            rsu_grant=0,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["sc"],
        ),
    ],
    # Google salary info from level.fyi
    "GE LPB to Google in NYC": [
        # 2025
        CompensationPackage(
            company="GE",
            title="LPB Engineer",
            salary=(salary := 102000),
            bonus=salary * 0.10,
            rsu_grant=532 * 300 / 2, # 532 shares * 300 $ / share --> half vests at end of 2025
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["ny"],
        ),
        # 2026
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 150000),
            bonus=salary * 0.05 + 15000, # + Starting Bonus
            rsu_grant=33000,  
            retirement_match_percentage=0.07,
            net_worth_penalty=11000,
            tax_manager=tax_managers["nyc"],
        ),
        # 2027
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 153000),
            bonus=salary * 0.05,
            rsu_grant=33000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["nyc"],
        ),
        # 2028
        CompensationPackage(
            company="Google",
            title="SWE III",
            salary=(salary := 182000),
            bonus=salary * 0.10,
            rsu_grant=64000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["nyc"],
        ),
        # 2029
        CompensationPackage(
            company="Google",
            title="SWE III",
            salary=(salary := 186000),
            bonus=salary * 0.10,
            rsu_grant=64000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["nyc"],
        ),
    ],
    "Straight to Google in NYC": [
        # 2025
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 150000),
            bonus=salary * 0.05,
            rsu_grant=33000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["nyc"],
        ),
        # 2026
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 153000),
            bonus=salary * 0.05,
            rsu_grant=33000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["nyc"],
        ),
        # 2027
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 157000),
            bonus=salary * 0.05,
            rsu_grant=33000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["nyc"],
        ),
        # 2028
        CompensationPackage(
            company="Google",
            title="SWE III",
            salary=(salary := 182000),
            bonus=salary * 0.10,
            rsu_grant=64000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["nyc"],
        ),
        # 2029
        CompensationPackage(
            company="Google",
            title="SWE III",
            salary=(salary := 186000),
            bonus=salary * 0.10,
            rsu_grant=64000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["nyc"],
        ),
    ]
}

#########################################################################################################################################
#########################################################################################################################################
# Main
#########################################################################################################################################
#########################################################################################################################################

if __name__ == "__main__":

    career_path_results = {}
    for career_path_name, career_path_steps in career_paths.items():
        career_path_results[career_path_name] = wc = WealthCalculator(year=2025, initial_wealth=150000)
        for yearly_compensation_package in career_path_steps:
            wc.simulate_year(yearly_compensation_package)
        
    # Create and render the dashboard with pyecharts
    dashboard = create_career_dashboard(career_path_results)
    dashboard.render("career_dashboard.html")
        