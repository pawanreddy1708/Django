from .utils import Util
from .serializers import WishListSerializer,ProductSerializer
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    GenericAPIView, ListAPIView, DestroyAPIView
from user.models import User
from psycopg2 import OperationalError
from rest_framework.exceptions import ValidationError
from .models import WishList, Cart, Products, Order
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.filters import SearchFilter


class ProductCreateAPI(ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    queryset = Products.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save()
            return Response({'response':'Product added successfully'},status=status.HTTP_201_CREATED)
        except OperationalError as e:
            return Response({'response':'Could not add the product to DB'},status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'response':'Invalid data'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            all= self.get_queryset()
            serializer = ProductSerializer(all,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except OperationalError as e:
            return Response({'response':'could not fetch the products from DB'},status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'response':'Invalid data'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class ProductOperationsAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = "id"
    queryset = Products.objects.all()

    def perform_destroy(self, instance):
        try:
            instance.delete()
            return Response({'response':f'Instance with ID {instance.id} is deleted'},status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'response':'Invalid Data'},status=status.HTTP_400_BAD_REQUEST)
        except OperationalError as e:
            return Response({'response':'Could not connect to DB'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'response':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        try:
            serializer.save()
            return Response({'response':'Updated!'},status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'response':'Invalid Data'},status=status.HTTP_400_BAD_REQUEST)
        except OperationalError as e:
            return Response({'response':'Could not connect to DB'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'response':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class AddToCartAPI(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def post(self, request, id):
        quantity = int(request.data.get('quantity'))
        try:
            owner = User.objects.get(id=self.request.user.id)
            product = Products.objects.get(id=id)
            if quantity <= product.quantity and quantity !=0:
                obj, created = Cart.objects.get_or_create(owner=owner)
                obj.products.add(product)
                obj.quantity=quantity
                obj.save()
            else:
                return Response({'response':'Requested quantity not available'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'resposne':'Added to cart'},status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'response':'Invalid Data'},status=status.HTTP_400_BAD_REQUEST)
        except OperationalError as e:
            return Response({'response':'Could not connect to DB'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(str(e))
            return Response({'response':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,id):
        try:
            quantity = int(request.data.get('quantity'))
            owner = User.objects.get(id=self.request.user.id)
            product = Products.objects.get(id=id)

            if quantity <= product.quantity and quantity !=0:
                obj = Cart.objects.get(owner=owner)
                obj.products = product
                obj.quantity = quantity
                obj.save()
            else:
                return Response({'response':'Requested quantity not available'},status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'response':'Invalid Data'},status=status.HTTP_400_BAD_REQUEST)
        except OperationalError as e:
            print(e)
            return Response({'response':'Could not connect to DB'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'response':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)

class SearchProductsAPI(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields=['^brand','^model']
    queryset = Products.objects.all()
    def get_queryset(self):
        try:
            search_key = self.kwargs['item']
            return Products.objects.filter(Q(brand__contains=search_key)|Q(model__contains=search_key))
        except OperationalError as e:
            return Response({'response':'Could not connect to DB'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'response': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class DisplayBySortedProducts(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    def get_order_type(self, key):
        types = {
            'price-asc':'price','price-desc':'-price','brand-asc':'brand','brand-desc':'-brand',
            'model-asc':'model','model-desc':'-model','quantity-asc':'quantity','quantity-desc':'-quantity'
        }
        return types[key]

    def get_queryset(self):
        try:
            type = self.kwargs['type']
            value = self.get_order_type(type)
            return Products.objects.all().order_by(value)
        except OperationalError as e:
            return Response({'Message': 'Failed to connect with the database'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Message': 'Error Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class PlaceOrderAPI(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request,id):
        total_price = 0
        total_items = 0
        try:
            owner = self.request.user
            order, created = Order.objects.get_or_create(owner_id=owner.id)
            address = request.data.get('address')
            phone = request.data.get('phone')
            cart = Cart.objects.filter(owner_id=owner.id)
            owner = User.objects.get(id=self.request.user.id)

            if cart:
                cart_list=cart.values('products')

                for items in range(len(cart_list)):
                    product_id = cart_list[items]['products']
                    product = Products.objects.get(id=product_id)
                    cart_object = Cart.objects.get(products=product)
                    order.products.add(product)
                    order.save()
                    total_price = total_price + (product.price * cart_object.quantity)
                    total_items = total_items + 1
                    cart_object.delete()
                order.total_price = total_price
                order.total_items = total_items
                order.address = address
                order.phone = phone
                order.save()
                email_body = f"Hi {owner.username} your order with id: {order.id} has been placed successfully" \
                             f"\nTotal items are {total_items}" \
                             f"\nTotal Price is: {total_price}"
                data = {
                    "email_body":email_body,
                    "email_subject":"Order placed",
                    "to_email":[owner.email]
                }
                Util.send_mail(self,data=data)
                return Response({'response':'order placed successfully'},status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'response': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        except OperationalError as e:
            return Response({'response': 'Could not connect to DB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            return Response({'response': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class AddWishListAPI(ListCreateAPIView,DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WishListSerializer
    pagination_class = PageNumberPagination
    lookup_field = "id"

    def post(self,request,id):
        try:
            owner = self.request.user
            obj,created = WishList.objects.get_or_create(owner=owner)
            Product =Products.objects.get(id=id)
            obj.products.add(Product)
            print("before save")
            obj.save()
            print("after save")
            return Response({'response':'Added to Wishlist'},status=status.HTTP_201_CREATED)
        except OperationalError as e:
            return Response({'response': 'Could not connect to DB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            return Response({'response':'Invalid Data'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        try:
            owner = User.objects.get(id=self.request.user.id)
            return WishList.objects.filter(owner=owner)
        except OperationalError as e:
            return Response({'response': 'Could not connect to DB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            return Response({'response': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, id):
        try:
            owner = User.objects.get(id=self.request.user.id)
            product = Products.objects.get(id=id)
            obj=WishList.objects.filter(owner=owner.id)
            if obj:
                obj.delete()
                return Response({'response':'deleted item from wish list'},status=status.HTTP_200_OK)
            else:
                return Response({'response':'Invalid Id to delete'},status=status.HTTP_400_BAD_REQUEST)
        except OperationalError as e:
            return Response({'response': 'Could not connect to DB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            return Response({'response': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'response': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

