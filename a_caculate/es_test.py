from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['es-fx731b5q.public.tencentelasticsearch.com'],
    http_auth=('elastic', '$EStest.813'),
    scheme="https",
    port=9200
)

# res = es.search(index="amazon_product_2020-10-07", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print(hit["_source"])

a = es.indices.get_settings(index='amazon_product_2020-10-07')
print(a)
a = es.indices.put_settings(index='amazon_product_2020-10-07', body={
  "index":{
    "refresh_interval" : -1
  }
})
a = es.indices.get_settings(index='amazon_product_2020-10-07')
print(a)

