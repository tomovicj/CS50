from django.contrib import admin
from .models import User, Redirect, Data

# Register your models here.
admin.site.register(User)
admin.site.register(Redirect)
admin.site.register(Data)
