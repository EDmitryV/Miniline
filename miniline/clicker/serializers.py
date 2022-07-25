from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import GameCore, Boost, WordsSet


class GameCoreSerializer(ModelSerializer):
    next_level_price = SerializerMethodField()
    words = SerializerMethodField()

    class Meta:
        model = GameCore
        fields = [
            'points',
            'click_power',
            'auto_click_power',
            'next_level_price',
            'lang_code',
            'words'
        ]

    def get_next_level_price(self, instance):
        return instance.calculate_next_level_price()

    def get_words(self, instance):
        return instance.words_set.content


class BoostSerializer(ModelSerializer):
    class Meta:
        model = Boost
        fields = '__all__'
