from rest_framework import serializers
from search.models import (
    Address,
    ContactData,
    PublicInstitutionData,
    PrivateInstitutionData,
    School,
    Statistics,
    ExtendedSubject,
    HighSchoolClass,
    Language,
)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactData
        fields = "__all__"


class PublicInstitutionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicInstitutionData
        fields = "__all__"


class PrivateInstitutionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateInstitutionData
        fields = "__all__"


class SchoolSerializer(serializers.ModelSerializer):
    classes = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = "__all__"
        depth = 2

    def get_classes(self, obj):
        classes = HighSchoolClass.objects.filter(school=obj.id)
        return HighSchoolClassSerializer(classes, many=True, context=self.context).data


class ExtendedSubjectSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = ExtendedSubject
        fields = "__all__"

    def get_full_name(self, obj):
        full_name = dict(ExtendedSubject.subjects).get(obj.name, None)
        if full_name is None:
            full_name = dict(Language.languages).get(obj.name, "")
        return full_name


class LanguageSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Language
        fields = "__all__"

    def get_full_name(self, obj):
        return dict(Language.languages).get(obj.name, "")


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = "__all__"


class SchoolNameField(serializers.RelatedField):
    def to_internal_value(self, data):
        try:
            try:
                school_id = data
                return School.objects.get(id=school_id)
            except KeyError:
                raise serializers.ValidationError("id is a required field.")
            except ValueError:
                raise serializers.ValidationError("id must be an integer.")
        except School.DoesNotExist:
            raise serializers.ValidationError("School does not exist.")

    def to_representation(self, value):
        return {"school_name": value.school_name}


# http://www.django-rest-framework.org/api-guide/fields/#serializermethodfield


class HighSchoolClassSerializer(serializers.HyperlinkedModelSerializer):
    languages = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = HighSchoolClass
        fields = "__all__"

    def get_languages(self, obj):
        lang = Language.objects.filter(high_school_class=obj.id)
        return LanguageSerializer(lang, many=True).data

    def get_subjects(self, obj):
        sub = ExtendedSubject.objects.filter(high_school_class=obj.id)
        return ExtendedSubjectSerializer(sub, many=True).data

    def get_stats(self, obj):
        stat = Statistics.objects.filter(high_school_class=obj.id)
        return StatisticsSerializer(stat, many=True).data
