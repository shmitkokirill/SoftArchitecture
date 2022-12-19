import db_api as db
from prettytable import PrettyTable
import sys

class DBManager:
    # (start, end)
    def get_period_of_sem(self, semester, year):
        if semester == '1':
            return (str(year + "-09-01"), str(year + "-12-31"))
        elif semester == '2':
            return (str(year + "-02-01"), str(year + "-06-30"))
        else:
            return None

    # in: list = [(int, )]; out: "'int','int', ..."
    def get_str_from_list(self, list):
        if len(list) == 0:
            return None
        result = ""
        for it in list:
            result += "'" + str(it[0]) + "',"
        return result[:-1]
    
    def get_str_elastic(self, lessons_list):
        if len(lessons_list) == 0:
            return None
        less_ids = ""
        for lesson in lessons_list:
            less_ids += lesson['_source']['id'] + ","
        return less_ids[:-1]
    
    def get_str_neo(self, list):
        if len(list) == 0:
            return None
        less_ids = ""
        for it in list:
            less_ids += "'" + it['_source']['id'] + "',"
        return less_ids[:-1]

    def exec_first_lab(self):
        postgres = db.Postgres()
        elastic = db.Elastic()
        neo = db.Neo()
        redis = db.Redis()

        term = input("Введите термин\n")
        les_ids = self.get_str_elastic(
            elastic.getLessonsByTerm(term)['hits']['hits']
        )
        if les_ids == None:
            print("Не найдено лекций по термину")
            return 1

        start_date = input("Введите дату начала периода\n")
        end_date = input("Введите дату окончания периода\n")

        lections_by_period = postgres.get_10_studs(start_date, end_date, les_ids)
        if len(lections_by_period) == 0:
            print("Не найдено студентов по периоду")
            return 1

        # it's neccessary list of studs cods
        studs_list = []
        unvis_lecs = []

        for it in lections_by_period:
            studs_list.append(it[0])
            unvis_lecs.append(it[1])
        
        res = postgres.get_allStuds(start_date, end_date, les_ids)
        if len(res) == 0:
            print("Не найдено студенов по периоду")
            return 1

        studs_list_1 = []
        all_lecs_1 = []

        for it in res:
            studs_list_1.append(it[0])
            all_lecs_1.append(it[1])

        # same len with studs_list, it's perc of visits
        perc = []       
        for j in range(len(studs_list)):
            for i in range(len(studs_list_1)):
                if studs_list[j] == studs_list_1[i]:
                    perc.append(1 - (unvis_lecs[j] / all_lecs_1[i]))
        
        studs_str = ""
        for stud in studs_list:
            studs_str += "'" + stud + "',"
        studs_str = studs_str[:-1]

        result = neo.get_groupInfo_by_studs(studs_str)
        output = PrettyTable()
        output.field_names = [
            "Студ. билет", "ФИО", "Группа", 
            "Специальность", "Кафедра", "Институт", "Процент посещения"
        ]
        for i in range(len(result)):
            name_fam = redis.get_fio(result[i][0])
            output.add_row(
                [
                    str(result[i][0]), 
                    str(name_fam), 
                    str(result[i][1]), 
                    str(result[i][2]), 
                    str(result[i][3]), 
                    str(result[i][4]), 
                    str(perc[i])
                ]
            )
        print(output)
    
    def exec_second_lab(self):
        postgres = db.Postgres()
        elastic = db.Elastic()
        neo = db.Neo()
        mongo = db.Mongo()

        course = input("Введите название курса\n")
        les_ids_neo = neo.get_lessons_ids(course)
        if len(les_ids_neo) == 0:
            print("Не найдено заданного курса")
            return 1

        term = input("Введите термин\n")
        lessons = elastic.getLessonsByTerm_Ids(term, les_ids_neo)['hits']['hits']

        less_ids = self.get_str_elastic(lessons)
        if less_ids == None or less_ids == "":
            print("Не найдено лекций по термину")
            return 1

        semester = input("Введите номер семестра (1/2)\n")
        year = input("Введите год семестра\n")
        period = self.get_period_of_sem(semester, year)
        founded_less_ids = \
            postgres.get_lesIds_by_period_lesIds(period[0], period[1], less_ids)
        if len(founded_less_ids) == 0:
            print("Не найдено лекций за период")
            return 1
        
        less_ids_str = self.get_str_from_list(founded_less_ids)
        studs_count = neo.get_students_count(less_ids_str, course)
        if len(studs_count) == 0:
            print("Не удалось получить количество студентов")
            return 1

        info_table = mongo.get_courseInfo_table(course)

        print("Количество студентов:", end='')
        print(studs_count)
        print(info_table)
    
    def exec_third_lab(self):
        postgres = db.Postgres()
        elastic = db.Elastic()
        redis = db.Redis()
        neo = db.Neo()
        mongo = db.Mongo()

        teg = input("Введите тег\n")
        group = input("Введите группу\n").replace(" ", "").upper()

        lessons = elastic.getLessonsByTerm(teg)['hits']['hits']
        less_ids_by_teg = self.get_str_elastic(lessons)
        if less_ids_by_teg == None or less_ids_by_teg == "":
            print("Найдено лекций по тегу")
            return 1

        start_date = input("Введите дату начала периода\n")
        end_date = input("Введите дату окончания периода\n")

        # [(tt_id, ), ]
        tt_ids = postgres.get_ttIds_by_group(
            start_date, end_date, less_ids_by_teg, group
        )
        if len(tt_ids) == 0:
            print("Не найдено лекций за период для группы")
            return 1

        tt_ids_str = self.get_str_from_list(tt_ids)
        #[(st_code, vis_count), ]
        stud_hours_tab = postgres.get_studHours_table(tt_ids_str)
        if len(stud_hours_tab) == 0:
            print("Не найдено студентов за период")
            return 1

        # output
        total_hours = len(tt_ids) * 1.5
        stud_table = PrettyTable()
        stud_table.field_names = [
            "Студ. билет", "ФИО", "Кол-во посещений (ч)", 
            "Общее кол-во часов", "Группа"
        ]
        for st in stud_hours_tab:
            st_code = st[0]
            fio = redis.get_fio(st_code)
            visit = float(st[1]) * 1.5
            stud_table.add_row([st_code, fio, visit, total_hours, group])

        print("Информация о студентах и посещениях")
        print(stud_table)

        group_table = PrettyTable()
        group_table.field_names = [
            "Группа", "Специальность", "Кафедра", "Институт"
        ]
        gr_info = neo.get_group_info(group)
        if len(gr_info) == 0 or len(gr_info[0]) == 0:
            print("Не найдено информации о группе")
            return 1

        group_table.add_row(gr_info[0])

        print("Информация о группе")
        print(group_table)
        
        # course info
        print("Информация о курсах")
        less_ids_neo = self.get_str_neo(lessons)
        course_titles = neo.exec_query(
            "match (l:Lesson)-[]->(c:Course) where l.id in [" + less_ids_neo + "] \
                return distinct c.title"
        )
        if len(course_titles) == 0 or len(course_titles[0]) == 0:
            print("Не найдено информации о курсе")
            return 1

        for title_arr in course_titles:
            for title in title_arr:
                print(mongo.get_courseInfo_table(title))
                print()
        
manager = DBManager()

if sys.argv[1] == "1":
    manager.exec_first_lab()
elif sys.argv[1] == "2":
    manager.exec_second_lab()
elif sys.argv[1] == "3":
    manager.exec_third_lab()


