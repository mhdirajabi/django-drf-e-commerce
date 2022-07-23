from accounts.models import CustomUser as User
from accounts.models import Profile, TOTPRequest
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import (
    PasswordField,
    TokenObtainPairSerializer,
)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        label="آدرس ایمیل",
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    phone_number = PhoneNumberField(
        label="شماره موبایل",
        required=True,
        help_text="شماره موبایل باید با فرمت ۰۹۱۲۳۴۵۶۷۸۹ وارد شود",
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = PasswordField(label="گذرواژه", validators=[validate_password])
    password2 = PasswordField(
        label="تکرار گذرواژه",
    )

    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "گذرواژه‌های وارد شده منطبق نیستند"}
            )

        return attrs

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(
            label="آدرس ایمیل",
            required=True,
        )
        self.fields["password"] = PasswordField(label="گذرواژه")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number", "first_name", "last_name", "password"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "bio", "profile_pic"]


class RequestTOTPSerializer(serializers.Serializer):
    receiver = serializers.CharField(
        label="شماره موبایل",
        max_length=20,
        allow_null=False,
        help_text="شماره موبایل باید با فرمت ۰۹۱۲۳۴۵۶۷۸۹ وارد شود",
    )
    channel = serializers.ChoiceField(
        allow_null=False, choices=TOTPRequest.TOTPChannel.choices
    )


class RequestTOTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOTPRequest
        fields = ("request_id",)


class VerifyTOTPRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null=False)
    code = serializers.CharField(max_length=4, allow_null=False)
    receiver = serializers.CharField(
        label="شماره موبایل",
        max_length=20,
        allow_null=False,
        help_text="شماره موبایل باید با فرمت ۰۹۱۲۳۴۵۶۷۸۹ وارد شود",
    )


class ObtainJWTSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
