from django.shortcuts import render


# Created an index view for the room creation and redirection.
def index(request):
    return render(request, 'core/index.html')


# Create the view function for the room view
def room(request, room_name):
    return render(request, 'core/room.html', {'room_name': room_name})
