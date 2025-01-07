from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializer import UserRegisterSerializer,UserLoginSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class UserRegisterViewSet(viewsets.GenericViewSet):
    """用戶註冊"""
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
        
class UserLogoutViewSet(APIView):
    """用戶登出"""
    permission_classes=[IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            refresh_token=request.data.get('refresh')
            if not refresh_token:
                return Response({
                    'success':False,
                    'message':"需要提供 refresh token"
                },status=status.HTTP_400_BAD_REQUEST)
            token=RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {
                    'success':True,
                    'message':"登出成功"
                },status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'success':False,
                    'message':"登出失敗",
                    "error":str(e)
                },status=status.HTTP_400_BAD_REQUEST
            )
class TokenRefreshViewSet(APIView):
    """用戶刷新token"""
    permission_classes=[IsAuthenticated]
    serializer_class=TokenRefreshSerializer
    def post(self, request, *args, **kwargs):
        try:
            refresh_token=request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {
                        'success':False,
                        'message':"需要提供refresh token"
                    },status=status.HTTP_400_BAD_REQUEST
                )
            serializer=self.serializer_class(data={'refresh':refresh_token})
            if serializer.is_valid():
                return Response(
                    {
                        'success':True,
                        'message':"刷新成功",
                        'access':serializer.validated_data['access']
                    },status=status.HTTP_200_OK
                )
            return Response(
                {
                    'success':False,
                    'message':"資料驗證失敗"
                },status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'success':True,
                    'message':"未預期的錯誤",
                    'error':str(e)
                },status=status.HTTP_400_BAD_REQUEST
            )