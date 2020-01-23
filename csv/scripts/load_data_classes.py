import csv
import re
from search.models import PublicSchool, HighSchoolClass, PublicInstitutionData, Address, ContactData, PrivateSchool, \
    ExtendedSubject


def load():
    with open('csv/Punkty 2018_2019 -  .csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_number = 0
        for row in csv_reader:
            row_number += 1
            if row_number > 4 and row[1] == 'LO':
                name = row[2].strip()
                school = PublicSchool.objects.get(school_name=name)
                print(school.school_name + ':')
                hss = HighSchoolClass()
                hss.school = school.id
                class_name = row[3]
                # class has only one type that is written in brackets eg. [O]
                hss.type = re.sub('[\\[\\]]', '', re.findall(r'\[.+\]', class_name)[0])
                # subjects are placed between the type and list of languages eg. [O] mat-fiz (ang,niem)
                subjects = re.sub('[\\]\\(]', '', re.findall(r'\].+\(', class_name)[0]).strip().split('-')

                for s in subjects:
                    subject = ExtendedSubject()
                    subject.name = s
                    subject.high_school_class = hss
                    print(subject.name)

                # languages are placed in brackets eg. (ang*, niem*)
                languages = re.sub('[\\(\\)]', '', re.findall(r'\(.+\)', class_name)[0]).strip().split(',')
                print(languages)
