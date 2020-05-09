from vidgear.gears.asyncio import NetGear_Async
import asyncio

# initialize Server with suitable source
server = NetGear_Async(source='pr.mp4', address='192.168.6.130', port='5454', protocol='tcp', pattern=3, logging=True).launch()

if __name__ == '__main__':
    # set event loop
    asyncio.set_event_loop(server.loop)
    try:
        # run your main function task until it is complete
        server.loop.run_until_complete(server.task)
    except KeyboardInterrupt:
        # wait for keyboard interrupt
        pass
    finally:
        # finally close the server
        server.close
