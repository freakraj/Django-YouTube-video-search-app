import requests
from isodate import parse_duration

from django.shortcuts import render,redirect
from django.conf import settings

# Create your views here.

def index(request):
    videos = []
    # this condition for form submit to click submit button
    if request.method =='POST':

        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url ='https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part':'snippet',
            # this q key here for searching results (input text to write some text
            # then click submit button
            # to search result)
            'q':request.POST['search'],
            'key':settings.YOUTUBE_DATA_API_KEY,
            'maxResults':12,
            'type':'video'
        }
        r = requests.get(search_url,params=search_params)
        results = r.json()['items']
        video_id = []
    
        for result in results:
            video_id.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_id[0] }')
    
        video_params = {
            'key':settings.YOUTUBE_DATA_API_KEY,
            'part':'snippet,contentDetails',
            'id': ',' .join(video_id),
            'maxResults':12
        }
        r = requests.get(video_url,params=video_params)
        results = r.json()['items']
    
        for result in results:
            video_data = {
                'title':result['snippet']['title'],
                'id':result['id'],
                'url':f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration':int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'thumbnails':result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
    context = {
        'videos':videos
    }
    return render(request, 'search/index.html', context)
