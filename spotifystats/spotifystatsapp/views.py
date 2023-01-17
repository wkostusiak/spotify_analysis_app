from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from decouple import config
import pandas as pd
import requests
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from django .utils import timezone
from datetime import timedelta
from django.shortcuts import redirect

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipy.util as util

from .functions import top10artists, top10genres, topdecades, topsongs_compared, compared

class WelcomePage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'spotifystatsapp/welcome.html')

class Congrats(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'spotifystatsapp/congrats.html')

class AuthURL(View):
    def get(self, request, *args, **kwargs):
        sp_auth=spotipy.oauth2.SpotifyOAuth(
        client_id = config('CLIENT_ID'),
        client_secret = config('CLIENT_SECRET'),
        redirect_uri='http://127.0.0.1:8000/congrats',
        scope='playlist-read-private user-top-read user-library-read',
        open_browser=True,
        )
        sp_auth.get_access_token(request.GET.get("code"))
        sp = spotipy.client.Spotify(auth_manager=sp_auth)

        # fething data using functions decribed in functions.py #

        names_cloud = top10artists(sp)
        genres_bar_div = top10genres(sp)
        donut_div_long = topdecades(sp, 'long_term')
        donut_div_short = topdecades(sp, 'short_term')
        bar_div,scattered_plot = topsongs_compared(sp)
        matrix_div, heat_div = compared(sp)



        context = {
            'genres_bar_div' : genres_bar_div,
            'names_cloud' : names_cloud,
            'bar_div' : bar_div,
            'donut_div_long' : donut_div_long,
            'donut_div_short': donut_div_short,
            'matrix_div' : matrix_div,
            'heat_div' : heat_div,
            'scattered_plot' : scattered_plot,

        }

        return render(request, 'spotifystatsapp/congrats.html', context)


