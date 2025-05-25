from dotenv import load_dotenv, find_dotenv
import os
import base64
from requests import post,get,put
import json
# from speechtotext import *

#path="C:\Users\krish\OneDrive\Desktop\Project 1 Virtual Assistant\Spotify API"
BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(find_dotenv())

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") 
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers= headers,data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers= get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("Artist not found.")
        return None
    return json_result[0]

def search_for_track(token,track_name):
    url = "https://api.spotify.com/v1/search"
    headers= get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"
    
    query_url = url + query
    
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("song not found.")
        return None
    return json_result[0]

def get_device_id(token):
    url = "https://api.spotify.com/v1/me/player/devices"
    headers=get_auth_header(token)
    result = get(url,headers=headers)
    json_result=json.loads(result.content)
    return json_result

def get_songs_by_artist(token,artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers= get_auth_header(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def play_song_old(token,name):
    url = "https://api.spotify.com/v1/me/player/play"
    headers = get_auth_header(token)
    uri = search_for_track(token,name)['uri']
    print(uri)
    data = {
        "uris" : [f"{uri}"]
    }
    result = put(url,data=json.dumps(data),headers=headers)
    print(result.status_code)

def play_song(token,ip):
    url = "https://api.spotify.com/v1/search"
    headers= get_auth_header(token)
    name = get_song_from_user(ip)
    query = f"?q={name}&type=track&limit=50"
    
    query_url = url + query
    
    result = get(query_url,headers=headers)
    tracks = result.json()['tracks']['items']
    ipartist=get_artist_from_user(ip)
    print(ipartist)
    flag = False
    track = None
    for i in range(len(tracks)):
        artist_name = tracks[i]['album']['artists'][0]['name'].lower()
        track = tracks[i]
        artist_name = [i for i in artist_name if ord(i) >= 97 and ord(i)<=122]
        artist_name="".join(artist_name)
        if artist_name == ipartist:
            flag = True
            break
    if flag:
        uri = track['uri']
        url = "https://api.spotify.com/v1/me/player/play"
        headers = get_auth_header(token)
        data = {
            "uris" : [f"{uri}"]
        }
        result = put(url,data=json.dumps(data),headers=headers)
        print(result.status_code)
    else:
        print("Track not found")
        
    
    
def skip_song(token):
    url = "https://api.spotify.com/v1/me/player/next"
    headers = get_auth_header(token)
    response = post(url,headers=headers)
    print(response.status_code)
    
def seek_song(token):
    url = "https://api.spotify.com/v1/me/player/previous"
    headers = get_auth_header(token)
    response = post(url,headers=headers)
    print(response.status_code)

def set_volume(token,value):
    url = "https://api.spotify.com/v1/me/player/volume"
    query=f"?volume_percent={value}"
    url_final = url + query
    headers = get_auth_header(token)
    # data = {
    #     "volume_percent" : value
    # }
    response = put(url_final,headers=headers)
    print(response.status_code)

def toggle_shuffle(token):
    url="https://api.spotify.com/v1/me/player/shuffle"
    shuffle_state = get_playback_state(token)['shuffle_state']
    shuffle_state = str(not shuffle_state).lower()
    print(shuffle_state)
    query_url = url + f"?state={shuffle_state}"
    headers = get_auth_header(token)
    response = put(query_url,headers=headers)
    print(response.status_code)

def get_playback_state(token):
    url = "https://api.spotify.com/v1/me/player"
    headers = get_auth_header(token)
    response = get(url,headers=headers)
    res_obj = response.json()
    return res_obj

def repeat_track(token):
    url = "https://api.spotify.com/v1/me/player/repeat?state=track"
    headers = get_auth_header(token)
    response = put(url,headers=headers)
    print(response.status_code)

def get_playlists(token):
    url = "https://api.spotify.com/v1/me/playlists?limit=50"
    headers = get_auth_header(token)
    response = get(url,headers=headers)
    #print(response.status_code)
    obj = response.json()
    playlists = obj['items']
    return playlists

def play_playlist(token,name):
    url = "https://api.spotify.com/v1/me/player/play"
    headers = get_auth_header(token)
    playlists = get_playlists(token)
    pl = 0
    for i in range(len(playlists)):
        pl = playlists[i]
        if(pl['name'].lower() == name):
            break
    if pl == 0:
        print("Playlist not found")
    else:
        uri = pl['uri']
        data = {
            "context_uri" : f"{uri}"
        }
        response = put(url,data=json.dumps(data),headers=headers)
        print(response.status_code)

def volume_up_down(token,command):
    pbstate = get_playback_state(token)
    cur_vol = int(pbstate['device']['volume_percent'])
    if command.lower() == "up":
        cur_vol+=10
    elif command.lower() == "down":
        cur_vol-=10
    else:
        pass
    set_volume(token,cur_vol)
    
def pause(token):
    url = "https://api.spotify.com/v1/me/player/pause"
    headers = get_auth_header(token)
    response = put(url,headers=headers)
    print(response.status_code)

def resume(token):
    url = "https://api.spotify.com/v1/me/player/play"
    headers = get_auth_header(token)
    response = put(url,headers=headers)
    print(response.status_code)

def add_to_queue(token,name):
    url = "https://api.spotify.com/v1/me/player/queue"
    headers = get_auth_header(token)
    uri = str(search_for_track(token,name)['uri'])
    query_url = url + f"?uri={uri}"
    response = post(query_url,headers=headers)
    print(response.status_code)

token = get_token()
result = search_for_artist(token, "J Cole")
# print(result["followers"]["total"])
artist_id = result["id"]
songs = get_songs_by_artist(token,artist_id)

# play_song(token)
# for idx,song in enumerate(songs):
#     print(f"{idx+1}. {song['name']}")
    
# res=search_for_track(token,"No Role Modelz")
# print(res["uri"])

# res=get_device_id(token)
# print(res)

def get_song_from_user(inp):
    inp=inp.split()
    song=""
    for i in range(inp.index("play")+1,inp.index("by")):
        song+=inp[i]
    return song

def get_artist_from_user(ip):
    ip = ip.split(" ")
    ipartist=""
    for i in range(ip.index("by")+1,len(ip)):
        ipartist+=ip[i]
    ipartist=("".join(ipartist)).lower()
    return ipartist
refreshtoken = os.getenv("REFRESH_TOKEN")

def refresh_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": "AQBXYAPIeV01fGwpB02JgEuEinZktENdVWY5vHkSAH7SSTie2Bf3gavW74sTXPVIJmt-gVCGJBAPbxOcKXkRmYZdCnwLRa_EnIx_wFewg6i80G7jAloqInwARYmFZQuhhGk"
    }
    response = post(url, headers=headers, data=data)
    # json_result = json.loads(response.content)
    # print(json_result)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Failed to refresh token:", response.status_code)
        return None




def main():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    token = refresh_token(client_id,client_secret)
    # ip = speechrecog()
    # print(play_song(token,ip.lower()))
    print(get_playback_state(token))
    # print(ip)
    # print(get_song_from_user(ip.lower()))
    # play_song(token,get_song_from_user(ip.lower()))
    # print(search_for_track(token,get_song_from_user(ip.lower()))['uri'])
    # toggle_shuffle(token)
    # print(play_playlist(token,"bangers"))
    # print(search_for_track(token,"a lot"))
    # print(play_song(token,"play earthquake by tyler the creator"))
    # print(play_playlist(token,"liked songs"))
    
    
    
if __name__ == '__main__':
    main()
# ip = speechrecog()
# print(ip)
# print(get_song_from_user(ip.lower()))
# tokennew='BQBhldlCks6nd0JmFqop_BIn0N8DBFYSZfO20KOzGvENIIly0170RLtIUV0yy6UsO2Z5j70DJaLVwIAryIsFJ6iMgJRB0RpJlWSJWEJcr6OJvbAlt_Mlr71rxmqH70OMMRifqA0IBwEY1kynLEuD-8PH3yx2XMM0kJJGZzj4krYLcVX9Y4iL_hKL9DWYZPxZ3XYUDACzIzqp8C9tojQH3D-wjJzVaAsGrcB8MwwZqFwfGKp7HQZkP9TKldC9k3TS0iid5L--TJVloo5ycgnSJM-_iXBR'
# play_song(tokennew,get_song_from_user(ip.lower()))
# print(search_for_track(token,get_song_from_user(ip.lower()))['uri'])
