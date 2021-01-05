from rest_framework import serializers
from questions.models import Answer, Question, Tag


class TagSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField()
    question_slug = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        exclude = ["question", "up_voters", "down_voters", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_likes_count(self, instance):
        return instance.up_voters.count()

    def get_dislikes_count(self, instance):
        return instance.down_voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.up_voters.filter(pk=request.user.pk).exists() or instance.down_voters.filter(pk=request.user.pk).exists()

    def get_question_slug(self, instance):
        return instance.question.slug


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    answers_count = serializers.SerializerMethodField()
    user_has_answered = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ["updated_at", "up_voters", "down_voters"]
        # fields = "__all__"

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        return instance.answers.filter(author=request.user).exists()

    def get_likes_count(self, instance):
        return instance.up_voters.count()

    def get_dislikes_count(self, instance):
        return instance.down_voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.up_voters.filter(pk=request.user.pk).exists() or instance.down_voters.filter(pk=request.user.pk).exists()
