import asyncio
import random
import os
import time
from nats.aio.client import Client as NATS

import helloworld_nrpc
import helloworld_pb2

from jaeger_client import Config
from jaeger_client import Span, SpanContext
from jaeger_client import  constants

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
        validate=True,
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
    return '%x:%x:%x:%x' % ( span1.trace_id, span1.span_id, span1.parent_id, span1.flags)


async def req(c):
    for ii in range(1):
        span_id1 = randomnize.getrandbits(32)

        with tracer.start_span('TestSpan') as span:

            span.log_kv({'span.trace_id': span.trace_id,
                         'span.span_id': span.span_id,
                         'span.parent_id': span.parent_id,
                         'span.operation_name': span.operation_name,
                         })

            with tracer.start_span('ChildSpan', child_of=span) as child_span:
                child_span.log_kv({'span.trace_id': child_span.trace_id,
                                   'child_span.span_id': child_span.span_id,
                                   'child_span.parent_id': child_span.parent_id,
                                   'child_span.operation_name': child_span.operation_name,
                                   })

                ctx = SpanContext(trace_id=child_span.trace_id, span_id=span_id1, parent_id=child_span.span_id, flags=1)
                span1 = Span(context=ctx, operation_name='ChildSpanChildSpan', tracer=tracer)
                span1.log_kv({'event': 'ChildSpanChildSpan', })

                try:
                    print(get_span_str(span1))
                    print(span1.span_id)

                    r = await c.SayHello(
                        helloworld_pb2.HelloRequest(name='test11', spaninfo=get_span_str(span1)))
                    print("Greeting:", r.message)
                except Exception as e:
                    print(e)

                span1.finish()

                child_span.log_kv({'span.trace_id': child_span.trace_id,
                                   'child_span.span_id': child_span.span_id,
                                   'child_span.parent_id': child_span.parent_id,
                                   'child_span.operation_name': child_span.operation_name,
                                   })

            span.log_kv({'span.trace_id': span.trace_id,
                         'span.span_id': span.span_id,
                         'span.parent_id': span.parent_id,
                         'span.operation_name': span.operation_name,
                         })


async def close(nc):
    await nc.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    nc, c = loop.run_until_complete(main(loop))

    tasks = [req(c) for ii in range(1)]
    # 返回一个列表,内容为各个tasks的返回值
    status_list = loop.run_until_complete(asyncio.gather(*tasks))

    loop.close()
    time.sleep(5)   # yield to IOLoop to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50
    tracer.close()  # flush any buffered spans
