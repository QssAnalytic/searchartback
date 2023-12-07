from django.forms import model_to_dict

from rest_framework.views import APIView
from core.models import Country
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q


# diagram1 -  countries and their amount by selected ranks and year
class AmountView(APIView):
    def get(self, request):
        indicator_name = request.GET.get("indicator")
        countries = str(request.GET.get("countries")).split(";")
        year1 = int(request.GET.get("year1"))
        ranks = list(map(int, str(request.GET.get("ranks")).split(",")))

        queryset = Country.objects.select_related("indicator").filter(
            indicator__indicator=indicator_name, year=year1
        )
        result = {}

        amounts = []
        for data in queryset:
            amounts.append(float(data.amount))

        result["min_amount"] = min(amounts)
        result["max_amount"] = max(amounts)

        result["countries_by_rank"] = []
        for data in queryset.filter(
            country__in=countries,
            rank__range=ranks
        ):
            result["countries_by_rank"].append(
                {
                    "country": data.country,
                    "country_code": data.country_code,
                    "country_code_2": data.country_code2,
                    "rank": data.rank,
                    "amount": data.amount,
                    "year": data.year,
                }
            )

        result["countries_by_rank"] = sorted(
            result["countries_by_rank"], key=lambda x: x["rank"], reverse=False
        )  # sort values by amount

        return Response(result, status=status.HTTP_200_OK)
