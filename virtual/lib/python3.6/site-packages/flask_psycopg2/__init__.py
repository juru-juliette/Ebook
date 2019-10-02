import psycopg2

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


SCHEMES = set(['postgresql', 'postgres', 'pgsql'])


class Psycopg2(object):
    def __init__(self, app=None, **kwargs):
        self.init_db_func = kwargs.pop('init_db_func', None)
        self._connection_kwargs = kwargs
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app, **kwargs):
        self.app = app
        self.init_db_func = kwargs.pop('init_db_func', self.init_db_func)
        self._connection_kwargs.update(kwargs)
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(self.app, 'teardown_appcontext'):
            self.app.teardown_appcontext(self.teardown)
        else:
            self.app.teardown_request(self.teardown)
        if self.init_db_func is not None:
            self.init_db(self.init_db_func)

    def init_db(self, init_db_func):
        if not self.app:
            raise TypeError('app has not been initialized')
        if not callable(init_db_func):
            raise TypeError('init_db_func is not callable')
        conn = self.connect()
        init_db_func(conn)
        conn.close()

    def connect(self):
        uri = self.app.config.get('PSYCOPG2_DATABASE_URI')
        if uri is None:
            return psycopg2.connect(**self._connection_kwargs)
        r = urlparse(uri)
        if r.scheme.lower() not in SCHEMES:
            raise ValueError('scheme must be one of %s.' % ', '.join(SCHEMES))
        kwargs = {
            'user': r.username,
            'password': r.password,
            'host': r.hostname,
            'port': r.port,
            'database': r.path[1:]
        }
        kwargs.update(self._connection_kwargs)
        return psycopg2.connect(**kwargs)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'postgresql_db'):
            if not ctx.postgresql_db.closed:
                ctx.postgresql_db.close()

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'postgresql_db'):
                ctx.postgresql_db = self.connect()
            return ctx.postgresql_db
