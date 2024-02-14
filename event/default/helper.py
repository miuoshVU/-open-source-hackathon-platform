from django.contrib.auth.models import Group

def decide_redirect(user):
    if user.groups.filter(name='hacker').exists(): 
        return "hacker-dash"
    elif user.groups.filter(name='organizer').exists(): 
        return "organizer-dash"
    else:
        return "organizer-dash"


def decide_type(user):
    if user.groups.filter(name='hacker').exists(): 
        return "hacker"
    elif user.groups.filter(name='organizer').exists(): 
        return "organizer"
    else:
        return "head-organizer"


def add_group(user, group_name):
    user.groups.add(Group.objects.get(name=group_name))

def remove_group(user, group_name):
    user.groups.remove(Group.objects.get(name=group_name))