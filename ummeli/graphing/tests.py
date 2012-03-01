from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from neo4django import db
db.DEFAULT_DB_ALIAS = 'test'

from ummeli.graphing.models import Person
from ummeli.graphing.utils import add_connection_for_user

import requests

def cleandb():
    key = getattr(settings, 'NEO4J_DELETE_KEY', None)
    server = getattr(settings, 'NEO4J_DATABASES', None)
    server = server.get(db.DEFAULT_DB_ALIAS, None) if server else None
    
    resp = requests.delete('http://%s:%s/cleandb/%s' %
                           (server['HOST'], str(server['PORT']), key))
    
    if resp.status_code != 200:
        print "\nTest database couldn't be cleared - have you installed the cleandb extension at https://github.com/jexp/neo4j-clean-remote-db-addon?"

cleandb()

class BaseTestCase(TestCase):
    def setUp(self):        
        self.joe = Person.objects.get_or_create(name='Joe', user_id=100)
        self.bob = Person.objects.get_or_create(name='Bob', user_id=200)
        self.alice = Person.objects.get_or_create(name='Alice', user_id=300)
        self.susan = Person.objects.get_or_create(name='Susan', user_id=400)
        self.will = Person.objects.get_or_create(name='Will', user_id=500)
        self.pete = Person.objects.get_or_create(name='Pete', user_id=600)
        
        self.joe.knows.add(self.bob)
        self.joe.knows.add(self.alice)
        self.joe.save()
        
        self.bob.knows.add(self.alice)
        self.bob.knows.add(self.susan)
        self.bob.save()
        
        self.alice.knows.add(self.susan)
        self.alice.knows.add(self.will)
        self.alice.save()
        
        self.will.knows.add(self.joe)
        self.will.save()
        
        self.pete.knows.add(self.will)
        self.pete.save()
        
    def test_model_connections(self):
        self.assertEquals(len(list(self.joe.knows.all())), 2)
        self.assertEquals(len(list(self.joe.is_known.all())), 1)
    
    def test_model_traversal(self):    
        self.assertEquals(len(self.joe.connections()), 3) #depth 1 connections
        self.assertEquals(len(self.joe.connections(2)), 5) #depth 5 connections
        
        self.assertEquals(len(self.pete.connections()), 1) #depth 1 connections
        self.assertEquals(len(self.pete.connections(2)), 3) #depth 5 connections
        
        
class UserConnectionsTestcase(TestCase):    
    def setUp(self):        
        self.tom = User.objects.create_user('tom', 'tom@domain.com','tom123')
        profile = self.tom.get_profile()
        profile.first_name = 'Tom'
        profile.surname = 'Jones'
        profile.save()
        
        self.luke = User.objects.create_user('luke', 'luke@domain.com','luke123')
        profile = self.luke.get_profile()
        profile.first_name = 'Luke'
        profile.surname = 'Warm'
        profile.save()
        
    def test_user_node_creation(self):
        tom = Person.get_and_update(self.tom)
        luke = Person.get_and_update(self.luke)
        
        self.assertEquals(len(tom.connections()), 0)
        
        add_connection_for_user(self.tom, self.luke)
        
        self.assertEquals(len(tom.connections()), 1)
        self.assertEquals(len(luke.connections()), 1)
        
        self.assertTrue(tom.is_connected_to(luke))