from .models import User

def create_user(username):
    user = User(username=username)
    user.save()
    return user

user = User.objects.get(serial_number=1)