from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from home.models import *
from rest_framework import permissions

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
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


class AppViewSet(ModelViewSet):
    # we are telling we have to use AppSerializer for the JSON converstion of AppViewSet
    serializer_class = AppSerializer
    queryset = App.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(key=request.auth.key)
            apps = App.objects.filter(user=token.user_id)
            return Response(data=AppSerializer(apps, many=True).data)
        except:
            return Response(data={"message": f"Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            app_id = kwargs['pk']
            app = App.objects.filter(id=app_id).first()
            token = Token.objects.get(key=request.auth.key)
            if app is None:
                return Response(data={"message": f"No App found against id {app_id}."}, status=status.HTTP_404_NOT_FOUND)
            if app.user_id != token.user_id:
                return Response(data={"message": f"User is not authorized to retrieve app having id {app_id}."},status=status.HTTP_403_FORBIDDEN)
            return Response(data=AppSerializer(app).data)
        except:
            return Response(data={"message": f"Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            request.data['user'] = Token.objects.get(key=request.auth.key).user_id
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            return super().create(request, *args, **kwargs)
        except:
            return Response(data={"message": f"Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
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
        except:
            return Response(data={"message": f"Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            app_id = kwargs['pk']
            app = App.objects.filter(id=app_id).first()
            token = Token.objects.get(key=request.auth.key)
            if app is None:
                return Response(data={"message": f"No App found to delete against id {app_id}."}, status=status.HTTP_404_NOT_FOUND)
            if app.user_id != token.user_id:
                return Response(data={"message": f"User is not authorized to retrieve app having id {app_id}."}, status=status.HTTP_403_FORBIDDEN)
            App.objects.filter(id=app_id).delete()
            return Response(data={"message": f"App deleted successfully."})
        except :
            return Response(data={"message": f"Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlanViewSet(ModelViewSet):
    # we are telling we have to use AppSerializer for the JSON converstion of AppViewSet
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    http_method_names = ["get"]
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        try:
            plan_id = kwargs.get('pk')
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return Response(data={"message": f"No plan found against id {plan_id}."}, status=status.HTTP_404_NOT_FOUND)


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "post", "put"]


    def list(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(key=request.auth.key)
            subscriptions = Subscription.objects.filter(user=token.user_id)
            return Response(data=SubscriptionSerializer(subscriptions, many=True).data)
        except:
            return Response(data={"message": f"Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            subscription_id = kwargs['pk']
            subscription = Subscription.objects.filter(id=subscription_id).first()
            token = Token.objects.get(key=request.auth.key)
            if subscription is None:
                return Response(data={"message": f"No subscription found against id {subscription_id}."}, status=status.HTTP_404_NOT_FOUND)
            if subscription.user_id != token.user_id:
                return Response(data={"message": f"User is not authorized to retrieve subscription having id {subscription_id}."},status=status.HTTP_403_FORBIDDEN)
            return Response(data=SubscriptionSerializer(subscription).data)
        except:
            return Response(data={"message": f"Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            # override user id which is creating user
            request.data['user'] = Token.objects.get(key=request.auth.key).user_id
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            return super().create(request, *args, **kwargs)
        except:
            return Response(data={"message": f"Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            print(e)
            return Response(data={"message": f"Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
