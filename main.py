from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from wiser_funding_app.calculation import z_score_calculate
from wiser_funding_app import schemas, models, crud
from wiser_funding_app.database import SessionLocal,engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"Data": "Please Check Docs for more information"}


@app.get("/company/reports/{country_iso}/{id}/")
def reports(country_iso:str, id:int, minyear : Optional[int] = 0, maxyear: Optional[int] =9999 ,db:Session= Depends(get_db)):
    company_id = country_iso+str(id)
    return crud.get_reports(db, company_id, minyear=minyear, maxyear=maxyear)


@app.post("/company/reports/{country_iso}/{id}/")
def save_report(country_iso:str, id:int, financial_report: schemas.YearlyFinancial, db:Session = Depends(get_db)):
    company_id = country_iso+str(id)
    crud.add_report(db, financial_report, company_id)
    return {'Data' : 'Commit successful'}


@app.put("/company/{country_iso}/{company_id}", description='Expects a 5 year financial history and calculates z scores')
def z_scorer(country_iso: str, company_id: int, financials: schemas.FinancialInfo):
    #print('Gonna calculate')
    z_scores = z_score_calculate(the_data=financials)

    if len(z_scores['scores']) != 5:
        raise HTTPException(status_code=400, detail="Bad Input received check values")
    else:
        return z_scores


# uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=800)
