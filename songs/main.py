import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint


CLIENT_ID = '04701e23dc4342b091cd1e8d26faacca'
CLIENT_SECRET = 'e6f2b0e96cdd473abf107e0f48e48dfc'
REDIRECT_URI = 'http://example.com'

ACCESS_TOKEN = 'BQDf2_Gr7_YZmaOAXuD8mwCeLiC6XjS233LR--ynMHBusIdl4DVImO_FX26youhp1NvB0iYmt52NgtdeYIblxo5k8x2p3cjVhuaC4bFrAOeJcvQHiAVtt5BUaC-V4D2V4VavMXh-NzSTAEI8_njjJfJgIM7qKBvlu_WaIKoqYF5xJl1FynSDhNO2TBuO-RBrMgRXxwnPdYrdurqRaoVux2qEHKsI62R35f52QNlhKVuDhEaY3zN39yHlCNe2_NbSgre6Qrxh9_BLSIt36NOu8pRe'


sp = spotipy.Spotify(auth=ACCESS_TOKEN)


date = input("Enter the date you would like to travel to (YYYY-MM-DD): ")


url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    chart_list = soup.select('ul > li.lrv-u-width-100p > ul > li.o-chart-results-list__item')
    song_titles = []
    for item in chart_list:
        title = item.find('h3', class_='c-title')
        if title:
            song_titles.append(title.get_text(strip=True))
else:
    print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
    exit()


song_uris = []
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{date[:4]}", type='track', limit=1)
    tracks = result['tracks']['items']
    if tracks:
        song_uris.append(tracks[0]['uri'])


user_id = sp.current_user()['id']


playlist_name = f"{date} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = playlist['id']


sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=song_uris)

print(f"Playlist '{playlist_name}' created successfully with {len(song_uris)} songs.")