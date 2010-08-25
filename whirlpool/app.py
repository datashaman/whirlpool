import stream, bottle, itertools, model

bottle.debug(True)

templates = dict(
    anchor = '<a href="{0.url}">{0}</a>',
    tr = '<tr><td>{0.login}</td><td>{0.name}</td><td>{0.email}</td></tr>',
    table = '<table>{0}</table>',
    page = '<html><body>{0}</body></html>',
    li = '<li>{0}</li>',
    ul = '<ul>{0}</ul>',
)

class Template(stream.Stream):
    def __init__(self, *names, **variables):
        super(Template, self).__init__()

        self.names = names
        self.variables = variables

    def function(self, inp):
        outp = inp
        for name in self.names: outp = templates[name].format(outp, **self.variables)
        return outp

    def __pipe__(self, inpipe):
        return itertools.imap(self.function, inpipe)

def collect(*names):
    class process(stream.Stream):
        def __pipe__(self, inpipe): return [ inpipe >> Template(*names) ]
    return process()

@bottle.route('/', method='GET')
def root(): return index()

@bottle.route('/:page', method='GET')
def index(page=1):
    users = stream.Stream(model.User.paginate(page))
    return [ ''.join(users >> Template('tr')) ] >> Template('table', 'page')

@bottle.route('show', method='GET')
def show():
    return 'show'

@bottle.route('create', method='POST')
def create():
    return 'create'

@bottle.route('update', method='PUT')
def update():
    return 'update'

@bottle.route('destroy', method='DELETE')
def destroy():
    return 'destroy'

@bottle.route('new', method='GET')
def new():
    return 'new'

@bottle.route('edit', method='GET')
def edit():
    return 'edit'

bottle.run(reloader=True)
