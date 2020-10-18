import django_filters
from graphene import relay
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from search.models import (
    Address,
    ContactData,
    PublicInstitutionData,
    PrivateInstitutionData,
    School,
    HighSchoolClass,
    Language,
    ExtendedSubject,
    Statistics,
)


class AddressNode(DjangoObjectType):
    class Meta:
        model = Address
        filter_fields = "__all__"
        interfaces = (relay.Node,)


class ContactDataNode(DjangoObjectType):
    class Meta:
        model = ContactData
        filter_fields = "__all__"
        fields = "__all__"
        interfaces = (relay.Node,)


class PublicInstitutionDataNode(DjangoObjectType):
    class Meta:
        model = PublicInstitutionData
        fields = "__all__"
        filter_fields = (
            "short_name",
            "institution_name",
            "institution_short_name",
            "institution_type",
            "institution_nr",
            "institution_RSPO",
            "RSPO",
            "institution_regon",
            "regon",
        )
        interfaces = (relay.Node,)


class PrivateInstitutionDataNode(DjangoObjectType):
    class Meta:
        model = PrivateInstitutionData
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (relay.Node,)


class SchoolFilter(django_filters.FilterSet):
    class Meta:
        model = School
        fields = [
            "school_name",
            "nickname",
            "school_type",
            "school_type_generalised",
            "student_type",
            "is_special_needs_school",
            "address",
            "contact",
            "is_public",
            "public_institution_data",
            "private_institution_data",
        ]


class SchoolNode(DjangoObjectType):
    class Meta:
        model = School
        fields = "__all__"
        interfaces = (relay.Node,)
        filterset_class = SchoolFilter


class HighSchoolClassNode(DjangoObjectType):
    class Meta:
        model = HighSchoolClass
        fields = "__all__"
        filter_fields = ("type", "name", "school")
        interfaces = (relay.Node,)


class LanguageNode(DjangoObjectType):
    class Meta:
        model = Language
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (relay.Node,)


class ExtendedSubjectNode(DjangoObjectType):
    class Meta:
        model = ExtendedSubject
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (relay.Node,)


class StatisticsNode(DjangoObjectType):
    class Meta:
        model = Statistics
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    address = relay.Node.Field(AddressNode)
    all_addresses = DjangoFilterConnectionField(AddressNode)

    contact = relay.Node.Field(ContactDataNode)
    all_contacts = DjangoFilterConnectionField(ContactDataNode)

    public_institution_data = relay.Node.Field(PublicInstitutionDataNode)
    all_public_institution_data = DjangoFilterConnectionField(PublicInstitutionDataNode)

    private_institution_data = relay.Node.Field(PrivateInstitutionDataNode)
    all_private_institution_data = DjangoFilterConnectionField(
        PrivateInstitutionDataNode
    )

    school = relay.Node.Field(SchoolNode)
    all_schools = DjangoFilterConnectionField(SchoolNode)

    high_school_class = relay.Node.Field(HighSchoolClassNode)
    all_high_school_classes = DjangoFilterConnectionField(HighSchoolClassNode)

    language = relay.Node.Field(LanguageNode)
    all_languages = DjangoFilterConnectionField(LanguageNode)

    extended_subject = relay.Node.Field(ExtendedSubjectNode)
    all_extended_subjects = DjangoFilterConnectionField(ExtendedSubjectNode)

    statistics = relay.Node.Field(StatisticsNode)
    all_statistics = DjangoFilterConnectionField(StatisticsNode)


schema = graphene.Schema(query=Query)
