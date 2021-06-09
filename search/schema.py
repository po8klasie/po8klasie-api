from graphene import ObjectType, relay, Schema, Connection, Int, String, Field, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene.utils.str_converters import to_snake_case
from search.models import (
    School,
    HighSchoolClass,
    ExtendedSubject,
    Address,
    ContactData,
    PublicInstitutionData,
    PrivateInstitutionData,
    Statistics,
)
from .filters import SchoolFilter, SchoolClassFilter


# https://stackoverflow.com/a/61543302


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        order = args.get("orderBy", None)
        if order:
            if type(order) is str:
                snake_order = to_snake_case(order)
            else:
                snake_order = [to_snake_case(o) for o in order]
            qs = qs.order_by(*snake_order)
        return qs


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


class StatisticsNode(DjangoObjectType):
    class Meta:
        model = Statistics
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

    statistics = Field(StatisticsNode)

    year = Int()

    def resolve_extended_subjects(self, info):
        return ExtendedSubject.objects.filter(high_school_class__id=self.id)

    def resolve_statistics(self, info):
        try:
            return Statistics.objects.get(high_school_class__id=self.id)
        except Statistics.DoesNotExist:
            return None

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

    school_id = String()

    def resolve_classes(self, info, year=None):
        return HighSchoolClass.objects.filter(school__id=self.id)

    def resolve_school_id(self, info):
        return str(self.id)


class Query(ObjectType):
    address = relay.Node.Field(AddressNode)
    contact = relay.Node.Field(ContactDataNode)
    public_institution_data = relay.Node.Field(PublicInstitutionDataNode)
    private_institution_data = relay.Node.Field(PrivateInstitutionDataNode)
    extended_subject = relay.Node.Field(ExtendedSubjectNode)
    statistics = relay.Node.Field(StatisticsNode)

    school = Field(SchoolNode, school_id=String())
    all_schools = OrderedDjangoFilterConnectionField(
        SchoolNode, orderBy=List(of_type=String)
    )

    school_class = relay.Node.Field(SchoolClassNode)
    all_school_classes = DjangoFilterConnectionField(SchoolClassNode)

    def resolve_school(self, info, school_id):
        return School.objects.get(id=school_id)


schema = Schema(query=Query)
