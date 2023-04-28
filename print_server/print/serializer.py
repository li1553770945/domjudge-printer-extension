from rest_framework import serializers
from print.models import PrintModel


class PrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintModel
        fields = '__all__'
    status = serializers.ChoiceField(choices=("pending", "processing", "done"), default="pending")

