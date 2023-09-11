from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, When, Value, IntegerField, Case
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, DetailView

from forum.models import ThreadComment, ForumThread
from mediapop.models import Media, MediaVote
from reviews.models import Review, ReviewComment


# Create your views here.


class IndexView(TemplateView):
    template_name = "mediapop/index.html"


class MediaView(TemplateView):
    template_name = "mediapop/media-index.html"

    def get(self, request, *args, **kwargs):
        items_per_page = 10

        q_name = request.GET.get('name')
        q_media_type = request.GET.get('type')
        q_order_by = request.GET.get('order_by')
        q_recommended = (q_order_by == "recommended")

        media = None

        if not q_order_by or q_recommended:
            q_order_by = "name"

        if q_recommended and request.user.is_authenticated:
            # -- RECOMMENDATION SYSTEM --

            thread_comment_counts = ThreadComment.objects.filter(user=request.user).values(
                'thread__media__media_type').annotate(
                comment_count=Count('id'))
            review_comment_counts = ReviewComment.objects.filter(user=request.user).values(
                'review__media__media_type').annotate(
                comment_count=Count('id'))
            forum_thread_counts = ForumThread.objects.filter(author=request.user).values('media__media_type').annotate(
                thread_count=Count('id'))
            media_vote_avg = MediaVote.objects.filter(user=request.user).values('media__media_type').annotate(
                vote_avg=Avg('vote'))

            recommendation_scores = {}
            for media_type in Media.MEDIA_TYPES:
                thread_comment_weight = 0.1
                forum_thread_weight = 0.3
                review_comment_weight = 0.1
                media_vote_weight = 0.4

                thread_comment_value = 0
                forum_thread_value = 0
                review_comment_value = 0
                media_vote_value = 0

                filtered_thread_comment = thread_comment_counts.filter(thread__media__media_type=media_type[0])
                if len(filtered_thread_comment) > 0:
                    thread_comment_value = filtered_thread_comment[0]['comment_count']

                filtered_forum_thread = forum_thread_counts.filter(media__media_type=media_type[0])
                if len(filtered_forum_thread) > 0:
                    forum_thread_value = filtered_forum_thread[0]['thread_count']

                filtered_review_comment = review_comment_counts.filter(review__media__media_type=media_type[0])
                if len(filtered_review_comment) > 0:
                    review_comment_value = filtered_review_comment[0]['comment_count']

                filtered_media_vote = media_vote_avg.filter(media__media_type=media_type[0])
                if len(filtered_media_vote) > 0:
                    media_vote_value = filtered_media_vote[0]['vote_avg']

                recommendation_scores[media_type] = (thread_comment_value * thread_comment_weight +
                                                     forum_thread_value * forum_thread_weight +
                                                     review_comment_value * review_comment_weight +
                                                     media_vote_value * media_vote_weight)

            recommendation_scores = sorted(recommendation_scores.keys(),
                                           key=lambda x: recommendation_scores[x],
                                           reverse=True)

            media = Media.objects.filter(media_type=recommendation_scores[0][0]).annotate(
                users_vote=Avg('mediavote__vote'),
                reviewers_vote=Avg('review__vote'))
            media = media.order_by(q_order_by)
            for i in range(1, len(recommendation_scores)):
                tmp = Media.objects.filter(media_type=recommendation_scores[i][0]).annotate(
                    users_vote=Avg('mediavote__vote'),
                    reviewers_vote=Avg('review__vote'))
                tmp = tmp.order_by(q_order_by)

                media = list(media) + list(tmp)
        else:
            media = Media.objects.annotate(users_vote=Avg('mediavote__vote'),
                                           reviewers_vote=Avg('review__vote'))
            media = media.order_by(q_order_by)

        if q_name:
            media = media.filter(name__contains=q_name)

        if q_media_type:
            media = media.filter(media_type=q_media_type)

        paginator = Paginator(media, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            "media": page
        }

        return render(request=request, template_name=self.template_name, context=context)


class MediaDetailView(DetailView):
    model = Media
    template_name = 'mediapop/media.html'
    context_object_name = 'media'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["users_vote"] = MediaVote.objects.filter(media=context.get("object")).aggregate(Avg('vote'))['vote__avg']
        context["reviewers_vote"] = Review.objects.filter(media=context.get("object")).aggregate(Avg('vote'))['vote__avg']

        return context

    # TODO: Write POST to accept user votes


class UserLoginView(FormView):
    template_name = "mediapop/login-form.html"
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        auth.login(self.request, user)
        # You can customize the success message as needed
        return HttpResponse("")


class UserSignupView(FormView):
    template_name = "mediapop/signup-form.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='User')
        user.groups.add(group)

        auth.login(self.request, user)
        # Redirect to a success page or do something else
        return HttpResponse("")
