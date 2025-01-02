from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserRegisterSerializer(serializers.ModelSerializer):
    """序列化用戶資訊"""
    class Meta:
        model=get_user_model() #會去settings.py中找到該模型
        fields=('username','email','password')
        extra_kwargs={'password': {'write_only': True,'style': {'hide_input': True}}} #設置密碼只能寫入
    def validate_username(self, value):
        if len(value)<8 or len(value)>16:
            raise serializers.ValidationError("用戶名長度需至少8~16位數")
        return value 
    def validate_password(self, value):
        """此方法的命名很重要 開頭需要用validate_ 後面是屬性名稱 如果開頭不是validate_ 就要自己額外再Create裡面去判斷對應的Method是否是Valid 且_後面的是屬性名稱 會去field中找到對應的屬性 如果沒有就會报錯"""
        
        if len(value)<8 or len(value)>16:
            raise serializers.ValidationError("密碼長度需至少8~16位數")
        
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("密碼必須包含數字")
        
        if not any(c.islower() for c in value):
            raise serializers.ValidationError("密碼必須包含小寫字母")
        
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("密碼必須包含大寫字母")
        return value
        
    def create(self, validated_data):
        """建立用戶"""
        return get_user_model().objects.create_user(**validated_data) #** 代表解包

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        # 額外的登入特定驗證
        username = data.get('username')
        password = data.get('password')

        # 檢查帳號是否存在
        try:
            user = get_user_model().objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError("密碼錯誤")
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("帳號不存在")
        data['user']=user
        return data