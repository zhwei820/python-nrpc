import asyncio

from nats.aio.client import Client as NATS

import helloworld_nrpc
import helloworld_pb2


async def run(loop):
    nc = NATS()

    await nc.connect(io_loop=loop)

    c = helloworld_nrpc.GreeterClient(nc)

    return nc, c


async def req(c):
    for ii in range(1000):
        try:
            r = await c.SayHello(helloworld_pb2.HelloRequest(name='test11'))
            print("Greeting:", r.message)
        except Exception as e:
            print(e)

async def close(nc):
    await nc.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    nc, c = loop.run_until_complete(run(loop))

    tasks = [req(c) for ii in range(1000)]
    # 返回一个列表,内容为各个tasks的返回值
    status_list = loop.run_until_complete(asyncio.gather(*tasks))

    loop.close()
