import asyncio

from nats.aio.client import Client as NATS

import helloworld_nrpc
import helloworld_pb2


class Server:
    async def SayHello(self, req):
        res = helloworld_pb2.HelloReply(message="Hello:" + req.name,)
        return res


async def run(loop):
    nc = NATS()

    await nc.connect(io_loop=loop)

    h = helloworld_nrpc.GreeterHandler(nc, Server())

    await nc.subscribe(h.subject(), cb=h.handler)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()
