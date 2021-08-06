from sqlalchemy.orm import Session

from wiser_funding_app.models import FinancialReport, Company
from wiser_funding_app.schemas import YearlyFinancial


def add_report(db:Session, report:YearlyFinancial, company_id:str):

    the_company = db.query(Company).filter(Company.company_id == company_id).first()
    print('AA')
    old_report = db.query(FinancialReport).filter(FinancialReport.company_id == company_id).filter(FinancialReport.year == report.year).first()

    if not the_company:
        add_company(db, company_id)
        print('Company didnt exist created a new one')

    if not old_report:
        report = FinancialReport(company_id=company_id,
                                 year=report.year,
                                 ebit=report.ebit,
                                 equity=report.equity,
                                 retained_earnings=report.retained_earnings,
                                 sales=report.sales,
                                 total_assets=report.total_assets,
                                 total_liabilities=report.total_liabilities)
        db.add(report)
        db.commit()
        print('Created new report')
    else:
        old_report.ebit = report.ebit
        old_report.equity = report.equity
        old_report.retained_earnings = report.retained_earnings
        old_report.sales = report.sales
        old_report.total_assets = report.total_assets
        old_report.total_liabilities = report.total_liabilities
        db.commit()
        print('Existing row updated')


    print('Done')


def add_company(db:Session, company_id:str):
    company = Company(company_id=company_id)
    db.add(company)
    db.commit()
    print('Done')


def get_reports(db:Session, company_id:str, minyear:int, maxyear:int):

    reports = db.query(FinancialReport).filter(FinancialReport.company_id == company_id).filter(FinancialReport.year.between(minyear, maxyear)).all()
    financials = {'financials': reports}
    return financials