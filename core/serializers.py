from rest_framework import serializers

class SentimentSerializer(serializers.Serializer):
    
    call_sid = serializers.CharField()
    transcript = serializers.CharField()
    sentiment = serializers.CharField()
