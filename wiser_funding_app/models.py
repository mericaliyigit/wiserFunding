from sqlalchemy import Column, ForeignKey, String, Integer, Float, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relation, relationship

from wiser_funding_app.database import Base


class Company(Base):
    __tablename__ = 'company'
    company_id = Column(String, primary_key=True, unique=True, nullable=False)
    financial_reports = relationship(lambda:FinancialReport)


class FinancialReport(Base):
    __tablename__ ='financial_report'
    __table_args__ = (
        PrimaryKeyConstraint('company_id', 'year'),
    )
    company_id = Column(String, ForeignKey(Company.company_id), nullable=False)
    year = Column(Integer, nullable=False)
    ebit = Column(Float, nullable=False)
    equity = Column(Float, nullable=False)
    retained_earnings = Column(Float, nullable=False)
    sales = Column(Float, nullable=False)
    total_assets = Column(Float, nullable=False)
    total_liabilities = Column(Float, nullable=False)
