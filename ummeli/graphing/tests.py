from django.test import TestCase
from ummeli.graphing.models import Person
from neo4django.db import models
from neo4jrestclient import client

class BaseTestCase(TestCase):
    
    def setUp(self):
        self.joe = Person.objects.get_or_create(name='Joe', user_id=1)
        self.bob = Person.objects.get_or_create(name='Bob', user_id=2)
        self.alice = Person.objects.get_or_create(name='Alice', user_id=3)
        self.susan = Person.objects.get_or_create(name='Susan', user_id=4)
        self.will = Person.objects.get_or_create(name='Will', user_id=5)
        self.pete = Person.objects.get_or_create(name='Pete', user_id=6)
        
        if len(list(self.joe.connections_made.all())) == 0:
            self.joe.connections_made.add(self.bob)
            self.joe.connections_made.add(self.alice)
            self.joe.save()
            
            self.bob.connections_made.add(self.alice)
            self.bob.connections_made.add(self.susan)
            self.bob.save()
            
            self.alice.connections_made.add(self.susan)
            self.alice.connections_made.add(self.will)
            self.alice.save()
            
            self.will.connections_made.add(self.joe)
            self.will.save()
            
            self.pete.connections_made.add(self.will)
            self.pete.save()
        
    def test_model_connections(self):
        self.assertEquals(len(list(self.joe.connections_made.all())), 2)
        self.assertEquals(len(list(self.joe.connections_received.all())), 1)
    
    def test_model_traversal(self):    
        self.assertEquals(len(self.joe.connections()), 3) #depth 1 connections
        self.assertEquals(len(self.joe.connections(2)), 5) #depth 5 connections
        
        self.assertEquals(len(self.pete.connections()), 1) #depth 1 connections
        self.assertEquals(len(self.pete.connections(2)), 3) #depth 5 connections
        
        