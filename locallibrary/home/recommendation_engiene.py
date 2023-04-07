import time

from django.apps import apps
from .click_house_link import ClickHouseService

Coeffciants = {
    "likes": 5,
    "step_in": 2,
    "active": 1,
    "friends": 2
}

PostDB = apps.get_model('home', 'Post')
UserDB = apps.get_model('accounts', 'User')
FollowDB = apps.get_model('home', 'HumanConnections')
CategoryDB = apps.get_model('home', 'Categories')
CommentsDB = apps.get_model('home', 'Comments')

UserAnalytics = ClickHouseService.instance()  # clickhouse


class StudyObject:
    def __init__(self, likes, step_in, categorie):
        self.categorie = categorie
        self.likes = likes
        self.step_in = step_in

    def calculate_crabby_patty(self, friends):
        if friends == 0:
            friends = 1
        if self.likes == 0:
            self.likes = 1

        if self.step_in == 0:
            self.step_in = 1

        like_weight = Coeffciants["likes"] * self.likes
        step_in_weight = Coeffciants["step_in"] * self.step_in
        friends_weight = Coeffciants["friends"] * friends

        return like_weight * step_in_weight * friends_weight


class CycleThread:
    @staticmethod
    def get_friends_data_map(user):
        friends = FollowDB.objects.filter(follower=user)

        # categories dict
        categories = {}

        for friend in friends:
            friend_cats = friend.follower.categories.split("#")

            for cat in friend_cats:
                try:
                    categories[cat] += 1
                except:
                    categories[cat] = 1
        ranking = []
        for i in range(len(categories)):
            min_key = min(categories, key=categories.get)
            ranking.append(min_key)
            del categories[min_key]

        return ranking

    @staticmethod
    def get_user_data_map(analysis_data):
        # get data with user
        study_user = []

        for row in analysis_data:
            category = row[0]

            sub_cats = category.split("#")

            for cat in sub_cats:
                study_user.append(StudyObject(row[1], row[2], cat))

        return study_user

    def calculate_categories(self, user_analysis, user):
        # use friends objects and user object to call analysis functions
        calculated_data = {}
        friends_top_cats = self.get_friends_data_map(user)

        for study_object in user_analysis:
            try:
                friends = friends_top_cats.index(study_object.categorie) + 1
            except:
                friends = 0
            calculated_data[study_object.categorie] = study_object.calculate_crabby_patty(friends)

        top_cats = []
        for i in range(3):
            key = max(calculated_data, key=calculated_data.get)
            top_cats.append(key)
            del calculated_data[key]

        return top_cats

    def start(self):
        # get all users
        DAY = 60 * 60 * 24
        while True:
            time.sleep(DAY)
            user_data = UserDB.objects.all()
            user_analytics = UserAnalytics

            for user in user_data:
                user_data_query = user_analytics.select('user_activity',
                                                        where=f"(user_id='{user.id}')",
                                                        select_list=['category',
                                                                     'sum(likes) AS likes, sum(step_in) AS step'],
                                                        group_by_list=['category']
                                                        )
                user_data = user_analytics.execute(user_data_query)
                if user_data:
                    user_analysis_data = self.get_user_data_map(user_data)
                    cat1, cat2, cat3 = self.calculate_categories(user_analysis_data, user)
                    user.categories = f"{cat1}#{cat2}#{cat3}"
                    user.save()


def main():
    cycle = CycleThread()
    cycle.start()
