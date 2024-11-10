import pandas as pd
from dataclasses import dataclass

@dataclass
class TaxBracket:
    """
    Represents a single tax bracket.
    
    Attributes
    ----------
    upper_limit : float
        The upper income limit for the bracket.
    rate : float
        The tax rate for the bracket as a decimal.
    """
    upper_limit: float
    rate: float

# NewType
TaxSchedule = list[TaxBracket]
    
@dataclass
class TaxManager:
    """
    Manages tax calculations for different locations.
    
    Attributes
    ----------
    tax_location : str
        Identifier for the tax location.
    income_tax_schedules : list[TaxSchedule]
        List of tax schedules (lists of tax brackets) for calculating income tax rates.
    """
    tax_location: str
    income_tax_schedules: list[TaxSchedule]

    @staticmethod
    def get_effective_tax_rate(income: float, tax_schedule: TaxSchedule) -> float:
        """
        Calculate effective tax rate based on given income and tax brackets.
        
        Parameters
        ----------
        income : float
            The income amount to calculate the tax rate for.
        tax_schedule : TaxSchedule
            A list of TaxBracket objects for calculating the tax.

        Returns
        -------
        float
            The effective tax rate as a decimal.
        """
        total_tax = 0.0
        prev_bracket_limit = 0.0
        remaining_income = income
        
        for bracket in tax_schedule:
            taxable_in_bracket = min(remaining_income, bracket.upper_limit - prev_bracket_limit)
            if taxable_in_bracket <= 0:
                break
            total_tax += taxable_in_bracket * bracket.rate
            remaining_income -= taxable_in_bracket
            prev_bracket_limit = bracket.upper_limit
        
        return total_tax / income if income > 0 else 0.0
    
    def get_income_tax_rate(self, income: float) -> float:
        """
        Calculate effective income tax rate based on income and income tax brackets.
        
        Parameters
        ----------
        income : float
            The income amount to calculate the income tax rate for.

        Returns
        -------
        float
            The effective income tax rate as a decimal.
        """
        effective_tax_rate = 0
        
        for tax_schedule in self.income_tax_schedules:
            effective_tax_rate += self.get_effective_tax_rate(income=income, tax_schedule=tax_schedule)
        
        return effective_tax_rate
    
@dataclass
class CompensationPackage:
    """
    Represents a single year's compensation package.
    
    Parameters
    ----------
    company : str
        The name of the company
    title : str
        The name of the role
    salary : float
        Base annual salary
    tax_manager : TaxManager
        Manager for calculating location-specific taxes
    bonus : float, optional
        Annual bonus amount
    retirement_match_percentage : float, optional
        Annual percentage of salary matched by employer as a decimal (ie, 0.07 for 7%). The default is 0.
    rsu_grant : float, optional
        RSU grant for this year, if any
    income_adjustment : float, optional
        Amount added to net worth. Can be negative to simulate a penalty (e.g., repayment of relocation bonus)
    comment : str, optional
        A comment. Does nothing otherwise. 
    """
    company: str
    title: str
    salary: float
    tax_manager: TaxManager
    bonus: float = 0.0
    retirement_match_percentage: float = 0.0
    rsu_grant: float = 0.0
    income_adjustment: float = 0.0
    comment: str | None = None
    
    def to_dict(self) -> dict:
        """
        Convert the compensation package to a dictionary suitable for DataFrame conversion,
        replacing the tax manager with the effective tax rate.

        Returns
        -------
        dict
            A dictionary representing the compensation package.
        """
        # Calculate the effective tax rate based on salary and bonus
        gross_income = self.salary + self.bonus + self.rsu_grant
        effective_tax_rate = self.tax_manager.get_income_tax_rate(gross_income)

        # Compile data into a dictionary
        return {
            "Company": self.company,
            "Title": self.title,
            "Location": self.tax_manager.tax_location,
            "Salary": self.salary,
            "Bonus": self.bonus,
            "Retirement Match %": self.retirement_match_percentage,
            "RSU Grant": self.rsu_grant,
            "Effective Tax Rate": effective_tax_rate,
            "Income Adjustment": self.income_adjustment,
            "Comment": self.comment
        }

class WealthCalculator:
    """
    Simulates wealth accumulation with location-aware tax calculations.
    
    Parameters
    ----------
    initial_wealth : float, optional
        Starting wealth amount, default 0
    year : int, optional
        Starting year, default 0
    """
    
    def __init__(self, initial_wealth: float = 0, year: int = 0, assumed_real_market_growth: float = 0.07):
        self.current_wealth = initial_wealth
        self.year = year
        self.annual_history: dict[int, dict] = {}
        self.compensation_history: dict[int, dict] = {}
        self.assumed_real_market_growth = assumed_real_market_growth
    
    def simulate_year(
        self,
        comp: CompensationPackage,
    ) -> float:
        """
        Simulate one year with given compensation package.
        
        Parameters
        ----------
        comp : CompensationPackage
            Compensation package for this year including tax manager
            
        Returns
        -------
        float
            Updated total wealth
        """
        # Calculate total income for tax purposes
        gross_income = comp.salary + comp.bonus + comp.rsu_grant
        
        # Get effective tax rates from tax manager
        income_tax_rate = comp.tax_manager.get_income_tax_rate(gross_income)
        
        # Calculate after-tax amounts
        net_salary = comp.salary * (1 - income_tax_rate)
        net_bonus = comp.bonus * (1 - income_tax_rate)
        net_rsus = comp.rsu_grant * (1 - income_tax_rate)
        retirement_match = comp.salary * comp.retirement_match_percentage
        
        # Calculate total tax burden
        total_tax_burden = (gross_income) * income_tax_rate 
        
        # Update wealth
        net_income = net_salary + net_bonus + net_rsus + retirement_match + comp.income_adjustment
        unrealized_investment_gain = self.current_wealth * self.assumed_real_market_growth
        self.current_wealth += unrealized_investment_gain
        self.current_wealth += net_income
        
        # Get the compensation package details
        comp_details = comp.to_dict()
        
        # Combine all details into a single record
        year_details = {
            # Compensation package details
            "Company": comp_details["Company"],
            "Title": comp_details["Title"],
            "Location": comp_details["Location"],
            "Comment": comp_details["Comment"],
            
            # Gross amounts
            "Gross Salary": comp.salary,
            "Gross Bonus": comp.bonus,
            "Gross RSUs": comp.rsu_grant,
            "Retirement Match %": comp.retirement_match_percentage,
            "Gross Income": gross_income,
            
            # Tax details
            "Effective Tax Rate": income_tax_rate,
            "Total Tax Burden": total_tax_burden,
            
            # Net amounts
            "Net Salary": net_salary,
            "Net Bonus": net_bonus,
            "Net RSUs": net_rsus,
            "Retirement Match": retirement_match,
            "Income Adjustment": comp.income_adjustment,
            "Net Income": net_income,
            
            # Investment and wealth
            "Unrealized Investment Gain": unrealized_investment_gain,
            "Total Earned Wealth": self.current_wealth,
        }
        self.annual_history[self.year] = year_details
        
        # Store this just for posterity... idk
        self.compensation_history[self.year] = comp_details
        
        self.year += 1
        
        return self.current_wealth
    
    def get_compensation_history_df(self) -> pd.DataFrame:
        """
        Return the compensation history as a DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame of the compensation history with each year's details.
        """
        return pd.DataFrame.from_dict(self.compensation_history, orient="index")
    
    def get_worth_history_df(self) -> pd.DataFrame:
        """
        Return the net worth history as a DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame of the net worth history with each year's details.
        """
        
        return pd.DataFrame.from_dict(self.annual_history, orient="index")