from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializer import UserRegisterSerializer,UserLoginSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterViewSet(viewsets.GenericViewSet):
    """用戶註冊"""
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes=[AllowAny]

    def create(self, request, *args, **kwargs):
        """建立用戶"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    'success': True,
                    'message': '註冊成功',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'success': False,
                    'message': '註冊失敗',
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'success': False,
            'message': '資料驗證失敗',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
class UserLoginViewSet(APIView):
    """用戶登入"""
    permission_classes=[AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            refresh=RefreshToken.for_user(user)
            return Response({
                    'success': True,
                    'message': '登入成功',
                    'refresh':str(refresh),
                    'access':str(refresh.access_token),
                },status=status.HTTP_200_OK
            )
                
        return Response(
                {
                    'success':False,
                    'message':'登入失敗',
                    'error':serializer.errors
                },status=status.HTTP_400_BAD_REQUEST
            )