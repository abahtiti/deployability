from rest_framework import serializers

class GetNsmSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIView"""
    devices = serializers.CharField()
