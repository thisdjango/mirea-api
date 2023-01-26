import requests
from mirea_video.config import CDATA
from mirea_video.models import VideoData
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

def index_page(request):
    return render(request, 'index.html')


def get_playlist_data():
    context = {'items': []}
    playlist_url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={CDATA.CHANNEL_ID}&maxResults=50&key={CDATA.TOKEN}"
    r = requests.get(playlist_url)
    data = r.json()
    for value in data['items']:
        context['items'].append(get_video_data(value))
    return context


def get_video_data(playlist):
    videos = []
    id = playlist['id']
    title = playlist['snippet']['title']
    video_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={id}&key={CDATA.TOKEN}"
    v = requests.get(video_url)
    vdata = v.json()
    items = vdata['items']
    for item in items:
        print(item)
        snippet = item['snippet']
        try:
            image_url = snippet['thumbnails']['high']['url']
        except KeyError:
            try:
                image_url = snippet['thumbnails']['default']['url']
            except KeyError:
                image_url = 'https://placehold.jp/c0c0c0/ffffff/195x146.png?text=No%20photo'
        item = VideoData(
            playlist_id=id,
            playlist_title=title,
            video_id=snippet['resourceId']['videoId'],
            name=snippet['title'],
            description=snippet['description'],
            image_url=image_url
        )
        item.save()
        dict_obj = model_to_dict(item)
        videos.append(dict_obj)
    return videos


def video_page(request):
    context = get_playlist_data()
    print(context)
    return JsonResponse(context)
