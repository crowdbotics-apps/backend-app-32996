from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet,
    AppViewSet,
    PlanViewSet,
    SubscriptionViewSet
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("password-reset", LoginViewSet, basename="login")
router.register("apps", AppViewSet, basename="app")
router.register("apps/<int:app_id>/?", AppViewSet, basename="app")
router.register("plans", PlanViewSet, basename="plan")
router.register("plans/<int:plan_id>/?", PlanViewSet, basename="plan")
router.register("subscriptions", SubscriptionViewSet, basename="subscription")
router.register("subscriptions/<int:subscription_id>/?", SubscriptionViewSet, basename="subscription")

urlpatterns = [
    path("", include(router.urls)),
]
