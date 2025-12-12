# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer لعرض بيانات المستخدم (مقروء فقط الحقول الحسّاسة).
    لا نعرض كلمة المرور هنا.
    نعرض المتابعين كقائمة أسماء مستخدمين.
    """
    followers = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "profile_picture", "followers"]
        read_only_fields = ["id", "followers"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer لإنشاء مستخدم جديد.
    يطلب حقلين password و password2 للمطابقة.
    يتحقق من صلاحية كلمة المرور باستخدام validate_password.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="هذا البريد مستخدم بالفعل.")]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="اسم المستخدم مستخدم بالفعل.")]
    )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2", "bio", "profile_picture"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError({"password": "كلمتا المرور غير متطابقتين."})
        # run Django's password validators
        validate_password(attrs.get("password"), user=None)
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)
        password = validated_data.pop("password")
        # Use create_user to ensure any custom create logic is respected
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer مبسّط لعرض/تحديث بروفايل المستخدم (يستخدم في ProfileView).
    لا يسمح بتعديل الحقول المحمية مثل username عبر هذا المسلسل إن لم تُدرج في الـ view.
    """
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username")

    class Meta:
        model = User
        fields = ["username", "email", "bio", "profile_picture", "followers"]
        read_only_fields = ["username", "email", "followers"]
