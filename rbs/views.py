from django.shortcuts import render,get_object_or_404
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rbs.models import Category,Table,Product
from rbs.serializers import CategorySerializer,TableSerializer,ProductSerializer,UserSerializer
from rest_framework.generics import CreateAPIView
# Create your views here.

class UserCreateView(CreateAPIView):
    serializer_class=UserSerializer

class TableViewSetView(ViewSet):
    serializer_class=TableSerializer

    def list(self,request,*args,**kwargs):
        qs=Table.objects.all()
        serializer_instance=self.serializer_class(qs,many=True)
        return Response(data=serializer_instance.data)
    
    def create(self,request,*args,**kwargs):
        serializer_instance=self.serializer_class(data=request.data)
        
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
    def retrieve(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        qs=get_object_or_404(Table,id=id)
        serializer_instance=self.serializer_class(qs,many=False)
        return Response(data=serializer_instance.data)
    

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        category_object=get_object_or_404(Table,id=id)
        serializer_instance=self.serializer_class(data=request.data,instance=category_object)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
    
        else:
            return Response(data=serializer_instance.errors)
        
    def destroy(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        category_object=get_object_or_404(Table,id=id)
        category_object.delete()
        return Response(data={"message":"deleted"})


class CategoryViewSet(ViewSet):

    serializer_class=CategorySerializer

    def list(self,request,*args,**kwargs):
        qs=Category.objects.all()
        serializer_instance=self.serializer_class(qs,many=True)
        return Response(data=serializer_instance.data)
    
    def create(self,request,*args,**kwargs):
        serializer_instance=self.serializer_class(data=request.data)
        
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
    def retrieve(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        qs=get_object_or_404(Category,id=id)
        serializer_instance=self.serializer_class(qs,many=False)
        return Response(data=serializer_instance.data)
    

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        category_object=get_object_or_404(Category,id=id)
        serializer_instance=self.serializer_class(data=request.data,instance=category_object)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
    
        else:
            return Response(data=serializer_instance.errors)
        
    def destroy(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        category_object=get_object_or_404(Category,id=id)
        category_object.delete()
        return Response(data={"message":"deleted"})
        

class ProductCreateView(CreateAPIView):
    serializer_class=ProductSerializer

    def perform_create(self, serializer):
        id=self.kwargs.get("pk")
        category_instance=get_object_or_404(Category,id=id)
        serializer.save(category_object=category_instance)

class ProductViewSet(ModelViewSet):
    http_method_names=["get","put","destroy"]
    serializer_class=ProductSerializer
    qs=Product.objects.all()

    def get_queryset(self):
        qs=Product.objects.all()
        if "category" in self.request.query_params:
            category_name=self.request.query_params.get("category")
            qs=qs.filter(category_object__name=category_name)
        return qs
