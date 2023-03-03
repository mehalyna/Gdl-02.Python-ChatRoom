from django.contrib import admin

# Register your models here.
# admin.site.register(Project)
# admin.site.register(Blog)
from chat.models import Chat, Message, Role, User

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Chat)
admin.site.register(Message)
