from django.contrib import admin
from Student.models import Studentdetails, Studentmarks
from Userapp.models import UserDetails


admin.site.register(Studentdetails)
admin.site.register(Studentmarks)

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    ordering = ['id']
    

#from Userapp.models import User, UserManager 
#admin.site.register(User)
# admin.site.register(CustomUser)


# @admin.register(UserDetails)
# class UserDetailsAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email', 'password']