from django.core.mail import EmailMessage
from user.models import User
from datetime import datetime, timedelta
from psycopg2 import OperationalError
from .models import Order
from rest_framework.exceptions import ValidationError
from celery import shared_task


class Util:
    @shared_task
    def send_mail(self,data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=data['to_email']
        )
        email.send()

    @shared_task
    def send_delivery_amil(self,email):
        try:
            orders = Order.objects.filter(is_delivered=False)
            if orders:
                order_list = orders.values('id')
                for order in range(len(order_list)):
                    order_id = order_list[order]['id']
                    order_obj = Order.objects.get(id=order_id)
                    user = User.objects.get(id=order_obj.owner_id)
                    order_time = order.obj.created_date
                    if datetime.now() - order_time.replace(tzinfo=None) > timedelta(hours=24):
                        email_body= 'Hi ' + user.username +" your order has been delivered successfully"
                        data = {"email_body":email_body,'to_email':user.email,"email_subject":"Order Delivered"}

                        self.send_mail(data)
                        order_obj.is_delivered = True
                        order_obj.save()
        except OperationalError as e:
            print(e)
        except ValidationError as e:
            print(e)
        except Exception as e:
            print(e)
