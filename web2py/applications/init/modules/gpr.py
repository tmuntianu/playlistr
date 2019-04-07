import sklearn.gaussian_process
from sklearn.gaussian_process import GaussianProcessRegressor
import numpy as np
import spotipy
import spotipy.util
import playlist as pl 
import heapq

def create_sp_objs(tokens):
    sp_objs = []
    for token in tokens:
        sp_objs.append(spotipy.Spotify(auth=token))
    return sp_objs

def get_all_track_ids(sp_objs):
    track_ids = []
    for sp in sp_objs:
        json = sp.current_user_top_tracks(limit=50)
        for item in json['items']:
            track_ids.append(item['id'])
    return track_ids

def get_seed_genres(sp_objs):
    genre_by_count = {}
    for sp in sp_objs:
        json = sp.current_user_top_tracks(limit=50)
        for item in json['items']:
            for genre in item['genres']:
                if genre_by_count[genre]:
                    genre_by_count[genre] += 1
                else:
                    genre_by_count[genre] = 1
    h =[]
    for genre in genre_by_count:
        genre_count = (genre_by_count[genre], genre)
        heapq.heappush(h, genre_count)
    return heapq.nlargest(5, h)

def get_audio_features(track_ids, token):
    features = np.ndarray(shape=(len(track_ids),11), dtype=float)
    sp = spotipy.Spotify(auth=token)
    for x in range(0, int(np.floor(len(track_ids)/100)) + 1):
        json = sp.audio_features(tracks=track_ids[x*100:(x+1)*100])
        i = 0
        for audio_features in json:
            features[i] = [audio_features['danceability'], audio_features['energy'], audio_features['key'], audio_features['loudness'], audio_features['mode'], audio_features['speechiness'], audio_features['acousticness'], audio_features['instrumentalness'], audio_features['liveness'], audio_features['valence'], audio_features['tempo']]
            i += 1
    return features

dnp = 4 # distance normalizing parameter
adv = 0.8 # adventurousness, scaled between 0 and 1

token_info = pl.refreshToken('AQCs5y17o1Fgoe9eRrtLrsee2Wv6qzgc1uSQe7ed5nYTKOa6Uuun1WUQuzVCT9R-bZ8OBCtDGMgHzuXd0HZEK6DE-Oyq9dMafpnmaYb8OkpRDpMj6P9NJAiZxg3EJrIcw8A4vQ')
token = token_info['access_token']
tokens = [token]
sp_objs = create_sp_objs(tokens)
track_ids = get_all_track_ids(sp_objs)
features = get_audio_features(track_ids, token)
seed_genres = get_seed_genres(sp_objs)

(n, m) = features.shape
distances = np.zeros(shape=n, dtype=float)
dist_max = 0
for i in range(0, n-1):
    norm_i = np.linalg.norm(features[i])
    norm_i_1 = np.linalg.norm(features[i+1])
    dist = np.sign(norm_i - norm_i_1)*np.linalg.norm(features[i] - features[i+1])
    # dist = np.linalg.norm(features[i]-features[i+1]) normal GPR
    if dist > dist_max:
        dist_max = dist
    distances[i] = dist

distances = np.divide(distances, dist_max / dnp)
distances[n-1] += np.abs(distances[n-2])
X = np.zeros(shape = n, dtype=float)
for i in range(0, n):
    X[i] = i % 50 + distances[i]

gpr = GaussianProcessRegressor(normalize_y=True, n_restarts_optimizer=10).fit(X.T.reshape(-1, 1), features)
# other = np.zeros(shape=n, dtype=float)
# for i in range(0,50):
#     other[i] += i
# gpr = GaussianProcessRegressor(normalize_y=True, n_restarts_optimizer=10).fit(other.T.reshape(-1, 1), features)

i = 5
while distances[i] < adv * dnp and i < n-5:
    i += 1

sampling_loc = np.array(X[i] + 0.5 * (X[i] - X[i+1]))

seed = gpr.predict(sampling_loc.reshape(1, -1))

json = sp_objs[0].recommendations(seed_tracks=[], seed_artists=[], seed_genres=seed_genres,
                       target_danceability=seed[0][0],
                       target_energy=seed[0][1],
                       target_key=int(seed[0][2]),
                       target_loudness=seed[0][3],
                       target_mode=int(seed[0][4]),
                       target_speechiness=seed[0][5],
                       target_acousticness=seed[0][6],
                       target_instrumentalness=seed[0][7],
                       target_liveness=seed[0][8],
                       target_valence=seed[0][9],
                       target_tempo=seed[0][10])

playlist_track_ids =[]
for track in json['tracks']:
    playlist_track_ids.append(track['id'])

user_id = sp_objs[0].current_user()['id']
playlist_id = sp_objs[0].user_playlist_create(user_id, 'GPR')['id']
sp_objs[0].user_playlist_add_tracks(user_id, playlist_id, playlist_track_ids)
