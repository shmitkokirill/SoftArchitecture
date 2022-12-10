from ElasticSearchAPI import ElasticSearchAPI
from PostgreAPI import PostgreAPI 

if __name__ == '__main__':

    es = ElasticSearchAPI()
    postgreCon = PostgreAPI()
    lectionTitleByTermList = es.crud()
    postgreCon.crud(lectionTitleByTermList['hits']['hits'])