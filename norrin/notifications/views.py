from django.shortcuts import render
from django.views.generic import View

class StatusView(view):

    def get(self, request, *args, **kwargs):
        return render(request, 'notifications/status.html')
