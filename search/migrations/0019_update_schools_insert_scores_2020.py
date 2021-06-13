import pandas as pd
from django.db import migrations
from psycopg2.extras import NumericRange


def update_school_data(apps):
    School = apps.get_model("search", "School")

    data = pd.read_csv("csvs/publiczne_oddzialy_2020.csv", sep=";").to_dict(orient="records")
    for item in data:
        regon = str(item.get("REGON szkoły")).zfill(9)
        try:
            school = School.objects.get(public_institution_data__regon=regon)
        except School.DoesNotExist:
            continue
        else:
            school.address.city = item.get("Miejscowość szkoły")
            school.address.postcode = item.get("Kod pocztowy szkoły")
            school.address.district = item.get("Dzielnica")
            school.address.street = item.get("Ulica szkoły")
            school.address.building_nr = item.get("Nr budynku szkoły")
            school.school_name = item.get("Nazwa szkoły").strip()
            school.school_type = item.get("Typ szkoły (LO/LP/TECH/BR1St/LU/TU/PS)")
            school.is_public = item.get("Uprawnienia publiczne") == "szkoła publiczna"
            school.address.save()
            school.save()


def insert_scores(apps):
    HighSchoolClass = apps.get_model("search", "HighSchoolClass")
    Statistics = apps.get_model("search", "Statistics")

    data = pd.read_csv("csvs/scores_2020.csv", sep=";").to_dict(orient="records")
    for item in data:
        try:
            hsc = HighSchoolClass.objects.get(
                name=item.get("school_class").split(" ")[0],
                school__school_name=item.get("school_name").strip(),
                year=NumericRange(2020, 2022, "[)"),
            )
        except HighSchoolClass.DoesNotExist:
            continue
        else:
            hsc.name = item.get("school_class").strip()
            hsc.save()
            Statistics.objects.create(
                high_school_class=hsc,
                points_min=float(item.get("points_min").replace(",", ".")),
                points_max=float(item.get("points_max").replace(",", ".")),
                points_avg=float(item.get("points_avg").replace(",", ".")),
                round=1,
            )


def load_data(apps, schema_editor):
    update_school_data(apps)
    insert_scores(apps)


def reverse(apps, schema_editor):
    Statistics = apps.get_model("search", "Statistics")
    Statistics.objects.filter(high_school_class__year=(2020, 2022)).delete()


class Migration(migrations.Migration):
    dependencies = [("search", "0018_insert_raport_2021")]
    operations = [migrations.RunPython(load_data, reverse)]
