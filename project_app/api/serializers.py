from project_app.models import CashFlow ,Trade
from rest_framework import serializers


class TradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = '__all__'
        
        

class CashFlowSerializer(serializers.ModelSerializer):
    trade = TradeSerializer()

    class Meta:
        model = CashFlow
        fields = '__all__'



        

        
        