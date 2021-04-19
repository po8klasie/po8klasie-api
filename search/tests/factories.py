import factory
import factory.fuzzy
from psycopg2.extras import NumericRange

from search.models import (
    Address,
    School,
    SchoolType,
    HighSchoolClass,
    HighSchoolClassType,
    ExtendedSubject,
    LanguageName,
    SubjectName,
)


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    city = factory.Faker("city", locale="pl_PL")
    postcode = factory.Faker("postcode", locale="pl_PL")
    district = factory.Faker("city", locale="pl_PL")
    street = factory.Faker("street_name", locale="pl_PL")
    building_nr = factory.Faker("building_number")


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    school_name = factory.Sequence(lambda n: "%02d. LO" % n)
    school_type = SchoolType.LO
    address = factory.SubFactory(AddressFactory)
    is_public = True


class HighSchoolClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HighSchoolClass

    type = factory.fuzzy.FuzzyChoice(choices=HighSchoolClassType.choices)
    name = factory.fuzzy.FuzzyText(length=3)
    school = factory.SubFactory(SchoolFactory)
    year = NumericRange(2020, 2022, "[)")


class ExtendedSubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExtendedSubject

    high_school_class = factory.SubFactory(HighSchoolClassFactory)
    name = factory.fuzzy.FuzzyChoice(choices=SubjectName.choices + LanguageName.choices)
