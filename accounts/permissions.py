from .models import UserRole, AccessRoleRule, BusinessElement


def check_permissions(user, element_name, action):

    if not user:
        return False

    try:
        element = BusinessElement.objects.get(name=element_name)
    except BusinessElement.DoesNotExist:
        return False

    user_roles = UserRole.objects.filter(user=user)

    for user_role in user_roles:
        role = user_role.role

        try:
            rule = AccessRoleRule.objects.get(role=role, element=element)
        except AccessRoleRule.DoesNotExist:
            continue

        if action == "read" and rule.read_permission:
            return True

        if action == "create" and rule.create_permission:
            return True

        if action == "update" and rule.update_permission:
            return True

        if action == "delete" and rule.delete_permission:
            return True

    return False


def is_admin(user):
    if not user:
        return False

    return user.user_roles.filter(role_name="admin").exists()
