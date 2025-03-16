from django.shortcuts import render,get_object_or_404
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rbs.models import Category,Table,Product,Order,OrderItems
from rbs.serializers import CategorySerializer,TableSerializer,ProductSerializer,UserSerializer,OrderSerializer,OrderItemSerializer
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView
from twilio.rest import Client
from decouple import config
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

class OrderCreateView(CreateAPIView):
    serializer_class=OrderSerializer
    def perform_create(self, serializer):
        id=self.kwargs.get("pk")
        table_instance=get_object_or_404(Table,id=id)
        if table_instance.table_status==True:
            table_instance.table_status=False
            table_instance.save()
            serializer.save(table_object=table_instance)
        else:
            raise serializers.ValidationError({"message":"table occupied"})

class OrderItemCreateView(CreateAPIView):
    serializer_class=OrderItemSerializer

    def create(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        order_instance=get_object_or_404(Order,id=id)
        product_id=request.data.get("product_object")
        product_instance=get_object_or_404(Product,id=product_id)
        qty=request.data.get("qty")
        order_item_instance,created=OrderItems.objects.get_or_create(order_object=order_instance,product_object=product_instance)
    
        if created:
            order_item_instance.qty=qty
            order_item_instance.save()
        else:
            order_item_instance.qty+=qty
            order_item_instance.save()

        serializer_instance=OrderItemSerializer(order_item_instance)
        return Response(serializer_instance.data)
    

class OrderRetrieveView(RetrieveAPIView):
    serializer_class=OrderSerializer
    queryset=Order.objects.all()

class GenerateBillView(UpdateAPIView):
    serializer_class=OrderSerializer
    queryset=Order.objects.all()
    def perform_update(self, serializer):
        id=self.kwargs.get("pk")
        order_instance=get_object_or_404(Order,id=id)
        if order_instance.status:
            raise serializers.ValidationError("Bill already generated")
        order_items=OrderItems.objects.filter(order_object=order_instance)
        total=sum([oi.product_object.price * oi.qty for oi in order_items])
        send_invoice_to_whatsapp(order_instance,total)
        serializer.save(status=True,total=total)


def send_invoice_to_whatsapp(order_instance,total):

    account_sid = config("account_sid")
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=f"Order Completed \n order_id: {order_instance.id} \n Your order total is {total}",
    to='whatsapp:+919567372459'
    )
    print(message.sid)
