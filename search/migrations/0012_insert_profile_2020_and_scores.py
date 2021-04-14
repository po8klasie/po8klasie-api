from django.db import migrations
from search.load_data import load_data


def reverse(apps, schema_editor):
    HighSchoolClass = apps.get_model("search", "HighSchoolClass")
    HighSchoolClass.objects.filter(year=(2020, 2022)).delete()


class Migration(migrations.Migration):
    dependencies = [("search", "0011_swap_long_and_lat")]
    operations = [migrations.RunPython(load_data, reverse)]
