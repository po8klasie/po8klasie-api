from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from django.contrib.postgres.fields import JSONField, IntegerRangeField
from django.contrib.postgres.fields import ArrayField


class Address(models.Model):
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=6, validators=[RegexValidator(regex='^\\d\\d-\\d\\d\\d$')])
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building_nr = models.CharField(max_length=20)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)


class ContactData(models.Model):
    website = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(EmailValidator(), max_length=100, null=True)


class School(models.Model):
    school_name = models.CharField(max_length=200)
    school_type = models.CharField(max_length=100)
    school_type_generalised = models.CharField(max_length=40)
    student_type = models.CharField(max_length=100)
    is_special_needs_school = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    contact = models.ForeignKey(ContactData, on_delete=models.CASCADE, null=True)
    specialised_divisions = ArrayField(models.CharField(max_length=100), null=True)
    data = JSONField(null=True)

    class Meta:
        abstract = True


class PublicInstitutionData(models.Model):
    # institution = placówka
    short_name = models.CharField(max_length=20)
    institution_name = models.CharField(max_length=200)
    institution_short_name = models.CharField(max_length=20)
    institution_type = models.CharField(max_length=100)
    institution_nr = models.CharField(max_length=20)
    institution_RSPO = models.CharField(max_length=20)
    RSPO = models.CharField(max_length=20)
    institution_regon = models.CharField(max_length=14)
    regon = models.CharField(max_length=14)
    data = JSONField(null=True)


class PublicSchool(School):
    public_institution_data = models.ForeignKey(PublicInstitutionData, on_delete=models.CASCADE)
    data = JSONField(null=True)


class PrivateSchool(School):
    registration_nr = models.CharField(max_length=20)


class HighSchoolClass(models.Model):
    # O - ogólnokształcące, MS - mistrzostwa sportowego
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    school_id = models.IntegerField()
    year = IntegerRangeField()


class Language(models.Model):
    languages = [('ang', 'język angielski'), ('franc', 'język francuski'),
                 ('hiszp', 'język hiszpański'), ('niem', 'język niemiecki'),
                 ('ros', 'język rosyjski'), ('wło', 'język włoski'),
                 ('antyk', 'język łaciński i kultura antyczna'),
                 ('język białoruski', 'język białoruski'), ('język litewski', 'język litewski'),
                 ('język ukraiński', 'język ukraiński'), ('język łemkowski', 'język łemkowski'),
                 ('język kaszubski', 'język kaszubski')]
    high_school_class = models.ForeignKey(HighSchoolClass, on_delete=models.CASCADE)
    name = models.CharField(choices=languages, max_length=40)
    # pierwszy język obcy/drugi język obcy
    nr = models.IntegerField(choices=[(1, 'pierwszy'), (2, 'drugi')])
    is_bilingual = models.BooleanField(default=False)
    multiple_levels = models.BooleanField(default=False)


class ExtendedSubject(models.Model):
    subjects = [('biol', 'biologia'), ('chem', 'chemia'), ('filoz', 'filozofia'), ('fiz', 'fizyka'),
                ('geogr', 'geografia'), ('hist', 'historia'), ('h.muz.', 'historia muzyki'),
                ('h.szt.', 'historia sztuki'), ('inf', 'informatyka'),
                ('pol', 'język polski'), ('mat', 'matematyka'),
                ('wos', 'wiedza o społeczeństwie'), ('obcy', 'obcy')]

    high_school_class = models.ForeignKey(HighSchoolClass, on_delete=models.CASCADE)
    name = models.CharField(choices=subjects + Language.languages, max_length=40)


class Statistics(models.Model):
    LAUREAT = -1.0
    high_school_class = models.ForeignKey(HighSchoolClass, on_delete=models.CASCADE)
    # tura rekrutacji
    round = models.IntegerField()
    # aka próg
    points_min = models.FloatField()
    points_max = models.FloatField()
    points_avg = models.FloatField()
    with_competency_test = models.BooleanField(default=False)
    only_sports_test = models.BooleanField(default=False)

# TODO technika, szkoły sportowe, prywatne
