import spotipy
import spotipy.util

def authSpotipy(tokens):
	sps = []
	for token in tokens:
		sps.append(spotipy.Spotify(auth=token))
	return sps

def authSpotipyOwner(token):
	return spotipy.Spotify(auth=token)

def refreshToken():
	scope = 'user-top-read playlist-modify-public'
	client_id="22afe11d6c9a4302804622924738a872"
	client_secret="f6ab191a59de4b59af13dc44d7ec16c5"
	redirect_uri="http://127.0.0.1:8000/init/default/auth_success"
	oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
	return oauth.refresh_access_token('AQDSHea-PFwOCyu2RSB7nmqwqaGXwvFUaOQ_PIeyOsHlc2qCDJweevuk3fXPVcFFg1_Zuf_ULMa6gc7xnfmPPXdnwtal-eEE8gxkyRW4fhDepsY064159ST4xJrzFtgFbbKh3Q')


testToken = 'BQBrWxT62zOd6ci1C0sTIs7Vn8wZ3teazf3fjFlUGAt774nfdGLhUblcu-xHw4QXvXh8qman9h5Nn2AvQaDdDSkUWpvuGYWPPbnkdhcry1dI_Bj4GIuibjUzUyAr5szzum1MHL8uPzH6DNNW8Gatoa_xuclAQS1tMafEH5wHkjfEDAe-OG4Ww3vRCad87g'
testTokens = []
testToken = refreshToken()['access_token']
testTokens.append(testToken)


def getTopTracks(sp):
	topList = []
	tempTracks = sp.current_user_top_tracks(limit = 50, offset = 0, time_range = 'medium_term')
	for item in tempTracks["items"]:
		topList.append(item)

	return topList


def getArtist(track, sp):
	return sp.artist(track["artists"][0]["id"])


def getTopGenres(tracks, sp):
	genres = {}
	newTracks = []

	for track in tracks:
		newTrack = track
		newTrack["genres"] = []
		artist = getArtist(track, sp)
		# genre = ""
		if len(artist["genres"]) > 0:
			for subGenre in artist["genres"]:
				newTrack["genres"].append(subGenre)
				if subGenre in genres:
					genres[subGenre] +=1
				else:
					genres[subGenre] = 1
		newTracks.append(newTrack)

	firstCount = 0
	secondCount = 0
	thirdCount = 0

	bestArray = []

	for key in genres.keys():
		if genres[key] >= firstCount:
			bestArray.insert(0, key)
			firstCount = genres[key]
		elif genres[key] >= secondCount:
			bestArray.insert(1, key)
			secondCount = genres[key]
		elif genres[key] >= thirdCount:
			bestArray.insert(2, key)
			thirdCount = genres[key]

	return (bestArray[0:3], newTracks, sp)


def getTracksByGenre(genresNewTracks):
	sp = genresNewTracks[2]

	genreDict = {}
	for genre in genresNewTracks[0]:
		genreDict[genre] = []
	for track in genresNewTracks[1]:
		for genre in genresNewTracks[0]:
			if genre in track["genres"]:
				genreDict[genre].append(track)

	return genreDict, sp


def featureVectors(tracksbyGenre):
	# Given a dictionary from genre to list of tracks
	# Take every song in that genre
	# Average each's audio features
	# create a new vector
	# return this vector as the seed
	track_list = []

	genreMap = tracksbyGenre[0]
	sp = tracksbyGenre[1]

	for item in genreMap.keys(): # list of tracks
		for track in genreMap.get(item):
			track_list.append(track["id"])

	feature_list = sp.audio_features(track_list)

	feature_dict = {}
	relevant_features = ["danceability", "energy", "key", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

	for feature in relevant_features:
		feature_dict[feature] = 0

	for trackAndFeatures in feature_list:
		for feature in relevant_features:
			feature_dict[feature] += trackAndFeatures[feature]

	target_vector = []

	for feature in relevant_features:
		feature_dict[feature] = (feature_dict[feature]/len(feature_list))
		average_feature = feature_dict[feature]
		target_vector.append(average_feature)

	return target_vector, sp


def getSongsBySeed(target):
	target_vector = target[0]
	sp = target[1]

	track_seeds = []
	top_tracks = sp.current_user_top_tracks(limit=1)
	for item in top_tracks["items"]:
		track_seeds.append(item["id"])

	recommendation_songs = sp.recommendations(seed_tracks = track_seeds, limit = 30, target_danceability = target_vector[0], target_energy = target_vector[1], target_key = int(target_vector[2]), target_loudness = target_vector[3], target_speechiness = target_vector[4], target_acousticness = target_vector[5], target_instrumentalness = target_vector[6], target_liveness = target_vector[7], target_valence = target_vector[8], target_tempo = target_vector[9], target_time_signature = int(target_vector[10]))

	title_list = []
	for song in recommendation_songs['tracks']:
		title_list.append(song["name"])

	return recommendation_songs['tracks']#, sp


def compileRecommendations(sps):
	totalAverageVector = []
	for i in range(11):
		totalAverageVector.append(0) #All entries start as zero, get added to  by each userAverageVector

	for sp in sps:
		userTopTracks = getTopTracks(sp) #5 lists of top 50 tracks
		userTopGenres = getTopGenres(userTopTracks, sp) #list of top 3 genres for that user
		userGenreDict = getTracksByGenre(userTopGenres) #dictionary of user songs sorted by genre
		userAverageVector = featureVectors(userGenreDict) #average metrics of top 3 genres for that user

		for i in range(len(userAverageVector[0])): #Add user's Av. vector to group vector
			totalAverageVector[i] += userAverageVector[0][i]
			i+=1

	for i in range(len(totalAverageVector)):
		totalAverageVector[i] = (totalAverageVector[i]/len(sps))

	passList = []
	passList.append(totalAverageVector)
	passList.append(sps[0])

	groupRecSongs = getSongsBySeed(passList) #recommended song object list for that group

	return (list(groupRecSongs), sps[0])


def createPlaylists(currentUserId, trackList, owner):
	sp = owner

	trackIDList = []
	trackNameList = []
	for item in trackList:
		trackIDList.append(item["id"])
		trackNameList.append(item["name"])


	playlist = sp.user_playlist_create(currentUserId, "Your Carpool Playlist")

	sp.user_playlist_add_tracks(currentUserId, playlist["id"], trackIDList)

	print(trackNameList)


def main(userList):
	spList = []

	for userSD in userList:
		spList.append(userSD)

	trackList, owner = compileRecommendations(spList)
	owner = userList[0]
	userID = owner.current_user()['id']
	createPlaylists(userID, trackList, owner)


sps = authSpotipy(testTokens)
sp = authSpotipyOwner(testToken)
x = [sp]
main(x)


#Todo done:
# 	tracks = getTopTracks(sps) #put all the top tracks into one list
# 	genres = getTopGenres(tracks) # get the top 3 genres
# 	tracksByGenre = getTracksByGenre(tracks, genres) #return dictionary of genre names to tracks
# 	featureVectors = getFeatureVectors(tracksByGenre) #returns a dictionary of genre names to feature vectors
# 	playlists = getTracksFromSeed(featureVectors) #returns a dictionary of genre name to track array

#Todo:
# 	createPlaylists(ownerToken, playlists) #creates playlists in the owner's account

# sps = authSpotipy(testTokens)
# sp = authSpotipyOwner(testToken)
# currentUserId = sp.current_user()['id']
# createPlaylists(sp, currentUserId, [])
#tracks = getTopTracks(sps)
#getTracksByGenre(getTopGenres(tracks, sp))
#generatePlaylists(testToken, testTokens)
