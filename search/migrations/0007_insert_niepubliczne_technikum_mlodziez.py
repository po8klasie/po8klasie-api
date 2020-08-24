from django.db import migrations
import csv
import re
from search.models import Address, School, PrivateInstitutionData


def load_data_private_technikum(apps, schema):
    with open("csvs/niepubliczne_technika_mlodziez.csv", newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        row_number = 0
        for row in csv_reader:
            if row_number == 0:
                row_number += 1
            else:
                row_number += 1
                print(f"row {row_number} inserted")

                school = School()
                address = Address()
                address.district = row[0]
                school.school_name = row[1].split("(")[0]
                if school.school_name is None:
                    continue
                address.street = row[2]
                address.building_nr = row[3]
                address.postcode = row[4].strip()
                address.city = row[5]

                # clean profession column
                data = re.sub(r"  +", "\n", row[6])
                data = re.sub(r", ", "\n", data)
                data = data.strip().strip("- ").strip("-").strip(",")
                profs = data.lower().splitlines()
                profs = list(filter(None, profs))
                school.data = {"zawód": profs}

                data = PrivateInstitutionData()
                data.registration_nr = row[7]
                school.private_institution_data = data
                school.is_public = False

                school.registration_nr = row[7]
                school.school_type = "technikum"
                school.school_type_generalised = "szkoła ponadpodstawowa"
                school.student_type = "dzieci lub młodzież"
                school.address = address
                data.save()
                address.save()
                school.save()


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0006_insert_niepubliczne_policealne"),
    ]

    operations = [migrations.RunPython(load_data_private_technikum)]
