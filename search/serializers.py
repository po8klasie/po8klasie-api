from rest_framework import serializers
from search.models import *


class PublicSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicSchool
        fields = '__all__'


class ExtendedSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendedSubject
        fields = ['name']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name', 'nr', 'is_bilingual', 'multiple_levels']


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ['round', 'points_min', 'points_max', 'points_avg', 'with_competency_test', 'only_sports_test']


class SchoolNameField(serializers.RelatedField):
    def to_internal_value(self, data):
        try:
            try:
                school_id = data
                return School.objects.get(id=school_id)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except School.DoesNotExist:
            raise serializers.ValidationError(
                'School does not exist.'
            )

    def to_representation(self, value):
        return {'school_name': value.school_name}


class HighSchoolClassSerializer(serializers.ModelSerializer):
    # school = SchoolNameField(queryset=)
    languages = LanguageSerializer(many=True)
    subjects = ExtendedSubjectSerializer(many=True)
    stats = StatisticsSerializer(allow_null=True)

    class Meta:
        model = HighSchoolClass
        exclude = ['school_id']
        depth = 2
