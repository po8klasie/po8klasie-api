from django.db import migrations
import csv
import re


def load_data_private_policealne(apps, schema):
    School = apps.get_model("search", "School")
    PrivateInstitutionData = apps.get_model("search", "PrivateInstitutionData")
    Address = apps.get_model("search", "Address")
    with open("csvs/niepubliczne_policealne.csv", newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        row_number = 0
        for row in csv_reader:
            if row_number == 0:
                row_number += 1
            else:
                row_number += 1

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
                school.school_type = "szkoła policealna"
                school.school_type_generalised = "szkoła policealna"
                school.student_type = "bez kategorii"
                school.address = address
                data.save()
                address.save()
                school.save()


class Migration(migrations.Migration):
    dependencies = [
        ("search", "0005_insert_niepubliczne_lo_dorosli"),
    ]

    operations = [migrations.RunPython(load_data_private_policealne)]
