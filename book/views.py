from rest_framework import viewsets
from .models import Book
from .serializer import BookSerializer
from rest_framework.response import Response
from rest_framework import status

#localhost:8000/api/books/
class BookAPI(viewsets.ModelViewSet):
    queryset=Book.objects.all().order_by('created_at')
    serializer_class=BookSerializer
    
    def list(self, request, *args, **kwargs):
        serializer=self.serializer_class(self.queryset,many=True)
        return Response(
            {
                "success":True,
                "data":serializer.data,
                "code":200,
                "message":"success"
                },
            status=status.HTTP_200_OK
            )
    def retrieve(self, request,pk=None, *args, **kwargs):
        data=self.get_object() #自動會去找pk是否存在 否則404
        result=self.serializer_class(data)
        return Response(
            {
                "success":True,
                'data':result.data,
                'code':200,
                'message':'success'
            },
            status=status.HTTP_200_OK
            )
            
    def create(self, request,*args, **kwargs):
        result=self.serializer_class(data=request.data)
        if result.is_valid():
            result.save()
            return Response(
                {
                "success":True,
                "data":result.data,
                "code":201,
                "message":"success"
            },
                status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {
                "success":False,
                "data":result._errors,
                "code":400,
                "message":"Invalid data"
            },
                status=status.HTTP_400_BAD_REQUEST
        )
    def destroy(self, request, pk=None,*args, **kwargs):
        data=self.get_object()
        data.delete()
        return Response(
                {
                    "success":True,
                    "code":204,
                    "message":"Successfully Delete!"
                },
                status=status.HTTP_204_NO_CONTENT
            )
    def partial_update(self, request, pk=None,*args, **kwargs):
        data=self.get_object()
        result=self.serializer_class(data,data=request.data,partial=True)
        if result.is_valid():
            result.save()
            return Response(
                {
                    "success":True,
                    "data":result.data,
                    "code":200,
                    "message":"Successfully update!"
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "success":False,
                    "data":result.errors,
                    "code":400,
                    "message":"Update fail"
                },
                status=status.HTTP_400_BAD_REQUEST
            )