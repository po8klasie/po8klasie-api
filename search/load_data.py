import re

import pandas as pd
from psycopg2.extras import NumericRange

from search.models import (
    Address,
    ContactData,
    School,
    HighSchoolClass,
    SubjectName,
    ExtendedSubject,
    LanguageName,
    Language,
    Statistics,
)


def get_class_type(type: str) -> str:
    class_type = {
        "ogólnodostępny": "O",
        "mistrzostwa sportowego": "MS",
        "dwujęzyczny": "D",
        "międzynarodowy": "M",
        "wstępny": "DW",
        "sportowy": "S",
        "integracyjny cz. ogólnodostępna": "I-o",
        "integracyjny cz. dla kandydatów z orzeczeniem o potrzebie kształcenia specjalnego": "I-i",
        "przygotowania wojskowego": "PW",
    }
    return class_type.get(type, "")


def insert_publiczne_oddzialy_2020() -> None:
    data = pd.read_csv("csvs/publiczne_oddzialy_2020.csv", sep=";").to_dict(orient="records")
    for item in data:
        regon = str(item.get("REGON szkoły")).zfill(9)
        try:
            # get existing school object
            school = School.objects.get(public_institution_data__regon=regon)
        except School.DoesNotExist:
            # add new school
            address = Address.objects.create(
                city=item.get("Miejscowość szkoły"),
                postcode=item.get("Kod pocztowy szkoły"),
                district=item.get("Dzielnica"),
                street=item.get("Ulica szkoły"),
                building_nr=item.get("Nr budynku szkoły"),
                longitude=item.get(""),  # no data!
                latitude=item.get(""),  # no data!
            )
            contact = ContactData.objects.create(
                website=item.get(""),  # no data!
                phone=item.get(""),  # no data!
                email=item.get(""),  # no data!
            )
            # public_institution_data = PublicInstitutionData.objects.create(
            #     short_name=item.get(""),  # no data!
            #     institution_name=item.get(""),  # no data!
            #     institution_short_name=item.get(""),  # no data!
            #     institution_type=item.get(""),  # no data!
            #     institution_nr=item.get(""),  # no data!
            #     institution_RSPO=item.get(""),  # no data!
            #     RSPO=item.get(""),  # no data!
            #     institution_regon=item.get(""),  # no data!
            #     regon=item.get(""),  # no data!
            #     data=item.get(""),  # no data!
            # )
            school = School.objects.create(
                school_name=item.get("Nazwa szkoły"),
                school_type=item.get("Typ szkoły (LO/LP/TECH/BR1St/LU/TU/PS)"),
                school_type_generalised="fake",  # TODO create mapping based on school_type
                student_type="fake",  # no data!
                is_special_needs_school=False,  # no data!
                address=address,
                contact=contact,
                specialised_divisions=None,  # no data!
                is_public=item.get("Uprawnienia publiczne") == "szkoła publiczna",
                data={},
            )
        else:
            # update school object
            school.address.city = item.get("Miejscowość szkoły")
            school.address.postcode = item.get("Kod pocztowy szkoły")
            school.address.district = item.get("Dzielnica")
            school.address.street = item.get("Ulica szkoły")
            school.address.building_nr = item.get("Nr budynku szkoły")
            school.school_name = item.get("Nazwa szkoły")
            school.school_type = item.get("Typ szkoły (LO/LP/TECH/BR1St/LU/TU/PS)")
            school.school_type_generalised = (
                "fake"  # TODO create mapping based on school_type
            )
            school.is_public = item.get("Uprawnienia publiczne") == "szkoła publiczna"

        # create high_school_class object
        hsc = HighSchoolClass.objects.create(
            type=get_class_type(item.get("Typ szczególny")),
            name="{} {}".format(
                item.get("Symbol oddziału"), item.get("Nazwa krótka oddziału")
            ),  # TODO check consistency with the scoring
            school=school,
            year=NumericRange(2020, 2022, "[)"),
        )

        # create extended_subject objects
        subjects = item.get("Przedmioty rozszerzone")
        subject_list = subjects.split(",") if isinstance(subjects, str) else []
        subject_names = {
            val: key for (key, val) in SubjectName.choices + LanguageName.choices
        }
        for subject in subject_list:
            subject = subject.strip()
            name = subject_names[subject]
            ExtendedSubject.objects.create(name=name, high_school_class=hsc)

        # create languages objects
        print("value:", item.get("Nazwa krótka oddziału"))
        # TODO fix regex for single language abbr: (ang)
        languages = list(
            re.search(
                "\\((([A-z]+\\*?)(?:,([A-z]+\\*?))*)-([A-z]+\\*?)(?:,([A-z]+\\*?))*\\)",
                item.get("Nazwa krótka oddziału"),
            ).groups()
        )
        for i, lan in enumerate(languages[1:]):
            if not lan:
                continue
            is_multiple_levels = lan.endswith("*")
            is_bilingual = hsc.type = "D" and i == 0
            lan = lan.replace("*", "")
            nr = 1 if lan in languages[0] else 2
            Language.objects.create(
                high_school_class=hsc,
                name=lan,
                multiple_levels=is_multiple_levels,
                is_bilingual=is_bilingual,
                nr=nr,
            )


def insert_min_max_avg() -> None:
    data = pd.read_csv("csvs/scores_2020.csv", sep=";").to_dict(orient="records")
    for item in data:
        try:
            hsc = HighSchoolClass.objects.get(
                name=item.get("school_class"),
                school__school_name=item.get("school_name"),
            )
        except School.DoesNotExist:
            pass
        else:
            Statistics.objects.create(
                high_school_class=hsc,
                points_min=float(item.get("points_min").replace(",", ".")),
                points_max=float(item.get("points_max").replace(",", ".")),
                points_avg=float(item.get("points_avg").replace(",", ".")),
            )


def load_data(apps, schema_editor):
    insert_publiczne_oddzialy_2020()
    insert_min_max_avg()
