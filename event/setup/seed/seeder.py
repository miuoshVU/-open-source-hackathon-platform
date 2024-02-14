from dotenv import load_dotenv

from django.contrib.auth.models import Group
from default.models import CustomUser
from organizer.models import FeaturePermission, OrganizerPermission

load_dotenv()

# Create the necessary groups for the users

def create_groups():
    Group.objects.create(name="hacker")
    Group.objects.create(name="organizer")


def create_super_user():
    new_admin=CustomUser.objects.create_superuser(email="admin@gmail.com", password="admin12345")
    new_admin.first_name='Admin'
    new_admin.last_name='Admin'


permissions_list = []


def create_feature_permissions():
    permissions_list.append(FeaturePermission.objects.create(
        url_name='display-hackers', permission_name='h-Hackers'))
    permissions_list.append(FeaturePermission.objects.create(
        url_name='statistics', permission_name='s-Stats'))

def add_organizers_to_features():
    user = CustomUser.objects.get(email='admin@gmail.com')
    head_org = OrganizerPermission.objects.create(user=user)
    head_org.permission.add(permissions_list[0], permissions_list[1])


# site startup code
create_groups()
create_super_user()

create_feature_permissions()
add_organizers_to_features()
