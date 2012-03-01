from neo4django.db import models
import neo4django
from neo4jrestclient import client

class Person(models.NodeModel):
    user_id = models.IntegerProperty(indexed=True)
    name = models.StringProperty()
    knows = models.Relationship('Person',
                                  rel_type = neo4django.Outgoing.KNOWS,
                                  related_name = 'is_known')
    
    def __unicode__(self):  # pragma: no cover
        return '%s[%s]' % (self.name, self.user_id)
    
    def is_connected_to(self, person):
        uid = int(person.user_id)
        return any(connection.user_id == uid for connection in self.connections())
    
    def connections(self, depth=1):
        return [Person._neo4j_instance(node) \
            for node in self.node.traverse(types=[client.All.KNOWS], stop=depth)]
            
    @classmethod
    def get_and_update(cls, user):
        person = cls.objects.get_or_create(user_id=user.pk)
        person.name = user.get_profile().fullname()
        person.save()
        return person
