from django.urls import path, include


from apis.views import *

urlpatterns = [
    path('sectors/', SectViewSet.as_view(), name='sectors'),
    path('subsectors/', SubSectApiView.as_view(), name='subsectors'),
    path('indicators/',  IndicaApiView.as_view(), name='indicators'),
    path('unique-country/', UniqueCountryApiView.as_view(), name='unique_country'),
    path('min-max-years/', MinMaxYearsApiView.as_view(), name='min_max_years'),
    path('indicators/<int:pk>/', IndicaApiView.as_view(), name='indicators-detail'),
    path('country/', CountryApiView.as_view(), name='country'),
    path('years/', YearApiView.as_view(), name='years'),
    path('min-max-rank/', MinMaxRankApiView.as_view(), name='min_max_rank'),
    path('description/', DescriptionApiView.as_view(), name='description'),
    
    path('def/', SectSubsectIndicaView.as_view(), name='get-default-data'),
    path('ranks/', AvailableRanksView.as_view(), name='get-available-ranks'),
    
    #first dashboard
    path('bar-chart/', AmountView.as_view(), name='bar_chart'),
    path('rank-diff/', RankDifferenceApiView.as_view(), name='rank_difference'),
    path('rank-amount-chart/', RankAmountDiagrams.as_view(),name='diagram_3&4'),
    # path('line-chart/', LineChartApiView.as_view(), name='line_chart'),
    # path('bump-chart/', BumpChartApiView.as_view(), name='bump_chart'),
    # path('chat-bot/', ChatBotAPIView.as_view()),
    #second dashboard
    path('country-info/', CountryInfoApiView.as_view(), name='country_info'),
    path('country-diagram/', CountryIndicaDiagramApiView.as_view(), name='country_diagram'),
    path('country-rank-difference/', CountryIndicaRankDifferenceApiView.as_view(), name='country_rank_difference'),
    path('average-score/', AverageScoreIndicaApiView.as_view(), name='average_score'),
    path('year-score/', SectorYearScoreApiView.as_view(), name='year_score'),
    path("sector-rank-difference/", SectorRankDifferenceApiView.as_view(), name="country_score"),
    path("sector-average-score/", SectorAverageScoreApiView.as_view(), name="sector_average_score"),
    path("country-score-year/", CountryScoreYearByApiView.as_view(), name="country_score_year"),
    path("country-score-difference/", ScoreDifferenceTwoYearsApiView.as_view(), name="country_score_sector"),
    # path("country-test-score-difference/", ScoreTestDifferenceTwoYearsApiView.as_view(), name="country_score_sector"),
]