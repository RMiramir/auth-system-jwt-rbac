from django.contrib import admin
from .models import User, Role, UserRole, BusinessElement, AccessRoleRule

admin.site.register(User)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(BusinessElement)
admin.site.register(AccessRoleRule)
