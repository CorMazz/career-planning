from wealth_calculator import WealthCalculator, CompensationPackage, TaxManager, TaxBracket

#########################################################################################################################################
#########################################################################################################################################
# Tax Management
#########################################################################################################################################
#########################################################################################################################################

# Define tax brackets for each location using instances of TaxBracket
federal_brackets = [
    # https://taxfoundation.org/data/all/federal/2025-tax-brackets/
    TaxBracket(11925, 0.10),
    TaxBracket(48475, 0.12),
    TaxBracket(103350, 0.22),
    TaxBracket(197300, 0.24),
    TaxBracket(250525, 0.32),
    TaxBracket(626350, 0.35),
    TaxBracket(float('inf'), 0.37)
]

sc_brackets = [
    # https://taxfoundation.org/data/all/state/state-income-tax-rates-2024/
    TaxBracket(3460, 0.00),
    TaxBracket(17330, 0.03),
    TaxBracket(float('inf'), 0.064)
]

ny_brackets = [
    # https://taxfoundation.org/data/all/state/state-income-tax-rates-2024/
    TaxBracket(8500, 0.04),
    TaxBracket(11700, 0.045),
    TaxBracket(13900, 0.0525),
    TaxBracket(80650, 0.055),
    TaxBracket(215400, 0.06),
    TaxBracket(1_077_550, 0.0685),
    TaxBracket(5_000_000, 0.0965),
    TaxBracket(25_000_000, 0.103),
    TaxBracket(float('inf'), 0.109)
]

nyc_brackets = [
    TaxBracket(12000, 0.03078),
    TaxBracket(25000, 0.03762),
    TaxBracket(50000, 0.03819),
    TaxBracket(float('inf'), 0.0396)
]

# Define tax managers for each location using the new TaxManager class
tax_managers = {
    "SC": TaxManager(
        tax_location="SC",
        income_tax_schedules=[federal_brackets, sc_brackets]
    ),
    "NY": TaxManager(
        tax_location="NY",
        income_tax_schedules=[federal_brackets, ny_brackets]
    ),
    "NYC": TaxManager(
        tax_location="NYC",
        income_tax_schedules=[federal_brackets, ny_brackets, nyc_brackets]
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
            rsu_grant=532 * 300 / 2, # 532 shares * 300 $ / share --> half vests at end of 2025
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["SC"],
        ),
        # 2026
        CompensationPackage(
            company="GE",
            title="LPB Engineer",
            salary=(salary := 102000),
            bonus=salary * 0.10,
            rsu_grant=0,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["SC"],
        ),
        # 2027
        CompensationPackage(
            company="GE",
            title="LPB Engineer",
            salary=(salary := 105000),
            bonus=salary * 0.10,
            rsu_grant=532 * 300 / 2, # 532 shares * 300 $ / share --> half vests at end of 2025
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["SC"],
        ),
        # 2028
        CompensationPackage(
            company="GE",
            title="LPB Engineer",
            salary=(salary := 108000),
            bonus=salary * 0.10,
            rsu_grant=0,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["SC"],
        ),
        # 2029
        CompensationPackage(
            company="GE",
            title="Senior Engineer",
            salary=(salary := 120000),
            bonus=salary * 0.15,
            rsu_grant=0,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["SC"],
        ),
    ],    # Google salary info from level.fyi
        "Straight to Google in NYC": [
        # 2025
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 150000),
            bonus=salary * 0.05,
            rsu_grant=33000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-27000 - 24000,  # Grad school payment + 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for Grad School Repayment + NYC Housing"
        ),
        # 2026
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 153000),
            bonus=salary * 0.05,
            rsu_grant=33000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-24000,  # 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
        # 2027
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 157000),
            bonus=salary * 0.05,
            rsu_grant=33000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-24000,  # 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
        # 2028
        CompensationPackage(
            company="Google",
            title="SWE III",
            salary=(salary := 182000),
            bonus=salary * 0.10,
            rsu_grant=64000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-24000,  # 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
        # 2029
        CompensationPackage(
            company="Google",
            title="SWE III",
            salary=(salary := 186000),
            bonus=salary * 0.10,
            rsu_grant=64000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-24000,  # 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
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
            tax_manager=tax_managers["NY"],
            comment="NY taxes assuming remote work from Pok."
        ),
        # 2026
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 150000),
            bonus=salary * 0.05 + 15000, # + Starting Bonus
            rsu_grant=33000,  
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-15000 - 24000,  # Grad school payment + 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for Grad School Repayment + NYC Housing"
        ),
        # 2027
        CompensationPackage(
            company="Google",
            title="SWE II",
            salary=(salary := 153000),
            bonus=salary * 0.05,
            rsu_grant=33000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-24000,  # 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
        # 2028
        CompensationPackage(
            company="Google",
            title="SWE III",
            salary=(salary := 182000),
            bonus=salary * 0.10,
            rsu_grant=64000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],           
            income_adjustment=-24000,  # 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
        # 2029
        CompensationPackage(
            company="Google",
            title="SWE III",
            salary=(salary := 186000),
            bonus=salary * 0.10,
            rsu_grant=64000,
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-24000,  # 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
    ],
        "GE LPB to BCG in NYC": [
        # 2025
        CompensationPackage(
            company="GE",
            title="LPB Engineer",
            salary=(salary := 102000),
            bonus=salary * 0.10,
            rsu_grant=532 * 300 / 2, # 532 shares * 300 $ / share --> half vests at end of 2025
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NY"],
            comment="NY taxes assuming remote work from Pok."
        ),
        # 2026
        CompensationPackage(
            company="BCG",
            title="Associate",
            salary=(salary := 122000),
            bonus=salary * 0.06 + 10000, # + Starting Bonus  
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-15000 - 24000,  # Grad school payment + 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for Grad School Repayment + NYC Housing"
        ),
        # 2027
        CompensationPackage(
            company="BCG",
            title="Associate",
            salary=(salary := 125000),
            bonus=salary * 0.06, # + Starting Bonus  
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-24000,  # Grad school payment + 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
        # 2028
        CompensationPackage(
            company="BCG",
            title="Consultant",
            salary=(salary := 192000),
            bonus=salary * 0.10, # + Starting Bonus  
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-24000,  # Grad school payment + 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
        # 2029
        CompensationPackage(
            company="BCG",
            title="Consultant",
            salary=(salary := 192000),
            bonus=salary * 0.10, # + Starting Bonus  
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-24000,  # Grad school payment + 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
    ],
    # Datadog salary info from Tiago
    "GE LPB to Datadog Sales in NYC": [
        # 2025
        CompensationPackage(
            company="GE",
            title="LPB Engineer",
            salary=(salary := 102000),
            bonus=salary * 0.10,
            rsu_grant=532 * 300 / 2, # 532 shares * 300 $ / share --> half vests at end of 2025
            retirement_match_percentage=0.07,
            tax_manager=tax_managers["NY"],
            comment="NY taxes assuming remote work from Pok."
        ),
        # 2026
        CompensationPackage(
            company="Data Dog",
            title="Sales Engineer",
            salary=(salary := 100000),
            bonus=salary * 0.10 + 5000, # + Starting Bonus
            rsu_grant=15000,  
            retirement_match_percentage=0.02,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-15000 - 24000,  # Grad school payment + 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for Grad School Repayment + NYC Housing"
        ),
        # 2027
        CompensationPackage(
            company="Data Dog",
            title="Sales Engineer",
            salary=(salary := 100000),
            bonus=15000, # + Starting Bonus
            rsu_grant=15000 + 15000,  
            retirement_match_percentage=0.02,
            tax_manager=tax_managers["NYC"],
            income_adjustment=-15000 - 24000,  # Grad school payment + 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for Grad School Repayment + NYC Housing"
        ),
        # 2028
        CompensationPackage(
            company="Data Dog",
            title="Sales Engineer II",
            salary=(salary := 110000),
            bonus=15000,
            rsu_grant=15000+15000,
            retirement_match_percentage=0.02,
            tax_manager=tax_managers["NYC"],           
            income_adjustment=-24000,  # 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
        # 2029
        CompensationPackage(
            company="Data Dog",
            title="Sales Engineer III",
            salary=(salary := 120000),
            bonus=20000,
            rsu_grant=15000+15000+15000,
            retirement_match_percentage=0.02,
            tax_manager=tax_managers["NYC"],           
            income_adjustment=-24000,  # 2k/mo rent - 4k rent in GVL
            comment="Income Adjusted for NYC Housing"
        ),
    ],
}

#########################################################################################################################################
#########################################################################################################################################
# Main
#########################################################################################################################################
#########################################################################################################################################

def run_simulation():
    career_path_wealth_calculators = {}
    for career_path_name, career_path_steps in career_paths.items():
        career_path_wealth_calculators[career_path_name] = wc = WealthCalculator(year=2025, initial_wealth=150000)
        for yearly_compensation_package in career_path_steps:
            wc.simulate_year(yearly_compensation_package)
        
    career_path_net_worth_histories = {k: v.get_worth_history_df() for k, v in career_path_wealth_calculators.items()}
    career_path_compensation_histories = {k: v.get_compensation_history_df() for k, v in career_path_wealth_calculators.items()}
    
    return {
        "wealth_calculators": career_path_wealth_calculators, 
        "worth_histories": career_path_net_worth_histories, 
        "compensation_histories": career_path_compensation_histories
        }

if __name__ == "__main__":

    simulation_results = run_simulation()
