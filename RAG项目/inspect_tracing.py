import langchain_core
print('version', langchain_core.__version__)
print([name for name in dir(langchain_core) if 'trace' in name.lower()])
import inspect
print('tracers', [name for name in dir(langchain_core) if 'tracer' in name.lower()])
try:
    import langchain_core.tracing as tracing
    print('has tracing module', tracing)
    print(dir(tracing))
except Exception as e:
    print('no tracing module', e)
