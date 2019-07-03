import logging
import random
import os
import time
from jaeger_client import Config
from jaeger_client import Span, SpanContext

if __name__ == "__main__":

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='your-app-name',
        validate=True,
    )
    # this call also sets opentracing.tracer
    tracer = config.initialize_tracer()

    randomnize = random.Random(time.time() * (os.getpid() or 1))

    span_id1 = randomnize.getrandbits(64)

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

    time.sleep(5)   # yield to IOLoop to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50
    tracer.close()  # flush any buffered spans
