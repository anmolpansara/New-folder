from datetime import datetime, timedelta

from django.db.models import DateField, DateTimeField, ForeignKey, ManyToManyField, Q
from django.shortcuts import get_object_or_404

# from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blogapp.customs.paginations import CustomPageNumberPagination
from blogapp.utilities.swaggers import (  # limit,; page,
    end_date,
    filter,
    page_length,
    search,
    start_date,
)
from blogapp.utilities.utils import capitalize_key


# @method_decorator(
#     name="list",
#     decorator=swagger_auto_schema(
#         manual_parameters=[page, limit, search],
#         operation_description="description from swagger_auto_schema via method_decorator",
#     ),
# )
class CustomViewSet(ModelViewSet, CustomPageNumberPagination, SearchFilter):
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        response = {
            "message": "Created Succesfully",
            "data": serializer.data,
            "status": status.HTTP_201_CREATED,
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.get_queryset(request))
        response = {
            "data": self.get_serializer(self.get_object(request)).data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        results = super().paginate_queryset(
            queryset=super().filter_queryset(queryset=self.get_queryset()),
        )
        results = self.get_serializer(results, many=True).data
        response = {"results": results, "status": status.HTTP_200_OK}
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object(request)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = {
            "message": "Updated Succesfully",
            "data": serializer.data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(request)
        self.perform_destroy(instance)
        response = {
            "message": "Deleted Succesfully",
            "data": "deleted",
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)


class CustomViewSetMaster(ModelViewSet, CustomPageNumberPagination, SearchFilter):
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter]

    def get_object(self, request):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset(request))

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            response = {
                "message": "Created Succesfully",
                # "data": serializer.data,
                "status": True,
            }
            return Response(response, status=status.HTTP_200_OK, headers=headers)
        first_error_key = next(iter(serializer.errors))
        print(str(first_error_key), serializer.errors[first_error_key])
        first_error_value = str(serializer.errors[first_error_key][0])
        # first_error_key = capitalize_key(first_error_key)

        error_message = f"{first_error_key}: {first_error_value}"
        response = {"message": error_message, "status": False}
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = {
            "data": self.get_serializer(self.get_object(request)).data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[search, filter, start_date, end_date, page_length],
        operation_description="list api",
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)
        total_count = queryset.all().count()
        pagination = request.GET.get("pagination", True)
        filter = request.GET.getlist("filter", [])
        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)
        start_rate = request.GET.get("start_rate", None)
        end_rate = request.GET.get("end_rate", None)
        if start_date:
            print("start_date: ", start_date)
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            filter_by = "{0}__{1}".format("created_at", "gte")
            filter_value = start_date
            kwargs[filter_by] = filter_value
            queryset = queryset.filter(Q(**kwargs, _connector=Q.AND)).distinct()
        if end_date:
            print("end_date: ", end_date)
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if start_date and start_date == end_date:
                end_date = end_date + timedelta(days=1)
            filter_by = "{0}__{1}".format("created_at", "lte")
            filter_value = end_date
            kwargs[filter_by] = filter_value
            queryset = queryset.filter(Q(**kwargs, _connector=Q.AND)).distinct()
        if start_rate:
            currency = str(request.user.balance.currency).lower()
            filter_by = "{0}__{1}".format(f"rate_{currency}", "gte")
            filter_value = start_rate
            kwargs[filter_by] = filter_value
            queryset = queryset.filter(Q(**kwargs, _connector=Q.AND)).distinct()
        if end_rate:
            currency = str(request.user.balance.currency)
            filter_by = "{0}__{1}".format(f"rate_{currency}", "lte")
            filter_value = end_rate
            kwargs[filter_by] = filter_value
            queryset = queryset.filter(Q(**kwargs, _connector=Q.AND)).distinct()
        print("kwargs: ", kwargs)
        kwargs = {}
        if filter:
            list_filter_fields = [
                "category",
            ]
            for i in filter:
                filter_value = request.GET.get(i)
                if filter_value:
                    try:
                        model = queryset.model
                        field = model._meta.get_field(i)
                        print("field: ", field)
                        # if filter_value in self.filter_fields:
                        #     filter_by = "{0}__{1}".format(f"{i}", "id")
                        if isinstance(field, ForeignKey):
                            if i in list_filter_fields and filter_value:
                                filter_by = "{0}__{1}".format(f"{i}", "contains")
                                filter_value = filter_value.split(",")
                            else:
                                model = queryset.model._meta.get_field(i).related_model
                                first_field = model._meta.fields[1].name
                                # filter_by = "{0}__{1}".format(f"{i}__{first_field}", "icontains")
                                filter_by = "{0}__{1}".format(f"{i}", "id")
                        elif isinstance(field, DateTimeField):
                            print("field: ", field)
                            filter_by = "{0}__{1}".format(i, "range")
                            filter_value = filter_value.split(" ")
                            filter_value[1] = datetime.strptime(
                                filter_value[1], "%Y-%m-%d"
                            ) + timedelta(days=1)
                            print("filter_value[1]: ", filter_value[1])
                        elif isinstance(field, DateField):
                            print("--------------field: ", field)
                            filter_by = "{0}__{1}".format(i, "range")
                            filter_value = filter_value.split(" ")
                        elif isinstance(field, ManyToManyField):
                            model = queryset.model._meta.get_field(i).related_model
                            first_field = model._meta.fields[1].name
                            filter_by = "{0}__{1}".format(
                                f"{i}__{first_field}", "icontains"
                            )
                        else:
                            print("-----------------else")
                            filter_by = "{0}__{1}".format(i, "icontains")
                            if "," in filter_value:
                                filter_value = filter_value.split(",")
                                filter_by = "{0}__{1}".format(f"{i}", "in")

                    except Exception as e:
                        print("e: ", e)
                        if "date" in i:
                            filter_by = f"{i}"
                            filter_value = filter_value.split(" ")
                        elif i in list_filter_fields and filter_value:
                            filter_by = "{0}__{1}".format(f"{i}", "contains")
                            filter_value = filter_value.split(",")
                        else:
                            filter_by = f"{i}__icontains"
                    kwargs[filter_by] = filter_value
                    print("filter_by: ", filter_by)
                    print("kwargs: ", kwargs)
            queryset = queryset.filter(Q(**kwargs, _connector=Q.AND)).distinct()
        if pagination != "false":
            results = super().paginate_queryset(
                queryset=super().filter_queryset(queryset=queryset),
            )
            results = self.get_serializer(results, many=True).data
            response = super().get_paginated_response(data=results)
            response.data["total_data"] = total_count
            return response
        elif pagination == "false":
            results = super().filter_queryset(queryset=queryset)
            results = self.get_serializer(results, many=True).data
            response = results
            response = {
                "data": response,
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object(request)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            response = {
                "message": "Updated Succesfully",
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            }
            return Response(response, status=status.HTTP_200_OK)
        first_error_key = next(iter(serializer.errors))
        first_error_value = str(serializer.errors[first_error_key][0])
        # first_error_key = capitalize_key(first_error_key)

        error_message = f"{first_error_key}: {first_error_value}"
        response = {"message": error_message, "status": status.HTTP_400_BAD_REQUEST}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(request)
        self.perform_destroy(instance)
        response = {
            "message": "Deleted Succesfully",
            "data": "deleted",
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)


class CustomViewSetMasterWithoutPagination(ModelViewSet, SearchFilter):
    filter_backends = [SearchFilter]

    def get_object(self, request):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset(request))

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        response = {
            "message": "Created Succesfully",
            "data": serializer.data,
            "status": status.HTTP_201_CREATED,
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        response = {
            "data": self.get_serializer(self.get_object(request)).data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[search, filter, start_date, end_date],
        operation_description="Travel agent list api",
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)
        filter = request.GET.getlist("filter", [])

        search = request.GET.get("search", "")

        if filter:
            for i in filter:
                search = request.GET.get(i)
                try:
                    model = queryset.model
                    if i in ["agreement_start_date", "agreement_end_date"]:
                        filter_by = "{0}__{1}".format(f"bankcmrate__{i}", "range")
                        search = search.split(" ")
                    else:
                        field = model._meta.get_field(i)
                        print("field: ", field)
                        if isinstance(field, ForeignKey):
                            print("yes")
                            model = queryset.model._meta.get_field(i).related_model
                            first_field = model._meta.fields[1].name
                            filter_by = "{0}__{1}".format(
                                f"{i}__{first_field}", "icontains"
                            )
                        elif isinstance(field, DateTimeField):
                            print("field: ", field)
                            filter_by = "{0}__{1}".format(i, "range")
                            search = search.split(" ")
                            search[1] = datetime.strptime(
                                search[1], "%Y-%m-%d"
                            ) + timedelta(days=1)
                            print("search[1]: ", search[1])
                        elif isinstance(field, DateField):
                            print("--------------field: ", field)
                            filter_by = "{0}__{1}".format(i, "range")
                            search = search.split(" ")
                        elif isinstance(field, ManyToManyField):
                            model = queryset.model._meta.get_field(i).related_model
                            first_field = model._meta.fields[1].name
                            filter_by = "{0}__{1}".format(
                                f"{i}__{first_field}", "icontains"
                            )
                        else:
                            print("-----------------else")
                            filter_by = "{0}__{1}".format(i, "icontains")
                except Exception as e:
                    print("e: ", e)
                    if "date" in i:
                        filter_by = f"{i}"
                        search = search.split(" ")
                    else:
                        filter_by = f"{i}__icontains"
                kwargs[filter_by] = search
            queryset = queryset.filter(Q(**kwargs, _connector=Q.AND))

        results = queryset = super().filter_queryset(queryset=queryset)
        results = self.get_serializer(results, many=True).data
        response = results
        response = {
            "data": response,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object(request)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = {
            "message": "Updated Succesfully",
            "data": serializer.data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(request)
        self.perform_destroy(instance)
        response = {
            "message": "Deleted Succesfully",
            "data": "deleted",
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)


class CustomStatusTrue(CustomViewSetMaster):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        status = response.data["status"]
        print(response)
        response.data["status"] = (
            True if status in [True, 200] else False
        )  # Update the status to be True instead of HTTP 200 OK
        response.data["message"] = (
            "Success" if status in [True, 200] else "Something Went Wrong"
        )
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        status = response.data["status"]
        print(response)
        response.data["status"] = True if status in [True, 200] else False
        response.data["message"] = (
            "Success" if status in [True, 200] else "Something Went Wrong"
        )
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        status = response.data["status"]
        response.data["status"] = True if status in [True, 200] else False
        response.data["message"] = (
            "Success" if status in [True, 200] else "Something Went Wrong"
        )
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        status = response.data["status"]
        response.data["status"] = True if status in [True, 200] else False
        response.data["message"] = (
            "Success" if status in [True, 200] else "Something Went Wrong"
        )
        return response
