from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from .models import GameCore, Boost, WordsSet
from django.shortcuts import render, redirect
from rest_framework.response import Response
from .forms import UserForm
from rest_framework import viewsets
from .serializers import GameCoreSerializer, BoostSerializer, WordsSetSerializer


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

        return render(request, 'clicker/login.html', {'form': form, 'invalid': True})

    return render(request, 'clicker/login.html', {'form': form})


@login_required
def index(request):
    return render(request, 'clicker/index.html', {'username': request.user.username})


@login_required
def game(request):
    core = GameCore.objects.get(user=request.user)
    boosts = Boost.objects.filter(core=core)
    return render(request, 'clicker/game.html', {'core': core, 'boosts': boosts})


@api_view(['GET'])
@login_required
def call_click(request):
    core = GameCore.objects.get(user=request.user)
    is_levelup = core.click()
    if is_levelup:
        Boost.objects.create(core=core, price=core.points,
                             power=core.level * 2)
    core.save()
    return Response({'core': GameCoreSerializer(core).data, 'is_levelup': is_levelup})


@api_view(['POST'])
def update_points(request):
    points = request.data['current_points']
    core = GameCore.objects.get(user=request.user)

    is_levelup, boost_type = core.set_points(points)

    if is_levelup:
        Boost.objects.create(core=core, price=core.points,
                             power=core.level * 2, type=boost_type)
    core.save()

    return Response({
        'core': GameCoreSerializer(core).data,
        'is_levelup': is_levelup,
    })


@api_view(['GET'])
def get_core(request):
    core = GameCore.objects.get(user=request.user)
    return Response({'core': GameCoreSerializer(core).data})


@api_view(['PUT'])
def set_words_set(request):
    core = GameCore.objects.get(user=request.user)
    words = request.data['words']

    if len(words) != 0:
        if core.words_set.lang == "":
            WordsSet.objects.filter(id=core.words_set.id).delete()
        core.words_set = WordsSet.objects.create(words=words)
        core.save()
    return Response({"words_set": WordsSetSerializer(core.words_set).data})


@api_view(['PUT'])
def switch_lang(request):
    core = GameCore.objects.get(user=request.user)
    match core.words_set.lang:
        case '':
            WordsSet.objects.filter(id=core.words_set.id).delete()
            core.words_set = WordsSet.objects.get(lang='ru')
        case 'ru':
            core.words_set = WordsSet.objects.get(lang='en')
        case other:
            core.words_set = WordsSet.objects.get(lang='ru')
    core.save()
    return Response({"words_set": WordsSetSerializer(core.words_set).data})


@api_view(['PUT'])
def switch_theme(request):
    core = GameCore.objects.get(user=request.user)
    match core.night_theme:
        case True:
            core.night_theme = False
        case other:
            core.night_theme = True
    core.save()
    return Response({"theme": 'night' if core.night_theme else 'day'})


@api_view(['GET'])
def get_theme(request):
    core = GameCore.objects.get(user=request.user)
    return Response({"theme": ('night' if core.night_theme else 'day')})
