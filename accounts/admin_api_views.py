from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import is_admin
from accounts.models import AccessRoleRule, Role, BusinessElement, User, UserRole


class CreateRoleView(APIView):

    def post(self, request):

        if not is_admin(request.custom_user):
            return Response({"error": "Только админ"}, status=403)

        name = request.data.get("name")

        role = Role.objects.create(name=name)

        return Response({
            "message": "Роль создана",
            "role": role.name
        })


class CreateElementView(APIView):

    def post(self, request):

        if not is_admin(request.custom_user):
            return Response({"error": "Только админ"}, status=403)

        name = request.data.get("name")

        element =BusinessElement.objects.create(name=name)

        return Response({
            "message": "Элемент создан",
            "element": element.name
        })


class SetPermissionView(APIView):

    def post(self, request):

        if not is_admin(request.custom_user):
            return Response({"error": "Только админ"}, status=403)

        role_id = request.data.get("role_id")
        element_id = request.data.get("element_id")

        rule = AccessRoleRule.objects.create(
            role_id=role_id,
            element_id=element_id,

            read_permission=request.data.get("read", False),
            create_permission=request.data.get("create", False),
            update_permission=request.data.get("update", False),
            delete_permission=request.data.get("delete", False),
        )

        return Response({"message": "Права установлены"})


class AssignRoleView(APIView):

    def post(self, request):

        if not is_admin(request.custom_user):
            return Response({"error": "Только админ"}, status=403)

        user_id = request.data.get("user_id")
        role_id = request.data.get("role_id")

        user = User.objects.get(id=user_id)
        role = Role.objects.get(id=role_id)

        UserRole.objects.create(user=user, role=role)

        return Response({"message": "Роль назначена"})