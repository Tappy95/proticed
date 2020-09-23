import faust


class Greeting(faust.Record):
    from_name: str
    to_name: str


app = faust.App('pageviews', broker='kafka://47.112.96.218:9092')
topic = app.topic('mykafka', value_type=Greeting)


@app.agent(topic)
async def hello(greetings):
    async for greeting in greetings:
        print(f'Hello from {greeting.from_name} to {greeting.to_name}')


@app.timer(interval=1)
async def example_sender(app):
    await hello.send(
        value=Greeting(from_name='dddd', to_name='you'),
    )


if __name__ == '__main__':
    app.main()