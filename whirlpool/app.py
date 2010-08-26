import stream, bottle, model, itertools

# [model.User.fake() for x in range(1000000)]

bottle.debug(True)

templates = dict(
    tr = '<tr><td><a href="{0.url}">{0.login}</a></td><td>{0.name}</td><td>{0.email}</td></tr>',
    table = '<table>{0}</table>',
    page = '<html><body>{0}</body></html>',
    li = '<li>{0}</li>',
    ul = '<ul>{0}</ul>',
    user = '',
)

PAGE_SIZE = 10

class Template(stream.Stream):
    def __init__(self, *names, **variables):
        super(Template, self).__init__()

        self.names = names
        self.variables = variables

    def function(self, inp):
        for name in self.names: inp = templates[name].format(inp, **self.variables)
        return inp

    def __pipe__(self, inpipe):
        return [ ''.join(map(self.function, inpipe)) ]

@bottle.route('/', method='GET')
def root(): return index()

class Page(stream.Stream):
    def __init__(self, page=1, page_size=PAGE_SIZE):
        self.start, self.end = ((int(page) - 1) * page_size, int(page) * page_size)

    def __call__(self, inpipe):
        return itertools.islice(iter(inpipe), self.start, self.end)

@bottle.route('/:page', method='GET')
def index(page=1):
    query = model.User.objects.order('login')
    return query >> Page(page) >> Template('tr') >> Template('table', 'page')

@bottle.route('show/:id', method='GET')
def show(id):
    query = model.User.objects.get_by_id(id)
    print query.attributes
    return [query] >> Template('user', 'page')

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
