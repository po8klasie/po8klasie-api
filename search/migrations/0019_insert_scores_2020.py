import pandas as pd
from django.db import migrations
from psycopg2.extras import NumericRange


def insert_scores(apps, schema_editor):
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


def reverse(apps, schema_editor):
    Statistics = apps.get_model("search", "Statistics")
    Statistics.objects.filter(high_school_class__year=(2020, 2022)).delete()


class Migration(migrations.Migration):
    dependencies = [("search", "0018_insert_raport_2021")]
    operations = [migrations.RunPython(insert_scores, reverse)]
