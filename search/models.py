from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from django.contrib.postgres.fields import JSONField
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

