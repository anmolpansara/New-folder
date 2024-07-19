# from rest_framework.settings import api_settings
from rest_framework import filters


class SearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, view, model, status=None):
        queryset = model.objects.all()
        if not isinstance(status, None):
            if isinstance(status, bool):
                return (
                    super()
                    .filter_queryset(request, queryset, view)
                    .filter(is_active=status)
                )
            return (
                super()
                .filter_queryset(request, queryset, view)
                .filter(is_user_kyc_verified=status)
            )
        else:
            return super().filter_queryset(request, queryset, view)


# class DateRangeFilter(django_filters.FilterSet):
#     start_date1 = django_filters.DateFilter(field_name="last_updated_date", lookup_expr="gte")
#     end_date1 = django_filters.DateFilter(field_name="last_updated_date", lookup_expr="lte")

#     class Meta:
#         abstract = True
#         models = (Region, State, SubState, Area)
#         fields = ["created_at", "last_updated_date"]
