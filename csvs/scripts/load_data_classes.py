import csv
import re

from search.models import PublicSchool, HighSchoolClass, ExtendedSubject, Statistics


def load():
    with open('csvs/Punkty 2018_2019 -  .csv', newline='') as csv_file:
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
                # TODO

                # stats
                st = Statistics()
                st.high_school_class = hss
                stats = {'min': row[4].strip(), 'avg': row[5].strip(), 'max': row[6].strip()}
                for (k, v) in stats.items():
                    if 'laur' in v.lower():
                        stats[k] = Statistics.LAUREAT
                    elif '**' in v:
                        st.with_competency_test = True
                        stats[k] = re.sub('\\*', '', v)
                    elif '*' in v:
                        st.only_sports_test = True
                        stats[k] = re.sub('\\*', '', v)

                st.points_min = stats['min']
                st.points_avg = stats['avg']
                st.points_max = stats['max']


