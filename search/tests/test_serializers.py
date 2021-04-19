from django.test import TestCase

from search.models import SubjectName, LanguageName
from search.serializers import ExtendedSubjectSerializer
from search.tests.factories import ExtendedSubjectFactory


class TestExtendedSubjectSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.serializer = ExtendedSubjectSerializer()

    def test_get_full_name(self):
        subject1 = ExtendedSubjectFactory.build(name=SubjectName.HMUZ)
        subject2 = ExtendedSubjectFactory.build(name=LanguageName.NIEM)
        self.assertEqual(
            self.serializer.get_full_name(subject1), SubjectName.HMUZ.label
        )
        self.assertEqual(
            self.serializer.get_full_name(subject2), LanguageName.NIEM.label
        )
