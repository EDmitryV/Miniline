from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import GameCore, Boost, WordsSet


class GameCoreSerializer(ModelSerializer):
    next_level_price = SerializerMethodField()
    words = serializers.CharField(source='words_set.words')
    lang = serializers.CharField(source='words_set.lang')

    class Meta:
        model = GameCore
        fields = ['points', 'click_power', 'auto_click_power', 'next_level_price', 'words', 'lang']

    def get_next_level_price(self, instance):
        return instance.calculate_next_level_price()


class BoostSerializer(ModelSerializer):
    class Meta:
        model = Boost
        fields = '__all__'


class WordsSetSerializer(ModelSerializer):
    class Meta:
        model = WordsSet
        fields = '__all__'
