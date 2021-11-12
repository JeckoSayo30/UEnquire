from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User

from .forms import RegistrationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *


from typing import Set

from django.utils.translation import ugettext_lazy as _
# Register your models here.

admin.site.site_header = "UEnquire Admin"
admin.site.site_title = "UEnquire Admin Area"
admin.site.index_title = "UEnquire Administration Area"

class intendsAdmin(admin.ModelAdmin):
	list_display = ['tag', 'pattern', 'response', 'context', 'context_set']
	search_fields = ['tag']

class SourceAdmin(admin.ModelAdmin):
	list_display = ['twitter_id', 'source_acct']
	search_fields = ['twitter_id', 'source_acct']

class DataSetsAdmin(admin.ModelAdmin):
	list_display = ['post_id','posts', 'likes', 'dates', 'data', 'tags', 'links']
	search_fields = ['post_id','posts', 'likes', 'dates', 'data', 'tags', 'links']

class AccountAdmin(UserAdmin):
	def get_form(sel, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		is_superuser = request.user.is_superuser
		disabled_fields = set()

		if not is_superuser:
			disabled_fields |= {'is_admin','is_superuser', 'user_permissions', 'groups'}

		if (not is_superuser and obj is not None and obj == request.user):
			disabled_fields |= {
			'is_staff'
			'is_superuser',
			'groups',
			'user_permissions',
			}

		for f in disabled_fields:
			if f in form.base_fields:
				form.base_fields[f].disabled = True
		return form


	list_display = ('email','account_id', 'username','password','date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email', 'username', 'account_id')
	
	readonly_fields = ('account_id', 'date_joined', 'last_login')
	
	# filter_horizontal = ('groups', 'user_permissions',)
	filter_horizontal = ()

	list_filter = ('is_staff', 'is_active', 'is_admin')
	
	fieldsets = (
		(None, {'fields': ('email','username', 'password')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_admin',)}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'username', 'password1', 'password2')}
			),
		)

	#def has_add_permission(self, request, obj=None):  # Can't add users
		#return request.user.is_superuser

	#def has_delete_permission(self, request, obj=None):
		#return request.user.is_superuser

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		user = request.user
		return qs if user.is_superuser else qs.filter(is_admin = False)

admin.site.register(Source, SourceAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Intents, intendsAdmin)
# admin.site.register(DataSets, DataSetsAdmin)
