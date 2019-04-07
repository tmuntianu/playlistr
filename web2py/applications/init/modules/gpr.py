import sklearn.gaussian_process
from sklearn.gaussian_process import GaussianProcessRegressor
import numpy as np
import spotipy
import spotipy.util
import playlist

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

dnp = 1 # distance normalizing parameter
adv = 0.3 # adventurousness, scaled between 0 and 1

token_info = playlist.refreshToken('AQCs5y17o1Fgoe9eRrtLrsee2Wv6qzgc1uSQe7ed5nYTKOa6Uuun1WUQuzVCT9R-bZ8OBCtDGMgHzuXd0HZEK6DE-Oyq9dMafpnmaYb8OkpRDpMj6P9NJAiZxg3EJrIcw8A4vQ')
token = token_info['access_token']
tokens = [token]
sp_objs = create_sp_objs(tokens)
track_ids = get_all_track_ids(sp_objs)
features = get_audio_features(track_ids, token)

(n, m) = features.shape
distances = np.zeros(shape=n, dtype=float)
dist_max = 0
for i in range(0, n-1):
    norm_i = np.linalg.norm(features[i])
    norm_i_1 = np.linalg.norm(features[i+1])
    dist = np.sign(norm_i - norm_i_1)*np.linalg.norm(norm_i - norm_i_1)
    if dist > dist_max:
        dist_max = dist
    distances[i] = dist

distances = np.divide(distances, dist_max / dnp)
distances[n-1] += np.abs(distances[n-2])
X = np.zeros(shape = n, dtype=float)
for i in range(0, n):
    X[i] = i % 50 + distances[i]

# gpr = GaussianProcessRegressor(normalize_y=True, n_restarts_optimizer=10).fit(X.T.reshape(-1, 1), features)
other = np.zeros(shape=n, dtype=float)
for i in range(0,50):
    other[i] += i
gpr = GaussianProcessRegressor(normalize_y=True, n_restarts_optimizer=10).fit(other.T.reshape(-1, 1), features)

i = 0
while distances[i] < adv and i < n-2:
    i += 1
sampling_loc = np.array(X[i] + 0.5 * (X[i] - X[i+1]))
print(sampling_loc)
# seed = gpr.predict(sampling_loc.reshape(1, -1))
seed = gpr.predict(np.array(25).reshape(1,-1))
print(seed)

seed_track = track_ids[0]
#recs = sp.recommendations(seed_tracks=list(seed_track),
 #                       target_danceability=seed[0][0],
  #                      target_energy=seed[0][1])