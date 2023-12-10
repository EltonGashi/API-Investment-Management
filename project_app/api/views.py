from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from project_app.models import CashFlow, Trade
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db import transaction

from project_app.api.serializers import TradeSerializer, CashFlowSerializer
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView


from rest_framework.permissions import IsAuthenticated, IsAdminUser


class FileUpload(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]
    parser_classes = (MultiPartParser,)

    
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")

        if file:
            #this checks if the file is a csv or an excel so it knows how to read it as 
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                return JsonResponse(
                    {"detail": "Unsupported file format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            #iterates in rows , _ is used to ignore the index because the df.iterrows() iterates through index 
            #and rows so in our case we dont need the index and with _ we ignore it 
            for _, row in df.iterrows():
                loan_id = row['loan_id'] #gets the loan_id for the row we are iterating 

                
                #get_or_create() - used for avoiding duplicates 
                #if the object with that 'loan_id' exists, it retrieves it 
                #if not, it creates a new Trade object with the provided 'loan_id'
                trade_instance, _ = Trade.objects.get_or_create(
                    loan_id=loan_id,
                    
                    #the get_or_create() has a keyword argument default which specifies the default values when 
                    #creating a new object . 
                    #each field is set by deafult None if that specified row is empty or None and if not None 
                    #it executes the condition 
                    defaults={
                        'investment_date': (
                            datetime.strptime(row.get('investment_date', ''), '%d/%m/%Y') if row.get('investment_date', '') else None
                        ),
                        'maturity_date': (
                            datetime.strptime(row.get('maturity_date', ''), '%d/%m/%Y') if row.get('maturity_date', '') else None
                        ),
                        'interest_rate': (
                            float(row.get('interest_rate', '').strip('%')) if row.get('interest_rate', '') else None
                        ),
                    }
                )

                #checks if 'cashflow_id' is present in the row in order to create an object , and if it isnt
                #it will not be created
                if 'cashflow_id' in df.columns:
                    cashflow_id = row.get('cashflow_id', '')
                    CashFlow.objects.create(
                        cashflow_id=cashflow_id,
                        trade=trade_instance,
                        cashflow_date=(
                            datetime.strptime(row.get('cashflow_date', ''), '%d/%m/%Y') if row.get('cashflow_date', '') else None
                        ),
                        cashflow_currency=row.get('cashflow_currency', ''),
                        cashflow_type=row.get('cashflow_type', ''),
                        amount=(
                            float(row.get('amount', '').replace(',', '')) if row.get('amount', '') else None
                        ),
                    )

            return JsonResponse(
                {"message": "File uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return JsonResponse(
                {"detail": "Missing file in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
            

class TradeRealizedAmountView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]
    serializer_class = TradeSerializer

    def get(self, request, *args, **kwargs):
        loan_id = self.kwargs['loan_id']
        reference_date = self.kwargs['reference_date']
        trade = Trade.objects.get(loan_id=loan_id)
        realized_amount = trade.get_realized_amount(reference_date)
        result = {'loan_id': loan_id, 'realized_amount': realized_amount}
        return Response(result)

class TradeRemainingInvestedAmountView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]
    serializer_class = TradeSerializer

    def get(self, request, *args, **kwargs):
        loan_id = self.kwargs['loan_id']
        reference_date = self.kwargs['reference_date']
        trade = Trade.objects.get(loan_id=loan_id)
        remaining_invested_amount = trade.get_remaining_invested_amount(reference_date)
        result = {'loan_id': loan_id, 'remaining_invested_amount': remaining_invested_amount}
        return Response(result)

class TradeGrossExpectedAmountView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]
    serializer_class = TradeSerializer

    def get(self, request, *args, **kwargs):
        loan_id = self.kwargs['loan_id']
        reference_date = self.kwargs['reference_date']
        trade = Trade.objects.get(loan_id=loan_id)
        
        #calculates gross_expected_amount using the Trade model method
        gross_expected_amount = trade.get_gross_expected_amount(reference_date)

        #creating the result dictionary
        result = {'loan_id': loan_id, 'gross_expected_amount': gross_expected_amount}

        return Response(result)
    
    
class TradeClosingDateView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]
    serializer_class = TradeSerializer

    def get(self, request, *args, **kwargs):
        loan_id = self.kwargs['loan_id']
        trade = Trade.objects.get(loan_id=loan_id)

        #getting the closing_date using the Trade model method
        closing_date = trade.get_closing_date()

        #creating the result dictionary
        result = {'loan_id': loan_id, 'closing_date': closing_date}

        return Response(result)
    
    
class GetCashFlowsView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]

    def get(self, request, *args, **kwargs):
        loan_id = self.kwargs['loan_id']
        cashflows = CashFlow.objects.filter(trade_id=loan_id)

        #serialize cashflows directly in the view
        cashflow_data = CashFlowSerializer(cashflows, many=True).data

        return Response(cashflow_data)
