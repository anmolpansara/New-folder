# import datetime

# from django.contrib.auth.models import BaseUserManager

# from blogapp import (
#     get_country_code,
#     get_country_currency_code,
# )

# class UserManager(BaseUserManager):
#     def create_user(
#         self,
#         email,
#         phone=None,
#         password=None,
#         first_name=None,
#         last_name=None,
#         fcm_token=None,
#         role=None,
#         is_online=None,
#         birth_date=None,
#         birth_time=None,
#         profile_pic=None,
#         country_code=None,
#         gender=None,
#         third_party_token=None,
#         *args,
#         **kwargs,
#     ):
#         # if not phone:
#         #     raise ValueError("User must have a phone number")
#         if super().get_queryset().filter(email=email):
#             raise ValueError("User with this email already exists")
#         balance = 0
#         country = get_country_code(phone)
#         balance_currency = get_country_currency_code(phone)
#         print("balance_currency: ", balance_currency)
#         user = self.model(
#             phone=phone,
#             password=password,
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             role=role,
#             last_login=datetime.datetime.now(),
#             fcm_token=fcm_token,
#             is_online=is_online,
#             country=country,
#             gender=gender,
#             balance=balance,
#             balance_currency=balance_currency,
#             birth_date=birth_date,
#             birth_time=birth_time,
#             profile_pic=profile_pic,
#             country_code=country_code,
#             third_party_token=third_party_token,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(
#         self,
#         email,
#         phone,
#         password=None,
#         role="admin",
#         first_name=None,
#         last_name=None,
#     ):
#         user = self.create_user(phone=phone, password=password, email=email, role=role,first_name=first_name,last_name=last_name)
#         user.is_active = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

#     def create(self, **kwargs):
#         return self.model.objects.create_user(**kwargs)
