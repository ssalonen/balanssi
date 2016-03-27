from rest_framework.serializers import ModelSerializer
from balanssi.models import Transaction

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
