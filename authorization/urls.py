from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name="index"),
    path("twitter_login/", views.twitter_login, name="twitter_login"),
    path("twitter_callback/", views.twitter_callback, name="twitter_callback"),
    path("twitter_logout/", views.twitter_logout, name="twitter_logout"),
    path(
        "users-searched/",
        views.SearchedTwitterUsersListView.as_view(),
        name="user_search_history",
    ),
    path(
        "result-list/tu/<int:tuid>/",
        views.SearchedTweetsDetailView.as_view(),
        name="tu_result_list",
    ),
    path("score-tweets/", csrf_exempt(views.score_tweets_api), name="score_tweets"),
    path("thankyou/", csrf_exempt(views.ThankYouView.as_view()), name="thankyou"),
]
