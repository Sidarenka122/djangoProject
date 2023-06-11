from django.contrib import admin
from .models import Photo, House, Announcement, Message

admin.site.register(Announcement)
admin.site.register(House)
admin.site.register(Photo)
admin.site.register(Message)
