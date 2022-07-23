from accounts.models import CustomUser as User
from accounts.models import Profile, TOTPRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import PhoneNumberVerificationPermission
from .serializers import (
    LoginSerializer,
    ObtainJWTSerializer,
    ProfileSerializer,
    RegisterSerializer,
    RequestTOTPResponseSerializer,
    RequestTOTPSerializer,
    VerifyTOTPRequestSerializer,
)

# Create your views here.


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, PhoneNumberVerificationPermission)

    def permission_denied(self, request, message=None, code=None):
        message = "لطفاً پیش از ورود به حساب کاربری شماره موبایل خود را تأیید کنید"
        return super().permission_denied(request, message, code)


class ProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]


class GetTOTPRequestIDView(APIView):
    @swagger_auto_schema(request_body=RequestTOTPSerializer)
    def post(self, request):
        serializer = RequestTOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            phone_number = data["receiver"]
            if not User.objects.filter(phone_number=phone_number).exists():
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data="کاربری با شماره تلفن وارد شده شناسایی نشد.",
                )
            totp = TOTPRequest.objects.generate(data)
            return Response(data=RequestTOTPResponseSerializer(totp).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class ValidateTOTPView(APIView):
    @swagger_auto_schema(request_body=VerifyTOTPRequestSerializer)
    def post(self, request):
        serializer = VerifyTOTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if TOTPRequest.objects.is_valid(
                data["receiver"],
                data["request_id"],
                data["code"],
            ):
                return Response(self._handle_login(data))
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data="کد اشتباه است."
                )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def _handle_login(self, totp):
        query = User.objects.filter(phone_number=totp["receiver"])
        if query.exists():
            user = query.first()
            user.passed_phone_number_verification = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return ObtainJWTSerializer(
                {
                    "refresh": str(refresh),
                    "token": str(refresh.access_token),
                }
            ).data
