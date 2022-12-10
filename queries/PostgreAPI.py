import psycopg2
import neo4j
import redis

class PostgreAPI(object):
    # lections_by_term - dictionary
    def crud(self, lections_by_term):
        database_name = "university"
        user_name = "kirill"
        password = "111"
        host_ip = "127.0.0.1"
        host_port = "5432"

        my_con = psycopg2.connect(
            database=database_name,
            user=user_name,
            password=password,
            host=host_ip,
            port=host_port
        )

        my_con.autocommit = True
        cursor = my_con.cursor()

        start_date = input("Введите дату начала периода")
        end_date = input("Введите дату окончания периода")

        #Выбираем дату за опр. период
        les_ids = ""
        for lection in lections_by_term:
            les_ids += lection['_source']['id'] + ","
        les_ids = les_ids[:-1]
        select_10_studs_query = \
    "SELECT v.studentid, count(*) as cnt \
        FROM TimeTable t, visit v WHERE \
            (t.id = v.tt_id) and \
                (t.date>'" + start_date + "'::date and t.date<'" + end_date + "'::date) and \
                        t.lessonid in (" + les_ids + ") and \
                            v.isvisited = false \
                            group by v.studentid \
                                order by cnt desc \
                                limit 10;"
        select_10_studs_all_query = \
    "SELECT v.studentid, count(*) as cnt \
        FROM TimeTable t, visit v WHERE \
            (t.id = v.tt_id) and \
                (t.date>'" + start_date + "'::date and t.date<'" + end_date + "'::date) and \
                        t.lessonid in (" + les_ids + ") \
                            group by v.studentid;"
        cursor.execute(select_10_studs_query)

        lections_by_period = cursor.fetchall()
        #Выводим результат выбора даты за период


        # it's neccessary list of studs cods
        studs_list = []
        unvis_lecs = []

        for it in lections_by_period:
            studs_list.append(it[0])
            unvis_lecs.append(it[1])

        cursor.execute(select_10_studs_all_query)
        res = cursor.fetchall()

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

        
        # get neo

        url = "bolt://localhost:7687"
        dr = neo4j.GraphDatabase.driver(
            url, auth=neo4j.basic_auth("neo4j", "111")
        )
        session = dr.session()

        studs_str = ""
        for stud in studs_list:
            studs_str += "'" + stud + "',"
        studs_str = studs_str[:-1]

        results = session.run("\
            MATCH (st)-[]->(g:Group)-[]->(s:Specialty)-[]->(c:Cafedra)-[]->(i:Institution) \
                WHERE st.code in [" + studs_str + "] \
                    RETURN \
                        st.code as stud_code, g.code as g_code, \
                            s.code as spec_code, c.code as caf_code, \
                                i.title as i_title")
        result = results.values()

        db_redis = redis.Redis(host="localhost", port=6379)
        # output:
        for i in range(len(result)):
            name_fam = db_redis.get(result[i][0]).decode("utf-8")
            print("{0:10}|{1:10}|{2:10}|{3:15}|{4:10}|{5:40}|{6:10}".format(str(result[i][0]), str(name_fam), str(result[i][1]), str(result[i][2]), str(result[i][3]), str(result[i][4]), str(perc[i]))) 
            print()







