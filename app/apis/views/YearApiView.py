from rest_framework.views import APIView
from core.models import Country
from rest_framework.response import Response


class YearApiView(APIView):
    def get(self, request):
        countries = str(request.GET.get("countries")).split(";")
        indicator = request.GET.get("indicator")

        queryset = (
            Country.objects.select_related('indicator').filter(country__in=countries, indicator__indicator=indicator)
            .values("year")
            .distinct()
        )

        years = []
        for year_dict in queryset:
            years.append(year_dict['year'])
        years = sorted(years)

        return Response(years)