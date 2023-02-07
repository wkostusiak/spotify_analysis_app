![](https://github.com/wkostusiak/spotify_analysis_app/blob/master/spotify_header.png)

<h2 align="center">Analyze your spotify data with plotly & spotify API</h2>

  <p align="center">
    Analyze your Spotify data in Django app using authorization code flow :musical_note: App renders different graphs using plotly.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>

      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>

    </li>
    <li>
      <li><a href="#features">Features</a></li>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This app allows each user to see and analyze their spotify data shown as graphs. Different features such as top artists, genres and decades are compared.
Data is fetched thanks to spotify API, Spotipy and OAuth Authorization Code Flow. Authorization token is stored in cache. 
The main goal of this project was to explore Plotly and to successfully apply Authorization Code Flow.

Short time results are based on streaming in the last month.


### Built With

* Python 3.10 
* Spotify API
* Plotly for python 5.13.0
* Django 4.10
* Spotipy 2.22.1
* OAuth 2.0
* HTML5
* CSS3

![main page](https://github.com/wkostusiak/spotify_analysis_app/blob/master/spotifystats/images/main_page.png)

### Features

* User can log in using authorization prompt. Successful authorization results in info: 'Congrats! You are authenticated!' 
* App shows user's top 10 artists & genres. Each artist is associated with one or more different genres. The bar chart in the app shows genres represented by these artists in a long term.
* Top 50 songs' features - data fetched using spotify API consists of artists, songs and their features. Each one is described in a range from 0 to 1. Bar chart allows user to compare average score for each feature in their top 50 songs in short time and long time. 
* Correlation heatmap visualizing the strength of relationships between average scores for each feature in top 50 songs.
* Average score for each feature in user's top 50 songs vs the score for world's current top 50 songs.
* Pie charts which decades occur in ones top 50 songs and what percentage they are.


![example bar chart](https://github.com/wkostusiak/spotify_analysis_app/blob/master/spotifystats/images/top_50.png)
<br>
![example pie charts](https://github.com/wkostusiak/spotify_analysis_app/blob/master/spotifystats/images/decades.png)

### To be done...
* deployment of the app - any free hosting with more memory than pythonanywhere




<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please let me know 😄



