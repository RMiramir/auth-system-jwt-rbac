from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название роли')

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_users')

    class Meta:
        unique_together = (('user', 'role'),)

    def __str__(self):
        return f'{self.user.email} {self.role.name}'


class BusinessElement(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AccessRoleRule(models.Model):


    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='rules')
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE, related_name='rules')

    read_permission = models.BooleanField(default=True)
    read_all_permission = models.BooleanField(default=False)

    create_permission = models.BooleanField(default=True)

    update_permission = models.BooleanField(default=True)
    update_all_permission = models.BooleanField(default=False)

    delete_permission = models.BooleanField(default=True)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        unique_together = (('role', 'element'),)

    def __str__(self):
        return f'{self.role.name} -> {self.element.name}'


class BlacklistedToken(models.Model):

    # Таблица для хранения "отозванных" JWT токенов.

    token = models.TextField()  # сам JWT токен
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.toke