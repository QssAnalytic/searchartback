from django.forms import model_to_dict

from rest_framework.views import APIView
from core.models import Country
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi
from django.db.models import Q


# diagram1 -  countries and their amount by selected ranks and year
class AmountView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'indicator',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Gross Domestic Product billions of U.S. dollars",
                default="Gross Domestic Product billions of U.S. dollars"
                
            ),
            openapi.Parameter(
                'year1',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="2019",
                default="2019"
                
            ),
            openapi.Parameter(
                'ranks',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="1,10",
                default="1,10"
                
            ),
            openapi.Parameter(
                'countries',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Afghanistan;Albania;Algeria;Andorra;Angola;Antigua and Barbuda;Argentina",
                default="Afghanistan;Albania;Algeria;Andorra;Angola;Antigua%20and%20Barbuda;Argentina;Armenia;Aruba;Australia;Austria;Azerbaijan;Bahamas;Bahrain;Bangladesh;Barbados;Belarus;Belgium;Belize;Benin;Bermuda;Bhutan;Bolivia;Bosnia%20and%20Herzegovina;Botswana;Brazil;Brunei;Bulgaria;Burkina%20Faso;Burma%20(Myanmar);Burundi;Cabo%20Verde;Cambodia;Cameroon;Canada;Central%20African%20Republic;Chad;Chile;China;China,%20P.R.:%20Hong%20Kong;China,%20P.R.:%20Macao;Colombia;Comoros;Costa%20Rica;Croatia;Cyprus;Czechia;Denmark;Djibouti;Ecuador;Egypt;El%20Salvador;Equatorial%20Guinea;Eritrea;Estonia;Eswatini;Ethiopia;Faroe%20Islands;Fiji;Finland;France;Gabon;Gambia;Georgia;Germany;Ghana;Greece;Grenada;Guatemala;Guinea;Guinea-Bissau;Guyana;Haiti;Honduras;Hungary;Iceland;India;Indonesia;Iran;Iraq;Ireland;Israel;Italy;Ivory%20Coast;Jamaica;Japan;Jordan;Kazakhstan;Kenya;Kiribati;Kuwait;Kyrgyzstan;Laos;Latvia;Lebanon;Lesotho;Liberia;Libya;Liechtenstein;Lithuania;Luxembourg;Madagascar;Malawi;Malaysia;Maldives;Mali;Malta;Mexico;Micronesia;Moldova;Monaco;Mongolia;Montenegro;Morocco;Mozambique;Namibia;Nepal;Netherlands;New%20Caledonia;New%20Zealand;Nicaragua;Niger;Nigeria;North%20Macedonia;Norway;Oman;Pakistan;Palau;Palestine;Panama;Papua%20New%20Guinea;Paraguay;Peru;Philippines;Poland;Portugal;Puerto%20Rico;Qatar;Romania;Russia;Rwanda;Samoa;San%20Marino;Sao%20Tome%20and%20Principe;Saudi%20Arabia;Senegal;Serbia;Seychelles;Sierra%20Leone;Singapore;Slovakia;Slovenia;Solomon%20Islands;Somalia;South%20Africa;South%20Korea;Spain;Sri%20Lanka;St.%20Lucia;St.%20Vincent%20and%20the%20Grenadines;Sudan;Suriname;Sweden;Switzerland;Syria;Tajikistan;Tanzania;Thailand;Togo;Tonga;Trinidad%20and%20Tobago;Tunisia;Turkiye;Turkmenistan;Tuvalu;Uganda;Ukraine;United%20Arab%20Emirates;United%20Kingdom;United%20States;Uruguay;Uzbekistan;Vanuatu;Venezuela;Vietnam;Yemen;Zambia;Zimbabwe"
                
            ),
            

        ],responses={200: ""},)
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
