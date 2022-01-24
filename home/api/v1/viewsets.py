from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from home.models import *
from rest_framework import permissions

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
    PasswordSerializer,
    AppSerializer,
    PlanSerializer,
    SubscriptionSerializer
)


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})

class PasswordViewSet(ModelViewSet):
    serializer_class = PasswordSerializer
    http_method_names = ["post"]

class AppViewSet(ModelViewSet):
    # we are telling we have to use AppSerializer for the JSON conversion of AppViewSet
    serializer_class = AppSerializer
    queryset = App.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        token = Token.objects.get(key=request.auth.key)
        apps = App.objects.filter(user=token.user_id)
        return Response(data=AppSerializer(apps, many=True).data)


    def retrieve(self, request, *args, **kwargs):
        app_id = kwargs['pk']
        app = App.objects.filter(id=app_id).first()
        token = Token.objects.get(key=request.auth.key)
        if app is None:
            return Response(data={"message": f"No App found against id {app_id}."}, status=status.HTTP_404_NOT_FOUND)
        if app.user_id != token.user_id:
            return Response(data={"message": f"User is not authorized to retrieve app having id {app_id}."},status=status.HTTP_403_FORBIDDEN)
        return Response(data=AppSerializer(app).data)

    def create(self, request, *args, **kwargs):
        request.data['user'] = Token.objects.get(key=request.auth.key).user_id
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        app_id = kwargs['pk']
        app = App.objects.filter(id=app_id).first()
        token = Token.objects.get(key=request.auth.key)
        if app is None:
            return Response(data={"message": f"No App found to update against id {app_id}."}, status=status.HTTP_404_NOT_FOUND)
        if app.user_id != token.user_id:
            return Response(data={"message": f"User is not authorized to modify app having id {app_id}."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        app_id = kwargs['pk']
        app = App.objects.filter(id=app_id).first()
        token = Token.objects.get(key=request.auth.key)
        if app is None:
            return Response(data={"message": f"No App found to delete against id {app_id}."}, status=status.HTTP_404_NOT_FOUND)
        if app.user_id != token.user_id:
            return Response(data={"message": f"User is not authorized to retrieve app having id {app_id}."}, status=status.HTTP_403_FORBIDDEN)
        App.objects.filter(id=app_id).delete()
        return Response(data={"message": f"App deleted successfully."})


class PlanViewSet(ModelViewSet):
    # we are telling we have to use PlanSerializer for the JSON conversion of PlanViewSet
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    http_method_names = ["get"]
    permission_classes = (permissions.IsAuthenticated,)


class SubscriptionViewSet(ModelViewSet):
    # we are telling we have to use SubscriptionSerializer for the JSON conversion of SubscriptionViewSet
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "post", "put"]


    def list(self, request, *args, **kwargs):
        token = Token.objects.get(key=request.auth.key)
        subscriptions = Subscription.objects.filter(user=token.user_id)
        return Response(data=SubscriptionSerializer(subscriptions, many=True).data)

    def retrieve(self, request, *args, **kwargs):
        subscription_id = kwargs['pk']
        subscription = Subscription.objects.filter(id=subscription_id).first()
        token = Token.objects.get(key=request.auth.key)
        if subscription is None:
            return Response(data={"message": f"No subscription found against id {subscription_id}."}, status=status.HTTP_404_NOT_FOUND)
        if subscription.user_id != token.user_id:
            return Response(data={"message": f"User is not authorized to retrieve subscription having id {subscription_id}."},status=status.HTTP_403_FORBIDDEN)
        return Response(data=SubscriptionSerializer(subscription).data)

    def create(self, request, *args, **kwargs):
        # active user id
        request.data['user'] = Token.objects.get(key=request.auth.key).user_id
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return super().create(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        subscription_id = kwargs['pk']
        subscription = Subscription.objects.filter(id=subscription_id).first()
        token = Token.objects.get(key=request.auth.key)
        if subscription is None:
            return Response(data={"message": f"No subscription found against id {subscription_id}."}, status=status.HTTP_404_NOT_FOUND)
        if subscription.user_id != token.user_id:
            return Response(data={"message": f"User is not authorized to update subscription having id {subscription_id}."}, status=status.HTTP_403_FORBIDDEN)
        request.data['user'] = token.user_id
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return super().update(request, *args, **kwargs)