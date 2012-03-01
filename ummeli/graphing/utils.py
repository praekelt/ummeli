from ummeli.graphing.models import Person

def add_connection_for_user(parent, child):
    if parent and child:
        parent_person = Person.get_and_update(parent)        
        child_person = Person.get_and_update(child)
        
        parent_person.knows.add(child_person)
        parent_person.save()
    else:
        raise ValueError("Both parent and child cannont be null.")