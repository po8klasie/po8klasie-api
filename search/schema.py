from graphene import ObjectType, relay, Schema, Connection, Int
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from search.models import (
    School,
    HighSchoolClass,
    ExtendedSubject,
    Address,
    ContactData,
    PublicInstitutionData,
    PrivateInstitutionData,
)
from .filters import SchoolFilter, SchoolClassFilter


class CountedConnection(Connection):
    class Meta:
        abstract = True

    total_count = Int()
    edge_count = Int()

    def resolve_total_count(self, info):
        return self.length

    def resolve_edge_count(self, info):
        return len(self.edges)


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


class ExtendedSubjectNode(DjangoObjectType):
    class Meta:
        model = ExtendedSubject
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (relay.Node,)


class AddressNode(DjangoObjectType):
    class Meta:
        model = Address
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (relay.Node,)


class SchoolClassNode(DjangoObjectType):
    class Meta:
        model = HighSchoolClass
        fields = "__all__"
        filterset_class = SchoolClassFilter
        interfaces = (relay.Node,)

    extended_subjects = DjangoFilterConnectionField(ExtendedSubjectNode)

    year = Int()

    def resolve_year(self, info):
        return self.year.lower


class SchoolNode(DjangoObjectType):
    class Meta:
        model = School
        exclude = ("highschoolclass_set",)
        filterset_class = SchoolFilter
        interfaces = (relay.Node,)
        connection_class = CountedConnection

    classes = DjangoFilterConnectionField(SchoolClassNode)

    def resolve_classes(self, info):
        return HighSchoolClass.objects.filter(school__id=self.id)


class Query(ObjectType):
    address = relay.Node.Field(AddressNode)
    contact = relay.Node.Field(ContactDataNode)
    public_institution_data = relay.Node.Field(PublicInstitutionDataNode)
    private_institution_data = relay.Node.Field(PrivateInstitutionDataNode)
    extended_subject = relay.Node.Field(ExtendedSubjectNode)

    school = relay.Node.Field(SchoolNode)
    all_schools = DjangoFilterConnectionField(SchoolNode)

    school_class = relay.Node.Field(SchoolClassNode)
    all_school_classes = DjangoFilterConnectionField(SchoolClassNode)


schema = Schema(query=Query)
