from django.urls import path
from project_app.api.views import FileUpload , TradeRealizedAmountView, TradeRemainingInvestedAmountView, TradeGrossExpectedAmountView, TradeClosingDateView, GetCashFlowsView

urlpatterns = [
    path('upload/', FileUpload.as_view(), name='upload-excel'),
    
    path('trade/realized-amount/<str:loan_id>/<str:reference_date>/', TradeRealizedAmountView.as_view(), name='trade-realized-amount'),
    path('trade/remaining-invested-amount/<str:loan_id>/<str:reference_date>/', TradeRemainingInvestedAmountView.as_view(), name='trade-remaining-invested-amount'),
    path('trade/gross-expected-amount/<str:loan_id>/<str:reference_date>/', TradeGrossExpectedAmountView.as_view(), name='trade-gross-expected-amount'),
    path('trade/closing-date/<str:loan_id>/', TradeClosingDateView.as_view(), name='trade-closing-date'),
    path('trade/get-cashflows/<str:loan_id>/', GetCashFlowsView.as_view(), name='cashflow-details'),


      
]
