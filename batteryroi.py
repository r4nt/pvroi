from numpy_financial import irr
import math

def returns(
    years,
    contribution,
    inflation,
    sell_price,
    initial_buy_price,
    efficiency,
    battery_decay,
    ):
    """Generates returns for each month in the given number of years.

    Args:
        years: Number of years to calculate.
        contribution: Overall energy taken from battery per year in kWh.
        inflation: Inflation rate, e.g. 0.02.
        sell_price: Sell price  / kWh in EUR, e.g. 0.082.
        initial_buy_price: Initial price / kWh to buy energy, e.g. 0.3.
        initial_efficiency: Initial efficiency of the battery, e.g. 0.9.
        battery_decay: Rate at which contribution is lower after the examined
            period, e.g. 0.8.
    """
    for month in range(0, 12*years):
        decay = (1 - month*(1-battery_decay)/(12*years))
        buy_price = initial_buy_price * math.pow(1+inflation/12, month) 

        sell_less = (contribution * decay / 12) * sell_price
        buy_less = (contribution * decay / 12) * efficiency * buy_price

        yield buy_less - sell_less

def cashflow(
    price,
    returns,
    ):
    """Generates a cashflow for a battery investment.
    
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
        years = 15,
        contribution = 200, 
        inflation = 0.02,
        sell_price = 0.082,
        initial_buy_price=0.3,
        efficiency = 0.95,
        battery_decay = 0.8,
    )

def gencashflow():
    return cashflow(
        437,
        genreturns(),
    )

print(12*irr(list(gencashflow())))

print(currentvalue(0.06, genreturns()))