import faker, inspect
from redisco import models

class User(models.Model):
    login = models.Attribute(required=True, unique=True)
    name = models.Attribute(required=True)
    email = models.Attribute(required=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def fake(cls):
        name = faker.name.name()
        obj = cls(login=faker.internet.user_name(name), name=name, email=faker.internet.email(name))
        obj.save()
        return obj

    @property
    def url(self): 
        return '/user/%s' % self.login

    def __repr__(self):
        return '%s: %s &lt;%s&gt;' % (self.login, self.name, self.email)
