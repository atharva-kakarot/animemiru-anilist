from django.shortcuts import render
import requests
from datetime import datetime
import math

def home(request):
    def get_season():
        month = datetime.now().month
        if 3 <= month <= 5:
            return "SPRING"
        elif 6 <= month <= 8:
            return "SUMMER"
        elif 9 <= month <= 11:
            return "FALL"
        else:
            return "WINTER"

    current_year = datetime.now().year
    
    url = 'https://graphql.anilist.co'
    
    airing_now_query= '''
    query ($page: Int, $perPage: Int, $season: MediaSeason) {
        Page (page: $page, perPage: $perPage) {
          pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
          }
          media(season: $season, type: ANIME, status: RELEASING, sort: POPULARITY_DESC, isAdult: false) {
            id
            title {
              romaji
              english
              native
            }
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            coverImage {
              large
              extraLarge
            }
            bannerImage
            episodes
            trailer {
              id
              thumbnail
            }
            format
            duration
            stats {
                scoreDistribution {
                    amount
                }
            }
            popularity
            genres
            favourites
            source
            studios {
                nodes {
                    id
                    name
                }
            }
            status
            description
            relations {
            edges {
                id
                relationType
                    node {
                        title {
                            romaji
                            english
                            native
                        }
                    }         
                }
            }
            season
            averageScore
            nextAiringEpisode {
              airingAt
              timeUntilAiring
              episode
            }
          }
        }
      }'''
      
    airing_now_variables = {
            'page': 1,
            'perPage': 50,
            'season': get_season(),
            'seasonYear': current_year
        }

    airing_now_response = requests.post(url, json={'query': airing_now_query, 'variables': airing_now_variables})
    
    if airing_now_response.status_code == 200:
        airing_now_data = airing_now_response.json()
    else:
        print(f"Error: {airing_now_response.status_code}")
        
    popular_anime_query = '''
    query {
            Page {
                media(sort: POPULARITY_DESC, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description
                    relations {
                        edges {
                            id
                            relationType
                                node {
                                    title {
                                        romaji
                                        english
                                        native
                                    }
                                }         
                            }
                        }
                    status
                    season
                    studios {
                        nodes {
                            id
                            name
                        }
                    }
                    source
                    favourites
                    trailer {
                        id
                        thumbnail
                    }
                    startDate {
                        year
                        month
                        day
                    }
                    endDate {
                        year
                        month
                        day
                    }
                    episodes
                    duration
                    stats {
                        scoreDistribution {
                            amount
                        }
                    }
                    bannerImage
                    genres
                    format
                    averageScore
                    coverImage {
                        large
                        extraLarge
                    }
                    popularity
                }
            }
        }'''
    
    popular_anime_response = requests.post(url, json={'query': popular_anime_query})
    
    if popular_anime_response.status_code == 200:
        popular_anime_data = popular_anime_response.json()
    else:
        print(f"Error: {popular_anime_response.status_code}, sdjfhsdfhk")
        
    top_anime_query ='''
    query {
            Page {
                media(sort: SCORE_DESC, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    coverImage {
                        large
                        extraLarge
                    }
                    startDate {
                        year
                        month
                        day
                    }
                    endDate {
                        year
                        month
                        day
                    }
                    status
                    season
                    studios {
                        nodes {
                            id
                            name
                        }
                    }
                    source
                    favourites
                    trailer {
                        id
                        thumbnail
                    }
                    popularity
                    relations {
                        edges {
                            id
                            relationType
                                node {
                                    title {
                                        romaji
                                        english
                                        native
                                    }
                                }         
                            }
                        }
                    episodes
                    duration
                    genres
                    stats {
                        scoreDistribution {
                            amount
                        }
                    }
                    format
                    description
                    averageScore
                    bannerImage
                }
            }
        }'''
        
    top_anime_variables = {
        'page': 1,
        'perPage': 50
    }
    
    top_anime_response = requests.post(url, json={'query': top_anime_query, 'variables': top_anime_variables})
    
    if top_anime_response.status_code == 200:
        top_anime_data = top_anime_response.json()
    else:
        print(f"Error: {top_anime_response.status_code}")
        
    context = {
        'airing_now_data': airing_now_data,
        'popular_anime_data': popular_anime_data,
        'top_anime_data': top_anime_data,
        }
    return render(request, 'index.html', context)
    

def anime_view(request, anime_id):
    anime_query = '''
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            description
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            season
            episodes
            trailer {
                id
                thumbnail
            }
            relations {
            edges {
                id
                relationType
                node {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                }         
            }
        }
        duration
        format
        status
        studios {
            nodes {
                id
                name
            }
        }
        genres
        source
        stats {
            scoreDistribution {
                amount
            }
        }
        averageScore
        episodes
        popularity
        favourites
        coverImage {
            large
            extraLarge
        }
        bannerImage
    }
    }'''
    
    anime_variables = {
        'id': anime_id 
    }

    anime_url = 'https://graphql.anilist.co'
    response = requests.post(anime_url, json={'query': anime_query, 'variables': anime_variables})
    
    if response.status_code == 200:
        anime_data = response.json()
    else:
        print(f"Error: {response.status_code}")
    

    formats = {
        "TV_SHORT": "TV Short",
        "MOVIE": "Movie",
        "SPECIAL": "Special",
        "MUSIC": "Music",
        "MANGA": "Manga",
        "NOVEL": "Novel",
        "ONE_SHOT": "One-shot",
        "TV": "TV"
    } 
    format = formats.get(anime_data['data']['Media']['format'], "N/A")

    seasons = {
        "WINTER": "Winter",
        "SPRING": "Spring",
        "SUMMER": "Summer",
        "FALL": "Fall",
    }
    season = seasons.get(anime_data['data']['Media']["season"], "N/A")

    
    if anime_data['data']['Media']['duration'] == None:
        episode_duration = "N/A"
    else:
        episode_duration = anime_data['data']['Media']['duration']
        
    statuses = {
        "FINISHED": "Finished",
        "RELEASING": "Releasing",
        "NOT_YET_RELEASED": "Not Yet Released",
        "CANCELLED": "Cancelled",
        "HIATUS": "Hiatus"
    }
    status = statuses.get(anime_data['data']['Media']["status"], "N/A")
    
    if anime_data['data']['Media']['episodes'] == None:
        episodes = "N/A"
    else:
        episodes = anime_data['data']['Media']['episodes']
        
    if anime_data['data']['Media']['stats']['scoreDistribution'] == None:
        score = "N/A"
    else:
        scores = anime_data['data']['Media']['stats']['scoreDistribution']
        score = 0
        for amount in scores:
            score += amount['amount']
    
    start_year = anime_data['data']['Media']['startDate']['year']
    start_month = anime_data['data']['Media']['startDate']['month']
    start_day = anime_data['data']['Media']['startDate']['day']
    
    if f"{start_day}/{start_month}/{start_year}" == f"{None}/{None}/{None}":
        start_date = "N/A"
    elif f"{start_day}/{start_month}/{start_year}" == f"{None}/{None}/{start_year}":
        start_date = f"?/?/{start_year}"
    else:
        start_date = f"{start_day}/{start_month}/{start_year}"
    
    end_year = anime_data['data']['Media']['endDate']['year']
    end_month = anime_data['data']['Media']['endDate']['month']
    end_day = anime_data['data']['Media']['endDate']['day']
    end_date = f"{end_day}/{end_month}/{end_year}"
    
    if f"{end_day}/{end_month}/{end_year}" == f"{None}/{None}/{None}":
        end_date = "N/A"
    elif f"{end_day}/{end_month}/{end_year}" == f"{None}/{None}/{end_year}":
        end_date = f"?/?/{end_year}"
    else:
        end_date = f"{end_day}/{end_month}/{end_year}"
    
    sources = {
        "ORIGINAL": "Original",
        "MANGA": "Manga",
        "LIGHT_NOVEL": "Light Novel",
        "VISUAL_NOVEL": "Visual Novel",
        "VIDEO_GAME": "Video Game",
        "OTHER": "Other",
        "NOVEL": "Novel",
        "DOUJINSHI": "Doujinshi",
        "ANIME": "Anime",
        "WEB_NOVEL": "Web Novel",
        "LIVE_ACTION": "Live Action",
        "GAME": "Game",
        "COMIC": "Comic",
        "MULTIMEDIA_PROJECT": "Multimedia Project",
        "PICTURE_BOOK": "Picture Book",
    }
    
    source = sources.get(anime_data['data']['Media']['source'], "N/A")
    
    if anime_data['data']['Media']['description'] == None:
        description = "N/A"
    else:
        import re
        def remove_html_tags(text):
            clean = re.compile('<.*?>')
            return re.sub(clean, '', text)
        description = remove_html_tags(anime_data['data']['Media']['description'])
    
    context = {
        'anime_data': anime_data['data']['Media'],
        'format': format,
        'episode_duration': episode_duration,
        'episodes': episodes,
        'status': status,
        'source': source,
        'season': season,
        'score': score,
        'start_date': start_date,
        'end_date': end_date,
        'description': description,
        'relation_length': len(anime_data['data']['Media']['relations']['edges'])
    }
    return render(request, 'anime-view.html', context)

def search_view(request, search_query):
    from django.http import JsonResponse
    
    query = '''
    query ($title: String) {
    Page {
        media (search: $title, type: ANIME, isAdult: false) {
            id
            title {
                romaji
                english
                native
            }
            description
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            season
            episodes
            trailer {
                id
                thumbnail
            }
            relations {
            edges {
                id
                relationType
                node {
                    title {
                        romaji
                        english
                        native
                    }
                }         
            }
        }
        duration
        format
        status
        studios {
            nodes {
                id
                name
            }
        }
        genres
        source
        stats {
            scoreDistribution {
            amount
            }
        }
        averageScore
        popularity
        favourites
        coverImage {
            large
            extraLarge
        }
        bannerImage
    }
    }
    }'''
    
    variables = {
        'title': search_query,
    }

    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        print(f"Error: {response.status_code}")
            

        
    
