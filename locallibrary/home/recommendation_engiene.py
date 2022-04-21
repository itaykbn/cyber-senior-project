from django.apps import apps
from .click_house_link import ClickHouseService

Categories = []

Coeffciants = {
    "likes": 5,
    "step_in": 2,
    "active": 1,
    "friends": 2
}

PostDB = apps.get_model('home', 'Post')
UserDB = apps.get_model('accounts', 'User')
UserAnalytics = ClickHouseService.instance()  # clickhouse


class StudyObject:
    def __init__(self, likes, active, step_in, categorie):
        self.categorie = categorie
        self.likes = likes
        self.step_in = step_in

    def calculate_crabby_patty(self, friends):
        like_weight = Coeffciants["likes"] * self.likes
        step_in_weight = Coeffciants["step_in"] * self.step_in
        friends_weight = Coeffciants["friends"] * friends

        return like_weight * step_in_weight * friends_weight


class CycleThread:

    def __init__(self):
        self.friends_objects = []

    def get_friends_data_map(self):

        # categories dict
        categories_counter = {}
        categories_ranking = {}

        # init bonus
        for user_categorie in Categories:
            categories_counter[user_categorie] = 0

        # sort categories
        for friend_obj in self.friends_objects:
            # filter categories for this friend
            friend_top = []  # friend object - get top 3

            for friend_categorie in friend_top:
                categories_counter[friend_categorie] += 1

        cat_number = len(Categories)  # initial rank
        # replace numbers
        while len(categories_counter) != 0:
            value = max(categories_counter, key=categories_counter.get)
            categories_ranking[value] = cat_number
            cat_number -= 1  # derank
            del categories_counter[value]

        return categories_ranking

    @staticmethod
    def get_user_data_map(analysis_data):
        # get data with user
        study_user = []

        for i in range(len(Categories)):
            categorie_analyitics = analysis_data  # filter only the relevant categorie

            study_object = StudyObject(categorie_analyitics.likes, categorie_analyitics.active_time,
                                       categorie_analyitics.step_in,
                                       Categories[i])

            study_user.append(study_object)  # add study_object to dict

        return study_user

    def calculate_categories(self, user_analysis, user_data):
        # use friends objects and user object to call analysis functions
        new_data = {}
        friends_data = self.get_friends_data_map()
        top_cats = []

        for study_object in user_analysis:
            friends = friends_data[study_object.categorie]
            new_data[study_object.categorie] = study_object.calculate_crabby_patty(friends)

        for i in range(3):
            value = max(new_data, key=new_data.get)
            top_cats.append(new_data[value])
            del new_data[value]

        return top_cats

    def start(self):
        # get all users
        user_data = UserDB.object.all()
        user_analytics = UserAnalytics

        for i in range(user_data.count()):
            self.friends_objects = None  # get friends from DB

            user_analysis = self.get_user_data_map(user_analytics[i])

            cat1, cat2, cat3 = self.calculate_categories(user_analysis, user_data[i])

            # insert new categories into DB
