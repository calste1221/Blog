from django.contrib import admin

# Register your models here.
from app02 import models


class HostInfoAdmin(admin.ModelAdmin):
    list_display = ('HostName', 'IP')
    search_fields = ('HostName', 'IP')
    list_filter = ('HostName', 'IP')
    
    

admin.site.register(models.UserType)
admin.site.register(models.Admin)
admin.site.register(models.Chat)
admin.site.register(models.NewsType)
admin.site.register(models.News)
admin.site.register(models.Reply)