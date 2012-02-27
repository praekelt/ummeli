from neo4django.db import models
import neo4django
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client

class Person(models.NodeModel):
    user_id = models.IntegerProperty(indexed=True)
    name = models.StringProperty()
    knows = models.Relationship('Person',
                                      rel_type = neo4django.All.KNOWS,
                                      related_name = 'is_known')
    
    def __unicode__(self):  # pragma: no cover
        return '%s[%s]' % (self.name, self.user_id)
    
    def connections(self, depth=1):
        return [Person.objects.get(user_id=node.properties['user_id']) \
            for node in self.node.traverse(types=[client.All.KNOWS], stop=depth)]
