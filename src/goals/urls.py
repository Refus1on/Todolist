from django.urls import path

from goals import views

urlpatterns = [
    path('goal_category/create', views.CategoryCreateView.as_view(), name="category-create"),
    path('goal_category/list', views.CategoryListView.as_view(), name="category-list"),
    path('goal_category/<pk>', views.CategoryView.as_view(), name="category-retrieve-update-destroy"),

    path('goal/create', views.GoalCreateView.as_view(), name="goal-create"),
    path('goal/list', views.GoalListView.as_view(), name="goal-list"),
    path('goal/<pk>', views.GoalView.as_view(), name="goal-retrieve-update-destroy"),

    path('goal_comment/create', views.GoalCommentCreateView.as_view(), name="comment-create"),
    path('goal_comment/list', views.GoalCommentListView.as_view(), name="comment-list"),
    path('goal_comment/<pk>', views.GoalCommentView.as_view(), name="comment-retrieve-update-destroy"),
]
