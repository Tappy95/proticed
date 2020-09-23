import asyncio

import faust
import random

app = faust.App(
    'leader-example',
    borker='kafka://47.112.96.218:9092',
    value_serializer='raw',
)

@app.agent()
async def say(greetings):
    async for greeting in greetings:
        print(greetings)



@app.timer(2.0, on_leader=True)
async def publist_greetings():
    print('publishing on leader!')
    greeting = str(random.random())
    print(greeting)
    await say.send(value=greeting)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.main()