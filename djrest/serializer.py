from models import MyDataset
from rest_framework import serializers


class MyDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDataset
        fields = ('server_id', 'application_id', 'start_timestamp')
