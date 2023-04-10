import datetime
import time
import psycopg2
import random

russian_letter = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЫЭЮЯ'
institutes_name = ["Институт кибербезопасности и цифровых технологий", "Институт информационных технологий",
                   "Институт радиоэлектроники и информатики"]
cafedras_name = ["КБ-1", "КБ-2", "КБ-3", "КБ-4", "БК-1", "БК-2", "БК-3", "БК-4", "БК-5", "БК-6", "БК-7", "БК-8"]
speciality_name = ["10.03.01", "10.05.03", "10.05.04", "09.03.02", "09.03.04", "09.03.01", "09.04.01", "09.03.03",
                   "11.03.01", "11.05.01", "11.03.03", "11.03.02"]
courses_name = [
	"Основы информационной безопасности", "Программно-аппаратные средства защиты информации",
	"Криптографические методы защиты информации", "Орг. и правовое обеспечение информ. безопасности",
	"Документоведение", "Основы управления информационной безопасностью",
	"Угрозы инф. безопасности автомат. систем", "Техническая защита информации",
	"Сети и системы передачи информации", "Технологии и методы программирования",
	"Теоретические основы компьютерной безопасности", "Безопасность операционных систем",
	"Безопасность вычислительных систем", "Безопасность систем баз данных",
	"Разработка защищенных автоматизированных систем", "Защита информации от вредоносного ПО",
	"Технические средства защиты объектов", "Катастрофоустойчивость информационных систем",
	"Основы формирования каналов возд. на инф. системы", "Биометрические системы аутентификации",
	"Стандарты информационной безопасности", "Инновационные методы защиты информации",
	"Защита инф. от вредоносного ПО",
	"Орг. и техн. защиты конф. инф. на предприятиях"]
lesson_name = ["Методы решения дифф. уравнений", "Программироване на Java", "Программироване на Python",
               "Программироване на C#", "Программироване на C++", "Программироване на Pascal",
               "Программироване на Ruby", "Английский язык", "Китайский язык", "Немецкий язык", "Русский язык",
               "Экономика", "Правоведение", "История России", "История США", "Политология", "Теория вероятности",
               "Философия", "Информатика", "Машинное обучение"]
gruppa_name = ["БСБО-01-19", "БСБО-02-19", "БСБО-03-19"]

first_names = ['Иван', 'Степан', 'Евгений', 'Сергей', 'Андрей', 'Павел', 'Руслан', 'Даниил', 'Михаил', 'Станислав']
last_names = ['Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов', 'Михайлов', 'Новиков',
              'Фёдоров']

times_of_lesson = [[9, 0], [10, 40], [12, 40], [14, 20], [16, 20], [18, 00]]
# postgre
postgreconn = psycopg2.connect(dbname='university', user='postgres',
                               password='postgres', host='localhost')
postgredb = postgreconn.cursor()
postgredb.execute('DELETE FROM mirea.visit')
postgredb.execute('DELETE FROM mirea.time_table')
postgredb.execute('DELETE FROM mirea.student')
postgredb.execute('DELETE FROM mirea.gruppa')
postgredb.execute('DELETE FROM mirea.lesson')
postgredb.execute('DELETE FROM mirea.speciality')
postgredb.execute('DELETE FROM mirea.course')
postgredb.execute('DELETE FROM mirea.cafedra')
postgredb.execute('DELETE FROM mirea.institutions')

postgreconn.commit()

time.sleep(5)

# fill_institutions
for inst in institutes_name:
	postgredb.execute(
		"INSERT INTO mirea.institutions(id, title) VALUES (%d,'%s')" % (institutes_name.index(inst) + 1, inst)
	)
postgreconn.commit()

time.sleep(5)

# fill_cafedras
for cafedra in cafedras_name:
	id = cafedras_name.index(cafedra) + 1
	postgredb.execute(
		"INSERT INTO mirea.cafedra(code, title, institution_id) VALUES ('%s','%s', %d)" % (
			cafedra,
			"Kaфедра " + str(id),
			institutes_name.index(random.choice(institutes_name)) + 1)
	)
postgreconn.commit()

time.sleep(5)

# fill_speciality
for spec in speciality_name:
	id = speciality_name.index(spec) + 1
	postgredb.execute(
		"INSERT INTO mirea.speciality(code, title, cafedra_code) VALUES ('%s','%s', '%s')" % (
			spec,
			"Специальность " + str(id),
			random.choice(cafedras_name))
	)
postgreconn.commit()

time.sleep(5)

# fill_course
for course in courses_name:
	id = courses_name.index(course) + 1
	postgredb.execute(
		"INSERT INTO mirea.course(id, title, spec_code) VALUES (%d, '%s', '%s')" % (
			id,
			course,
			random.choice(speciality_name))
	)
postgreconn.commit()

time.sleep(5)

# fill lesson
for lesson in lesson_name:
	id = lesson_name.index(lesson) + 1
	postgredb.execute(
		"INSERT INTO mirea.lesson(id, title, course_id) VALUES (%d, '%s', %d)" % (
			id,
			lesson,
			courses_name.index(random.choice(courses_name)) + 1)
	)
postgreconn.commit()

time.sleep(5)

# fill gruppa
for gruppa in gruppa_name:
	id = gruppa_name.index(gruppa) + 1
	postgredb.execute(
		"INSERT INTO mirea.gruppa(code, speciality_code, end_year) VALUES ('%s','%s',%d)" % (
			gruppa,
			random.choice(speciality_name),
			2023)
	)
postgreconn.commit()

time.sleep(5)

# fill student
stud_codes = [[], [], []]
for i in range(60):
	stud_code = "19Б0" + str(10 + i)
	gruppa = random.choice(gruppa_name)
	stud_codes[gruppa_name.index(gruppa)].append(stud_code)
	student_name = random.choice(first_names) + " " + random.choice(last_names)
	postgredb.execute(
		"INSERT INTO mirea.student (code, full_name, gruppa_code) VALUES ('%s','%s', '%s')" % (
			stud_code,
			student_name,
			gruppa)
	)
postgreconn.commit()

time.sleep(5)

# fill timetable + visit
tt_id = 0
visit_id = 0
for gruppa in gruppa_name:
	start_datetime = datetime.datetime(2022, 9, 1)
	while start_datetime < datetime.datetime(2023, 1, 1):
		rand_end_time = random.choice(times_of_lesson)
		for time in times_of_lesson:
			tt_id += 1
			postgredb.execute(
				"INSERT INTO mirea.time_table (id, date_time, gruppa_code, lesson_id, lesson_number) VALUES (%d,'%s','%s', %d, %d)" %
				(tt_id,
				 start_datetime + datetime.timedelta(hours=time[0], minutes=time[1]),
				 gruppa,
				 lesson_name.index(random.choice(lesson_name)) + 1,
				 times_of_lesson.index(time) + 1))


			for stud in stud_codes[gruppa_name.index(gruppa)]:
				visit_id+=1
				postgredb.execute(
					"INSERT INTO mirea.visit (id, student_code, time_table_id, is_visited) VALUES (%d,'%s',%d,%s)" % (
						visit_id,
						stud,
						tt_id,
						str(bool(random.getrandbits(1))).lower(),
					)
				)
			if time == rand_end_time:
				start_datetime += datetime.timedelta(days=1)
				if (start_datetime.weekday() == 6):
					start_datetime += datetime.timedelta(days=1)
				break

postgreconn.commit()

postgredb.close()
postgreconn.close()
