from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied

from questions.api.permissions import IsAuthorOrReadOnly, IsQuestionAuthorOrReadOnly
from questions.api.serializers import AnswerSerializer, QuestionSerializer, TagSerializer
from questions.models import Answer, Question, Tag


class AnswerCreateAPIView(generics.CreateAPIView):
    """Allow users to answer a question instance if they haven't already."""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=kwarg_slug)

        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question!")

        serializer.save(author=request_user, question=question)


class AnswerLikeAPIView(APIView):
    # """Allow users to add/remove a like to/from an answer instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """Remove request.user from the up_voters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.up_voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """Add request.user to the up_voters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.down_voters.remove(user)
        answer.up_voters.add(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerDisLikeAPIView(APIView):
    """Allow users to add/remove a like to/from an answer instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """Remove request.user from the down_voters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.down_voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """Add request.user to the up_voters queryset of an answer instance."""
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.up_voters.remove(user)
        answer.down_voters.add(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerListAPIView(generics.ListAPIView):
    """Provide the answers queryset of a specific question instance."""
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answer.objects.filter(question__slug=kwarg_slug).order_by("-created_at")


class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Provide *RUD functionality for an answer instance to it's author."""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    """Provide CRUD functionality for Question."""
    queryset = Question.objects.all().order_by("-created_at")
    lookup_field = "slug"
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["author__username", "tags__tag_name"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionLikeAPIView(APIView):
    """Allow users to add/remove a like to/from an question instance."""
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        """Remove request.user from the up_voters queryset of an answer instance."""
        question = get_object_or_404(Question, slug=slug)
        user = request.user

        question.up_voters.remove(user)
        question.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(
            question, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        """Add request.user to the up_voters queryset of an answer instance."""
        question = get_object_or_404(Question, slug=slug)
        user = request.user

        question.down_voters.remove(user)
        question.up_voters.add(user)
        question.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(
            question, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionDisLikeAPIView(APIView):
    """Allow users to add/remove a dislike to/from an question instance."""
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        """Remove request.user from the down_voters queryset of an answer instance."""
        question = get_object_or_404(Question, slug=slug)
        user = request.user

        question.down_voters.remove(user)
        question.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(
            question, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        """Add request.user to the down_voters queryset of an answer instance."""
        question = get_object_or_404(Question, slug=slug)
        user = request.user

        question.up_voters.remove(user)
        question.down_voters.add(user)
        question.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(
            question, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TagCreateAPIView(generics.CreateAPIView):
    """Allow authors to add tags a question instance if they haven't already added maximum number of tags."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=kwarg_slug)
        tag_count = Tag.objects.filter(
            question__slug=kwarg_slug).order_by("-created_at").count()

        if request_user == question.author:
            if tag_count <= 3:
                serializer.save(question=question)
            else:
                raise ValidationError(
                    "Maximum of 3 tags can be added to a question")
        else:
            raise PermissionDenied()


class TagListAPIView(generics.ListAPIView):
    """Provide the tags queryset of a specific question instance."""
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsQuestionAuthorOrReadOnly]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Tag.objects.filter(question__slug=kwarg_slug).order_by("-created_at")


class TagRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Provide *RUD functionality for an tag instance to it's author."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsQuestionAuthorOrReadOnly]
