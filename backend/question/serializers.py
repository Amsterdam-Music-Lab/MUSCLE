from rest_framework import serializers
from .models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["key", "text", "index"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(source="choice_set", many=True, required=False)

    class Meta:
        model = Question
        fields = [
            "key",
            "question",
            "editable",
            "explainer",
            "type",
            "scale_steps",
            "profile_scoring_rule",
            "min_value",
            "max_value",
            "max_length",
            "min_values",
            "view",
            "is_skippable",
            "choices",
        ]

    def create(self, validated_data):
        choices_data = validated_data.pop("choice_set", [])
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop("choice_set", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if choices_data:
            # Remove existing choices
            instance.choice_set.all().delete()
            for choice_data in choices_data:
                Choice.objects.create(question=instance, **choice_data)
        return instance
