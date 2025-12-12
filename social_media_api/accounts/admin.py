# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserChangeForm(forms.ModelForm):
    """ModelForm بسيط لواجهة الأدمين يسمح بعرض الحقول الإضافية."""
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    form = CustomUserChangeForm

    # حقول تظهر في قائمة المستخدمين في الأدمين
    list_display = ('username', 'email', 'is_staff', 'is_active', 'get_followers_count')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # الحقول في صفحة التعديل/الإنشاء
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_picture', 'followers'),
        }),
    )

    # لسهولة البحث
    search_fields = ('username', 'email')
    ordering = ('username',)

    # استخدم فلتر أفقي لعلاقة ManyToMany لتسهيل الإضافة/الحذف
    filter_horizontal = DefaultUserAdmin.filter_horizontal + ('followers',)

    def get_followers_count(self, obj):
        return obj.followers.count()
    get_followers_count.short_description = 'Followers'
