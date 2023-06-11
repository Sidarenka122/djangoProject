from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime
from django.http import JsonResponse
import json

from .models import Announcement, House, Photo, Message

app_url = "/announcements/"


# главная страница со списком available_announcements
def index(request):
    message = None
    if "message" in request.GET:
        message = request.GET["message"]
        # создание HTML-страницы по шаблону index.html
        # с заданными параметрами available_announcements и message
    return render(request, "index.html",
                  {"available_announcements": Announcement.objects.order_by('-pub_date')[:5], "message": message})


def detail(request, announcement_id):
    error_message = None

    if "error_message" in request.GET:
        error_message = request.GET["error_message"]
    return render(request, "detail.html",
                  {"announcement": get_object_or_404(Announcement, pk=announcement_id), "error_message": error_message})


def bet(request, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    bet = request.POST.get('bet', 0)

    try:
        if announcement.max_bet >= int(bet):
            return redirect(
                '/announcements/' + str(announcement_id) +
                '?error_message=Bet is too small!',
            )
        elif announcement.auction_completed:
            return redirect(
                '/announcements/' + str(announcement_id) +
                '?error_message=Auction is completed!',
            )
        else:
            announcement.max_bet = bet
            announcement.number_of_bets += 1
            if int(bet) >= announcement.bet_to_complete:
                announcement.auction_completed = True
                announcement.sold_to = request.user.username
            announcement.save()
            return redirect(
                "/announcements/?message=Nice! Choose another one!")
    except (KeyError, Announcement.DoesNotExist):
        return redirect(
            '/riddles/' + str(announcement_id) +
            '?error_message=Failed to apply the bet!',
        )


def post(request, announcement_id):
    msg = Message()
    msg.author = request.user
    msg.chat = get_object_or_404(Announcement, pk=announcement_id)
    msg.message = request.POST['message']
    msg.pub_date = datetime.now()
    msg.save()
    return HttpResponseRedirect(app_url + str(announcement_id))


def msg_list(request, announcement_id):
    res = list(
        Message.objects.filter(chat_id=announcement_id).order_by('-pub_date')[:5].values('author__username', 'pub_date',
                                                                                         'message'))
    for r in res:
        r['pub_date'] = r['pub_date'].strftime('%d.%m.%Y %H:%M:%S')

    return JsonResponse(json.dumps(res), safe=False)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = app_url + "login/"
    template_name = "reg/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "reg/login.html"
    success_url = app_url

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(app_url)


class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    template_name = 'reg/password_change_form.html'
    success_url = app_url + 'login/'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)
