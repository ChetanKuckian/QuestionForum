from django.urls import path, include
from rest_framework.routers import DefaultRouter

from questions.api import views as qv

router = DefaultRouter()
router.register(r"questions", qv.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("questions/<slug:slug>/answers/",
         qv.AnswerListAPIView.as_view(), name="answer-list"),

    path("questions/<slug:slug>/answer/",
         qv.AnswerCreateAPIView.as_view(), name="answer-create"),

    path("answers/<int:pk>/",
         qv.AnswerRUDAPIView.as_view(), name="answer-detail"),

    path("answers/<int:pk>/like/",
         qv.AnswerLikeAPIView.as_view(), name="answer-like"),

    path("answers/<int:pk>/dislike/",
         qv.AnswerDisLikeAPIView.as_view(), name="answer-dislike"),

    path("questions/<slug:slug>/like/",
         qv.QuestionLikeAPIView.as_view(), name="question-like"),

    path("questions/<slug:slug>/dislike/",
         qv.QuestionDisLikeAPIView.as_view(), name="question-dislike"),

    path("questions/<slug:slug>/tag/",
         qv.TagCreateAPIView.as_view(), name="tag-create"),
    path("questions/<slug:slug>/tags/",
         qv.TagListAPIView.as_view(), name="tag-list"),

    path("tags/<int:pk>/",
         qv.TagRUDAPIView.as_view(), name="tag-detail"),


]
