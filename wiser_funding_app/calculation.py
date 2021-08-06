from wiser_funding_app import schemas

COEFFICIENTS = {
    'x1': 1.2,
    'x2': 1.4,
    'x3': 3.3,
    'x4': 0.6,
    'x5': 1,
}


def z_score_calculate(the_data: schemas.FinancialInfo):
    z_scores = []
    for yearly_info in the_data.financials:
        # https://en.wikipedia.org/wiki/Working_capital
        working_capital = yearly_info.total_assets - yearly_info.total_liabilities
        try:
            x1 = working_capital / yearly_info.total_assets
            x2 = yearly_info.retained_earnings / yearly_info.total_assets
            x3 = yearly_info.ebit / yearly_info.total_assets
            x4 = yearly_info.equity / yearly_info.total_liabilities
            x5 = yearly_info.sales / yearly_info.total_assets

            z_score = x1 * COEFFICIENTS['x1'] + x2 * COEFFICIENTS['x2'] + x3 * COEFFICIENTS['x3'] +\
                      x4 * COEFFICIENTS['x4'] + x5 * COEFFICIENTS['x5']

            #print(z_score)

            z_scores.append({"year" : yearly_info.year,
                             "zscore" : z_score})
        except ArithmeticError as e:
            print(f'Error {e} , {e.__class__}')

    return {"scores" : z_scores}
