from rest_framework import serializers

class HealthCheckerSerializer(serializers.Serializer):
    """Serializers a devices field for testing our APIView"""
    devices = serializers.CharField()
