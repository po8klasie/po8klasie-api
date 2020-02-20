from rest_framework import serializers
from search.models import *


class PublicSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicSchool
        exclude = ['public_institution_data']
        depth = 2

class PrivateSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateSchool
        fields = '__all__'
        depth = 2


class ExtendedSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendedSubject
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'


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


# http://www.django-rest-framework.org/api-guide/fields/#serializermethodfield

class HighSchoolClassSerializer(serializers.HyperlinkedModelSerializer):
    languages = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = HighSchoolClass
        fields = '__all__'
        depth = 2

    def get_languages(self, obj):
        lang = Language.objects.filter(high_school_class=obj.id)
        return LanguageSerializer(lang, many=True).data

    def get_subjects(self, obj):
        sub = ExtendedSubject.objects.filter(high_school_class=obj.id)
        return ExtendedSubjectSerializer(sub, many=True).data

    def get_stats(self, obj):
        stat = Statistics.objects.filter(high_school_class=obj.id)
        return StatisticsSerializer(stat, many=True).data

