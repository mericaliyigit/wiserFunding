from pydantic import BaseModel, validator, conlist, conint, confloat


class YearlyFinancial(BaseModel):
    year: conint(gt=0)
    ebit: confloat(gt=0)
    equity: confloat(gt=0)
    retained_earnings: confloat(gt=0)
    sales: confloat(gt=0)
    total_assets: confloat(gt=0)
    total_liabilities: confloat(gt=0)


class FinancialInfo(BaseModel):
    financials: conlist(YearlyFinancial, min_items=5, max_items=5)


class Score:
    year: conint(gt=0)
    zscore: float


class Scores:
    scores: conlist(Score,min_items=5,max_items=5)


class Example(BaseModel):
    year: int
    must_string: str