from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, time
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.models import User

class Trade(models.Model):
    loan_id = models.CharField(primary_key=True, max_length=255, unique=True)
    investment_date = models.DateField()
    maturity_date = models.DateField()
    interest_rate = models.FloatField()

    def __str__(self):
        return self.loan_id

    @property
    def invested_amount(self):
        funding_amount = self.cashflows.filter(cashflow_type="funding").aggregate(
            total_funding=Sum("amount")
        )["total_funding"]
        return abs(funding_amount) if funding_amount else 0

    def get_realized_amount(self, reference_date):
        realized_amount = self.cashflows.filter(
            cashflow_date__lte=reference_date, cashflow_type="repayment"
        ).aggregate(total_repayment=Sum("amount"))["total_repayment"]
        return realized_amount if realized_amount else 0

    def get_remaining_invested_amount(self, reference_date):
        return self.invested_amount - self.get_realized_amount(reference_date)

    def get_gross_expected_amount(self, reference_date):
        
        if isinstance(reference_date, str):
            reference_date = datetime.strptime(reference_date, "%Y-%m-%d").date()
        
        invested_amount = Decimal(str(self.invested_amount))

        daily_interest_rate = Decimal(self.interest_rate / 100 / 365)

        passed_days = (reference_date - self.investment_date).days

        gross_expected_interest_amount = (
            daily_interest_rate * Decimal(self.invested_amount) * passed_days
        )

        gross_expected_amount = invested_amount + gross_expected_interest_amount

        return gross_expected_amount
    
    #nket rast self osht loan_id
    def get_all_cashflows(self):
        cashflows = CashFlow.objects.filter(trade=self)
        return cashflows
    
    def get_closing_date(self):
        cashflows = self.get_all_cashflows()
        get_gross_expected_amount_at_maturity = self.get_gross_expected_amount(self.maturity_date)
    
        repayments = 0
        closing_date = None
    
        for cashflow in cashflows:
            if cashflow.cashflow_type == 'repayment':
                repayments += cashflow.amount
            
                if repayments >= get_gross_expected_amount_at_maturity:
                    closing_date = cashflow.cashflow_date
                    break
            
        if closing_date is not None:
            return closing_date
        else:
            return "The repayment is not closed yet!"
                
        
        
    
class CashFlow(models.Model):
    cashflow_id = models.CharField(primary_key=True, max_length=255)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="cashflows")
    cashflow_date = models.DateField()
    cashflow_currency = models.CharField(max_length=255)
    cashflow_type = models.CharField(max_length=255)
    amount = models.FloatField()

    def __str__(self):
        return self.cashflow_id
