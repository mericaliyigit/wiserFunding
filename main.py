import uvicorn
from fastapi import FastAPI, HTTPException
from wiser_funding_app.calculation import z_score_calculate
from wiser_funding_app import schemas
app = FastAPI()


@app.get("/")
def home():
    return {"Data": "Check docs"}


@app.get("/company/{country_iso}/{id}")
def information(country_iso: str, id: int):
    return {'iso': country_iso, 'id': id}


@app.put("/company/{country_iso/{company_id}}", description='Expects a 5 year financial history and calculates z scores')
def z_scorer(country_iso: str, company_id: int, financials: schemas.FinancialInfo):
    print('Gonna calculate')
    z_scores = z_score_calculate(the_data=financials)

    if len(z_scores) != 5:
        raise HTTPException(status_code=400, detail="Bad Input received check values")
    else:
        return z_scores


@app.put('/test2')
def test2(financials: schemas.FinancialInfo):
    z_score_calculate(financials)


@app.put('/test')
def test(example: schemas.Example):
    print(example)
    return example


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=800)
