import asyncio
import random
import os
import time
from nats.aio.client import Client as NATS

import helloworld_nrpc
import helloworld_pb2

from jaeger_client import Config
from jaeger_client import Span, SpanContext
from jaeger_client import constants

constants.MAX_ID_BITS = 32

def init_tracer():
    config = Config(
        config={  # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='ServiceName',
        validate=False,
    )
    # this call also sets opentracing.tracer
    tracer = config.initialize_tracer()
    randomnize = random.Random(time.time() * (os.getpid() or 1))

    return tracer, randomnize

tracer, randomnize = init_tracer()


async def main(loop):
    nc = NATS()

    await nc.connect(io_loop=loop)

    c = helloworld_nrpc.GreeterClient(nc)

    return nc, c


def get_span_str(span1):
    return '%x:%x:%x:%x' % (span1.trace_id, span1.span_id, span1.parent_id if span1.parent_id else span1.span_id, span1.flags)


async def req(c):

    for ii in range(100):

        ctx = SpanContext(trace_id=randomnize.getrandbits(32), span_id=randomnize.getrandbits(32), parent_id=0, flags=1)
        span = Span(context=ctx, operation_name='RootSpan', tracer=tracer)
        span.log_kv({'event': 'RootSpan', })

        # with tracer.start_span('TestSpan') as span:
        #
        #     span.log_kv({'span.trace_id': span.trace_id,
        #                  'span.span_id': span.span_id,
        #                  'span.parent_id': span.parent_id,
        #                  'span.operation_name': span.operation_name,
        #                  })
        #
        #     #     ctx = SpanContext(trace_id=child_span.trace_id, span_id=span_id1, parent_id=child_span.span_id, flags=1)
        #     #     span1 = Span(context=ctx, operation_name='ChildSpanChildSpan', tracer=tracer)
        #     #     span1.log_kv({'event': 'ChildSpanChildSpan', })
        #
        #     # t1 = time.time()
        #     # try:
        #     #     r = await c.SayHello(
        #     #         helloworld_pb2.HelloRequest(name='test11', spaninfo=get_span_str(span)))
        #     #     # print("Greeting:", r.message)
        #     # except Exception as e:
        #     #     pass
        #     #
        #     # t2 = time.time()
        #     # print(t2 - t1)
        #
        #     span.log_kv({'span.trace_id': span.trace_id,
        #                  'span.span_id': span.span_id,
        #                  'span.parent_id': span.parent_id,
        #                  'span.operation_name': span.operation_name,
        #                  })

        t1 = time.time()
        try:
            r = await c.SayHello(
                helloworld_pb2.HelloRequest(name='test11', spaninfo=get_span_str(span)))
            # print("Greeting:", r.message)
        except Exception as e:
            pass

        t2 = time.time()
        print(t2 - t1)
        span.log_kv({'event': t2 - t1, })

        span.finish()

async def close(nc):
    await nc.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    nc, c = loop.run_until_complete(main(loop))

    tasks = [req(c) for ii in range(1000)]
    # 返回一个列表,内容为各个tasks的返回值
    status_list = loop.run_until_complete(asyncio.gather(*tasks))

    loop.close()
    time.sleep(5)   # yield to IOLoop to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50
    tracer.close()  # flush any buffered spans
