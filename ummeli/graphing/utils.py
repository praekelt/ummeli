from ummeli.graphing.models import Person

def add_connection_for_user(parent, child):
    if parent and child:
        parent_person = Person.objects.get_or_create(user_id=parent.pk)
        parent_person.name = parent.get_profile().fullname()
        parent_person.save()
        
        child_person = Person.objects.get_or_create(user_id=child.pk)
        child_person.name = child.get_profile().fullname()
        child_person.save()
        
        parent_person.knows.add(child_person)
        parent_person.save()
    else:
        raise ValueError("Both parent and child cannont be null.")