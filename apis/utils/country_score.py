from django.db.models import QuerySet
def country_score(max_indecator_rank: QuerySet, country_rank:QuerySet):
    max_rank_dict = {}
    for max_rank in max_indecator_rank:
        max_rank_dict[max_rank['indicator__indicator']] = max_rank['max_rank']
    total_score = 0
    num_sectors = 0
    for con in country_rank:
        indicator = con['indicator__indicator']
        if indicator in max_rank_dict:
            score = round((1 - con['rank'] / max_rank_dict[indicator]) * 100, 2)
            total_score += score
            num_sectors += 1
    average_score = round(total_score / num_sectors, 2)
    return average_score