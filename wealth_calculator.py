from typing import Callable
from dataclasses import dataclass

@dataclass
class TaxManager:
    """
    Manages tax calculations for different locations.
    
    Parameters
    ----------
    tax_location : str
        Identifier for the tax location
    income_tax_rate_calculator : Callable
        Function that takes income amount and returns effective tax rate
    capital_gains_tax_rate_calculator : Callable
        Function that takes capital gains amount and returns effective tax rate
    """
    tax_location: str
    income_tax_rate_calculator: Callable[[float], float]
    capital_gains_tax_rate_calculator: Callable[[float], float]
    
    def get_income_tax_rate(self, income: float) -> float:
        """Calculate effective income tax rate based on total income."""
        return self.income_tax_rate_calculator(income)
    
    def get_capital_gains_tax_rate(self, gains: float) -> float:
        """Calculate effective capital gains tax rate based on gains amount."""
        return self.capital_gains_tax_rate_calculator(gains)

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
    net_worth_penalty : float, optional
        Amount to subtract from net worth (e.g., repayment of relocation bonus)
    """
    company: str
    title: str
    salary: float
    tax_manager: TaxManager
    bonus: float = 0.0
    retirement_match_percentage: float = 0.0
    rsu_grant: float = 0.0
    net_worth_penalty: float = 0.0

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
    
    def __init__(self, initial_wealth: float = 0, year: int = 0):
        self.current_wealth = initial_wealth
        self.year = year
        self.yearly_history: list[dict] = []
    
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
        total_income = comp.salary + comp.bonus
        
        # Get effective tax rates from tax manager
        income_tax_rate = comp.tax_manager.get_income_tax_rate(total_income)
        capital_gains_tax_rate = comp.tax_manager.get_capital_gains_tax_rate(comp.rsu_grant)
        
        # Calculate after-tax amounts
        net_salary = comp.salary * (1 - income_tax_rate)
        net_bonus = comp.bonus * (1 - income_tax_rate)
        net_rsus = comp.rsu_grant * (1 - capital_gains_tax_rate)
        net_retirement_match = comp.salary * comp.retirement_match_percentage
        
        # Calculate total tax burden
        total_tax_burden = (
            (comp.salary + comp.bonus) * income_tax_rate +
            comp.rsu_grant * capital_gains_tax_rate
        )
        
        # Update wealth
        net_change = net_salary + net_bonus + net_rsus + net_retirement_match - comp.net_worth_penalty
        self.current_wealth += net_change
        
        # Record history
        year_details = {
            "year": self.year,
            "compensation_package": comp,
            "net_salary": net_salary,
            "net_bonus": net_bonus,
            "net_rsus": net_rsus,
            "net_retirement_match": net_retirement_match,
            "total_tax_burden": total_tax_burden,
            "net_worth_penalty": comp.net_worth_penalty,
            "net_change": net_change,
            "total_wealth": self.current_wealth,
            "effective_income_tax_rate": income_tax_rate,
            "effective_capital_gains_tax_rate": capital_gains_tax_rate
        }
        self.yearly_history.append(year_details)
        
        self.year += 1
        return self.current_wealth