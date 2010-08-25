import stream, faker
from elixir import *

metadata.bind = 'sqlite:///data/db.sqlite'
metadata.bind.echo = True

PAGE_SIZE = 10

class Factory:
    @classmethod
    def create(cls, number):
        return stream.repeatcall(cls.fake) >> stream.item[:int(number)]
        
    @classmethod
    def paginate(cls, page=1):
        page = int(page)
        start = int(page - 1) * PAGE_SIZE
        end = page * PAGE_SIZE
        page = cls.query[start:end]
        return page

class User(Entity, Factory):
    login = Field(Unicode(20), primary_key=True)
    name = Field(Unicode(60))
    email = Field(Unicode(128))

    @classmethod
    def fake(cls):
        name = faker.name.name()
        return cls(login=faker.internet.user_name(name), name=name, email=faker.internet.email(name))

    @property
    def url(self): 
        return '/user/%s' % self.login

    def __repr__(self):
        return '%s: %s &lt;%s&gt;' % (self.login, self.name, self.email)

setup_all()
create_all()
