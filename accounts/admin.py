from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # to make the passwrod read only
from accounts.models import Account
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name','last_name','date_joined','last_login','is_active')

    list_display_links=('email','first_name','last_name') # to access the even from last and first name in admin panel
    readonly_fields= ('last_login','date_joined')
    ordering=('-date_joined',)#shows in decesning order and , is necessary
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account,AccountAdmin)