import stream, faker, bottle, itertools

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return 'User: %s <%s>' % (self.name, self.email)

def UserFactory():
    while True:
        yield User(faker.name.name(), faker.internet.email())

bottle.debug(True)

tuples = {}

templates = dict(
    row = '<tr><td><a href="#">{0.name} &lt;{0.email}&gt;</a></td></tr>',
    table = '<table>{0}</table>',
    page = '<html><body>{0}</body></html>',
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
        return ''.join(itertools.imap(self.function, inpipe))

@bottle.route('/', method='GET')
def index():
    users = UserFactory()
    return [ stream.repeatcall(users.next) >> stream.item[:20] >> Template('row') ] >> Template('table', 'page')

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
