from elasticsearch import Elasticsearch, helpers

class ElasticSearchAPI(object):
    def crud(self):
        es = Elasticsearch('http://elastic:111111@localhost:9200')
        query = input("Введите термин\n")
        doctype = "_doc"
        res = es.search(index="lessons", body={"query": {"match": {"material": query}}})
        #res = es.search(index="lesson", query={"match_all": {}})
        #print("%d documents found:" % res['hits']['total'])
        #for doc in res['hits']['hits']:
            #print("%s" % (doc['_source']['title']))
        return res
# Возникает ошибка с несовместимостью версии API с версией ES
# Решение: File/Setting/Python Interpreter выбираем библиотеку elasticsearch и ставим версию ближе к версии БД