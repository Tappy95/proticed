search_info = {
    "from": 0,
    "size": 64,
    "query": {
        "bool": {
            "filter": [
                {"term": {"site": "us"}},
                {"range": {"price": {
                    "gte": 0,
                    "lte": 99999999,
                }}}
            ]
        }
    }
}

for i in search_info['query']['bool']['filter']:
    if "range" in i:
        if "price" in i['range']:
            pass



class menmen():

    @staticmethod
    def koko(info):
        print(info)



M = menmen()
M.koko("koko")