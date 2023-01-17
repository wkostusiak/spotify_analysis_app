import datetime
import plotly.express as px
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random
import numpy as np
import plotly.graph_objects as go

# top 10 artists, function returns wordcloud with their names#

def top10artists(current_sp):
    artists = current_sp.current_user_top_artists(limit=10, time_range='long_term')
    names = []
    list = artists['items']
    for item in list:
        names.append(item['name'])

    #wordcloud with top 10 long-term artists #

    colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(10)]
    weights = [random.randint(15, 35) for i in range(10)]

    data = go.Scatter(x=[random.random() for i in range(30)],
                      y=[random.random() for i in range(30)],
                      mode='text',
                      text=names,
                      marker={'opacity': 0.3},
                      textfont={'size': weights,
                                'color': colors},)
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}},)
    fig = go.Figure(data=[data], layout=layout)

    fig.update_layout(
        autosize=False,
        height=500,
        width=500,
    )
    names_cloud = plot(fig, output_type='div')

    return names_cloud


# genres represented by top 10 artists #
#returns horizontal bar chart with genres distribution"


def top10genres(current_sp):
    artists = current_sp.current_user_top_artists(limit=10, time_range='long_term')
    genres = []
    list = artists['items']
    for item in list:
        genres.append(item['genres'])

    genres_dict = {}
    for types in genres:
        for type in types:
            if type not in genres_dict.keys():
                genres_dict[type] = 1
            else:
                genres_dict[type] = genres_dict[type] + 1


    df = pd.DataFrame({"genres": genres_dict.keys(), "genres_distribution": genres_dict.values(), "genres names": genres_dict.keys() })
    fig = px.bar(
        data_frame=df,
        y="genres",
        x="genres_distribution",
        orientation="h",
        title='sth',
    )

    fig.update_layout(
        autosize=True,
    )

    genres_bar_div = plot(fig, output_type='div')

    return genres_bar_div


# top 50 tracks in long term and short term and their features (based on songs' ids) #
# returns comparative bar chart#

class TopSongs:
    pass
    def top_50_songs(self, current_sp, term):
        tracks = current_sp.current_user_top_tracks(limit=50, offset=0, time_range=term)

        return tracks

    def top_50_features_ids(self, tracks, current_sp):
        ids = []
        titleslist = tracks['items']
        for item in titleslist:
            ids.append(item['id'])

        return ids


    def top_50_features(self, current_sp, ids):

        danceability = []
        energy = []
        loudness = []
        speechiness = []
        acousticness = []
        instrumentalness = []
        liveness = []
        valence = []

        tracks_features = current_sp.audio_features(ids)
        for item in tracks_features:
            danceability.append(float(item['danceability']))
            energy.append(float(item['energy']))
            speechiness.append(float(item['speechiness']))
            acousticness.append(float(item['acousticness']))
            instrumentalness.append(float(item['instrumentalness']))
            liveness.append(float(item['liveness']))
            valence.append(float(item['valence']))

        list_of_features = [danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence]
        labels = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']

        return list_of_features, labels

    def average(self, list_of_features):

        avgs = []
        for list in list_of_features:
            value_sum = 0
            for value in list:
                value_sum = + value
            avg = value_sum / len(list_of_features)
            avgs.append(avg)

        return avgs


def topsongs_compared(current_sp):

    songs = TopSongs()

    # fetching data for both long and short term using TopSongs class #
    tracks_long_term = TopSongs.top_50_songs(songs, current_sp, 'long_term')
    tracks_short_term = TopSongs.top_50_songs(songs, current_sp, 'short_term')

    ids_long = TopSongs.top_50_features_ids(songs, tracks_long_term, current_sp)
    ids_short = TopSongs.top_50_features_ids(songs, tracks_short_term, current_sp)

    list_of_features_long, labels = TopSongs.top_50_features(songs, current_sp, ids_long)
    list_of_features_short, labels= TopSongs.top_50_features(songs, current_sp, ids_short)

    avgs_long = TopSongs.average(songs, list_of_features_long)
    avgs_short = TopSongs.average(songs, list_of_features_short)

    df = pd.DataFrame({"features": labels, "average_long": avgs_long, "average_short": avgs_short })
    fig = px.bar(
        data_frame=df,
        x="features",
        y=["average_long", "average_short"],
        barmode="group",
        orientation="v",
        title='sth',
        color_discrete_map={
            'avergae_long': '#1DB954',
            'average_short': '#191414',
        },
    )

    fig.update_layout(
        autosize=True,
    )

    bar_div = plot(fig, output_type='div')

    # top user's songs compared with top 50 world playlist#

    tracks_world = current_sp.playlist_tracks(playlist_id='37i9dQZEVXbNG2KDcFcKOF?si=18364ade5d4b4606')
    tracks_world_dict = tracks_world['tracks']
    listofdicts = tracks_world_dict['items']
    ids_world = []
    for dict in listofdicts:
        nested_dict = dict['track']
        ids_world.append(nested_dict['id'])

    list_of_features_world, labels = TopSongs.top_50_features(songs, current_sp, ids_world)

    world_compared_df = pd.DataFrame(zip(labels, list_of_features_world, list_of_features_short),
                                     columns=['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness',
                                              'liveness', 'valence'])

    fig_world = px.scatter(world_compared_df, y='labels',
                     x=['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness',
                                              'liveness', 'valence'],

                    )

    fig_world.update_layout(
        autosize=True,
    )

    scattered_plot = plot(fig_world, output_type='div')

    return bar_div, scattered_plot



# top 50 tracks in long term and decades they were released (based on songs' ids) #
# returns so-called donut chart with % of each decade #

def topdecades(current_sp, term):
    tracks = current_sp.current_user_top_tracks(limit=50, offset=0, time_range=term)
    titles = []
    ids = []
    titleslist = tracks['items']
    for item in titleslist:
        titles.append(item['name'])
        ids.append(item['id'])

    dates = []

    for item in titleslist:
        for dic in titleslist:
            dates.append(dic['album']['release_date'])

    decades = []
    for date in dates:
        try:
            datestrp = datetime.datetime.strptime(date, '%Y-%m-%d')
            year = datestrp.year
            decade = int(np.floor(year / 10) * 10)
            decades.append(decade)
        except ValueError:
            pass

    decades_dict = {}
    for decade in decades:
        if decade not in decades_dict.keys():
            decades_dict[decade] = 1
        else:
            decades_dict[decade] = decades_dict[decade] + 1

    decades_labels = [str(x) for x in decades_dict.keys()]

    df_decades = pd.DataFrame({"decades": decades_labels, "percentages": decades_dict.values()})
    fig_donut = px.pie(df_decades, values="percentages", names="decades", color_discrete_sequence=px.colors.sequential.Emrld)

    fig_donut.update_traces(hole=.4, hoverinfo="label+percent+name")
    donut_div = plot(fig_donut, output_type='div')

    return donut_div

#change names etc#

def compared(current_sp):
    songs = TopSongs()
    tracks_long_term = TopSongs.top_50_songs(songs, current_sp, 'long_term')
    ids_long = TopSongs.top_50_features_ids(songs, tracks_long_term, current_sp)
    list_of_features_long, labels = TopSongs.top_50_features(songs, current_sp, ids_long)
    res = {labels[i]: list_of_features_long[i] for i in range(len(labels))}
    df = pd.DataFrame.from_dict(res)

    fig = px.scatter_matrix(df,
                            dimensions=['danceability', 'energy',  'valence'],
                            labels=['danceability', 'energy', 'valence'],
                            title="Scatter matrix",

                            )

    fig.update_traces(diagonal_visible=False)
    fig.update_layout(
        height=600,
        width=600
    )

    matrix_div = plot(fig, output_type='div')

    #heatmap

    res = {labels[i]: list_of_features_long[i] for i in range(len(labels))}
    df_heat = pd.DataFrame.from_dict(res)


    matrix = df_heat.corr()  # returns a matrix with correlation of all features
    x_list = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=matrix,
        x=x_list,
        y=x_list,
        hoverongaps=True))
    fig_heatmap.update_layout(margin=dict(t=200, r=200, b=200, l=200),
                              width=800, height=650,
                              autosize=True)


    heat_div = plot(fig_heatmap, output_type='div')

    return matrix_div, heat_div



