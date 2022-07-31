from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .models import GameCore, Boost
from django.shortcuts import render, redirect
from rest_framework.response import Response
from .forms import UserForm
from rest_framework import viewsets
from .serializers import GameCoreSerializer, BoostSerializer
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
    finally:
        activate(cur_language)


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = GameCore.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts

    def partial_update(self, request, pk):
        points = request.data['points']
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup(points)
        if not is_levelup:
            return Response({'error': 'Не хватает денег'})

        old_boost_stats, new_boost_stats = is_levelup

        return Response({
            "old_boost_stats": self.serializer_class(old_boost_stats).data,
            "new_boost_stats": self.serializer_class(new_boost_stats).data,
        })


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'clicker/register.html', {'form': form})
    form = UserForm()
    return render(request, 'clicker/register.html', {'form': form})


def user_login(request):
    form = UserForm()
    if request.method == 'POST':
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')

        return render(request, 'clicker/login.html',
                      {'form': form, 'invalid': True})

    return render(request, 'clicker/login.html', {'form': form})


@login_required
def index(request):
    core = GameCore.objects.get(user=request.user)
    if core.lang_code != get_language():
        translate(core.lang_code)
        print("some magic with languages in index()")
    return render(request, 'clicker/index.html', {
        'welcome': _('Welcome, {}!').format(request.user.username)
    })


@login_required
def game(request):
    core = GameCore.objects.get(user=request.user)
    boosts = Boost.objects.filter(core=core)
    if core.lang_code != get_language():
        translate(core.lang_code)
        print("some magic with languages in game()")
    return render(request, 'clicker/game.html', {
        'core': core,
        'boosts': boosts,
        'hello': _('Hi, {}!').format(request.user.username)
    })


@api_view(['POST'])
def update_points(request):
    points = request.data['current_points']
    core = GameCore.objects.get(user=request.user)

    is_levelup, boost_type = core.set_points(points)

    if is_levelup:
        Boost.objects.create(core=core, price=core.points, power=core.level * 2, type=boost_type)
    core.save()

    return Response({
        'core': GameCoreSerializer(core).data,
        'is_levelup': is_levelup,
    })


@api_view(['GET'])
def get_core(request):
    core = GameCore.objects.get(user=request.user)
    # print("saved words: "+core.words_set.content)
    return Response({'core': GameCoreSerializer(core).data})


@api_view(['PUT'])
def switch_theme(request):
    core = GameCore.objects.get(user=request.user)
    if core.night_theme:
        core.night_theme = False
    else:
        core.night_theme = True
    core.save()
    return Response({"theme": 'night' if core.night_theme else 'day'})


@api_view(['GET'])
def get_theme(request):
    core = GameCore.objects.get(user=request.user)
    return Response({"theme": ('night' if core.night_theme else 'day')})


@api_view(['GET'])
def languages(request):
    core = GameCore.objects.get(user=request.user)
    result = {'current': core.lang}
    return Response(result)


@api_view(['GET'])
def book_languages(request):
    core = GameCore.objects.get(user=request.user)
    result = {'current': core.book}
    return Response(result)


@api_view(['POST'])
def set_language(request):
    lang_code = request.data['lang_code']
    core = GameCore.objects.get(user=request.user)
    core.set_language(lang_code)
    core.save()
    print("language set to: {}".format(core.lang_code))
    return Response({'lang_code': core.lang_code})


@api_view(['POST'])
def set_words_set(request):
    lang_code = request.data['lang_code']
    words_set = request.data['words_set']
    core = GameCore.objects.get(user=request.user)
    core.set_words_set(lang_code=lang_code, content=words_set)
    return Response({"words_set": core.words_set.content})


@api_view(['GET'])
def get_lang_code(request):
    print(GameCore.objects.get(user=request.user).lang_code)
    return Response({"lang_code": GameCore.objects.get(user=request.user).lang_code})
