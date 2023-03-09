from numpy_financial import irr
import math

def returns(
    years,
    initial_output_pa,
    self_use,
    inflation,
    sell_price,
    initial_buy_price,
    module_decay,
    ):
    """Generates returns for each month in the given number of years.

    Args:
        years: Number of years to calculate.
        inital_output_pa: Output / year in kWh in the first year.
        self_use: Fraction of output consumed by user, the rest is sold.
        inflration: Inflation rate, e.g. 0.02.
        sell_price: Sell price  / kWh in EUR, e.g. 0.082.
        initial_buy_price: Initial price / kWh to buy energy, e.g. 0.3.
        module_decay: Module effectiveness at the end of the period, e.g. 0.8.
    """
    for month in range(0, 12*years):
        decay = (1 - month*(1-module_decay)/(12*years))
        output = (initial_output_pa/12) * decay
        buy_price = initial_buy_price * math.pow(1+inflation/12, month) 
        saved = output * self_use * buy_price
        sold = output * (1-self_use) * sell_price
        yield saved + sold

def cashflow(
    price,
    returns,
    ):
    """Generates a cashflow for a PV investment.
    
    Args:
        price: Price of the installation (positive).
        returns: Generator for the returns in the examined period.
    """
    yield -price
    for r in returns:
        yield r

def currentvalue(
    rate,
    returns
):
    value = 0
    for m, r in enumerate(returns):
        value += r / math.pow(1 + rate/12, m)
    return value

def genreturns():
    return returns(
        years = 25,
        initial_output_pa = 900,
        self_use = 0.25,
        inflation = 0.02,
        sell_price = 0.082,
        initial_buy_price=0.3,
        module_decay = 0.8,
    )

def gencashflow():
    return cashflow(
        1600,
        genreturns(),
    )

print(12*irr(list(gencashflow())))

print(currentvalue(0.06, genreturns()))