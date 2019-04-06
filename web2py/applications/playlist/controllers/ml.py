import spotipy
testToken = 'BQAAF3xdLe2IhFRxP63ajBje3fztMAjOD4s60Dbzt8WAh3zH3Mtp9e2weoMrv_34RG872sA3lo731e8_ww5S2yJmT33e1f-wJTBDaDJnPd_3v2jtjS_aVId1owBDaZCu7Aq4l0w6wCwwmJl1jaN64y5LM0AfCrrCn_GtXIzQZOeYjiQG5TpZ6g'
testTokens = []
testTokens.append(testToken)
def getTopTracks(sps):
	topList = []

	for sp in sps:
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

	return (bestArray[0:3], newTracks)

def getTracksByGenre(genresNewTracks):
	print(genresNewTracks)
	genreDict = {}
	print(genresNewTracks[0])
	for genre in genresNewTracks[0]:
		genreDict[genre] = []
	for track in genresNewTracks[1]:
		for genre in genresNewTracks[0]:
			if genre in track["genres"]:
				genreDict[genre].append(track)
	print(genreDict)
	return genreDict

def featureVectors(tracksbyGenre):
	track_list = []

	for item in tracksbyGenre.keys(): # list of tracks
		track_list.append(item)

	feature_list = audio_features(track_list)
	print(feature_list)

# Given a dictionary from genre to list of tracks
# Take every song in that genre
# Average each's audio features
# create a new vector
# return this vector as the seed


# def getTopGenres(tracks):
#
# def getTracksByGenre(tracks, genres):
#
# def getFeatureVectors(tracksbyGenre):
#
# def getTracksFromSeed(featureVectors):


# def generatePlaylists(ownerToken, tokens):
# 	sps = authSpotipy(tokens)
# 	tracks = getTopTracks(sps) #put all the top tracks into one list
# 	genres = getTopGenres(tracks) # get the top 3 genres
# 	tracksByGenre = getTracksByGenre(tracks, genres) #return dictionary of genre names to tracks
# 	featureVectors = getFeatureVectors(tracksByGenre) #returns a dictionary of genre names to feature vectors
# 	playlists = getTracksFromSeed(featureVectors) #returns a dictionary of genre name to track array
# 	createPlaylists(ownerToken, playlists) #creates playlists in the owner's account

def authSpotipy(tokens):
	sps = []
	for token in tokens:
		sps.append(spotipy.Spotify(auth=token))
	return sps

def authSpotipyOwner(token):
	return spotipy.Spotify(auth=token)

sps = authSpotipy(testTokens)
sp = authSpotipyOwner(testToken)
tracks = getTopTracks(sps)
getTracksByGenre(getTopGenres(tracks, sp))
#generatePlaylists(testToken, testTokens)

