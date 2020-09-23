from typing import List

import faust
import random
from datetime import timedelta


class PageView(faust.Record, serializer='json', coerce=True, include_metadata=False):
    id: str
    user: str
    count: int
    # category_ids: List[str]
    # sold_last_1: int


class PageResult(faust.Record, serializer='json', coerce=True, include_metadata=False):
    id: str
    user: str
    category_id: List[str]
    sold_last_1: int


page_view_default = lambda: PageView(
    id='',
    user='',
    category_ids=[],
    sold_last_1=0
)

app = faust.App(
    id='page_views',
    broker='kafka://47.112.96.218:9092',
    topic_partitions=4
)

page_view_topic = app.topic('page_views', value_type=PageView)

page_views = app.Table('page_views',
                       default=int)



@app.agent(page_view_topic)
async def count_page_views(views):
    async for view in views.group_by(PageView.user):
        # for i in view.category_ids:
        #     page_views['category_id'] = i
        # page_views
        # print(key)
        page_views[view.user] += view.count
        # page_views[view.user] += 3
        # page_views[view.user] += 4
        print('{0}:{1}'.format(view.user, page_views[view.user]))


@app.timer(interval=1)
async def example_sender(app):
    uou = 'uset' + str(random.randint(0, 1))
    await page_view_topic.send(
        value=PageView(id='dddd', user=uou, count=random.randint(2, 9)),
    )


if __name__ == '__main__':
    app.main()
