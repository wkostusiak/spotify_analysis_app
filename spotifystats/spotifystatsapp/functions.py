import datetime
import plotly.express as px
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random
import numpy as np
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression

# top 10 artists, function returns wordcloud with their names #

def top10artists(current_sp):
    artists = current_sp.current_user_top_artists(limit=10, time_range='long_term')
    names = []
    list = artists['items']
    for item in list:
        names.append(item['name'])

    colors = [plotly.colors.sequential.algae[random.randrange(1, 10)] for i in range(10)]
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
        autosize=True,
    )
    names_cloud = plot(fig, output_type='div')

    return names_cloud


# genres represented by top 10 artists #
# returns horizontal bar chart with genres distribution #


def top10genres(current_sp):
    artists = current_sp.current_user_top_artists(limit=10, time_range='long_term')
    genres = []
    list = artists['items']
    for item in list:
        if item['genres'] == []:  #  if artist is not yet classified, the array is empty #
            pass
        else:
            genres.append(item['genres'])

    genres_dict = {}
    for types in genres:
        for type in types:
            if type not in genres_dict.keys():
                genres_dict[type] = 1
            else:
                genres_dict[type] = genres_dict[type] + 1


    df = pd.DataFrame({"genres": genres_dict.keys(), "genres distribution": genres_dict.values(), "genres names": genres_dict.keys() })
    fig = px.bar(
        data_frame=df,
        y="genres",
        x="genres distribution",
        orientation="h",
    )

    fig.update_layout(
        autosize=True,
        title={
            'text' : 'Genres distribution for your top 10 artists',
            'y': 0.95,
            'x': 0.5,
            'xanchor' : 'center',
            'yanchor' : 'top'
        },
        font_color = 'black',
    )
    fig.update_traces(marker_color='#1DB954',)

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

    df = pd.DataFrame({"features": labels, "long term": avgs_long,
                       "short term": avgs_short})
    fig = px.bar(
        data_frame=df,
        x="features",
        y=["long term", "short term"],
        barmode="group",
        orientation="v",
        color_discrete_map={
            'long term': '#1DB954',
            'short term': '#191414',
        },
        labels={
            "value": "average",
            "features": "features",
            "variable" : "term"
        },
    )

    fig.update_layout(
        autosize=True,
        title={
            'text': 'Averages for different features in long and short term',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font_color='black',
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
    avgs_world = TopSongs.average(songs, list_of_features_world)

    trace_short = plotly.graph_objs.Scatter(
        x=labels,
        y=avgs_short,
        mode='markers',
        name='trace short'
    )

    trace_world = plotly.graph_objs.Scatter(
        x=labels,
        y=avgs_world,
        mode='markers',
        name='trace world'
    )

    data = [trace_short, trace_world]
    fig_world = plot(data, output_type='div')


    return bar_div, fig_world



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

def scatter_matrix(current_sp):
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

    fig.update_traces(diagonal_visible=False,)
    fig.update_layout(
        height=600,
        width=600,
    )

    matrix_div = plot(fig, output_type='div')

    # IN PROGRESS #
    #list_of_features = [danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence]
    figs = make_subplots(specs=[[{"secondary_y": True}]])
    figs.add_trace(go.Scatter(x=list_of_features_long[0], y=list_of_features_long[6], mode='markers'))
    model = LinearRegression().fit(list_of_features_long[0],list_of_features_long[6])
    y_pred = model.predict(list_of_features_long[0])
    figs.add_trace(go.Scatter(x=list_of_features_long[0], y=y_pred, mode='lines'))

    figs.update_layout(
        autosize=True,
    )

    figs_div = plot(figs, output_type='div')

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

    return matrix_div, heat_div, figs_div



