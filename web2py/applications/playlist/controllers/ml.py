import spotipy
import spotipy.util
testToken = 'BQBrWxT62zOd6ci1C0sTIs7Vn8wZ3teazf3fjFlUGAt774nfdGLhUblcu-xHw4QXvXh8qman9h5Nn2AvQaDdDSkUWpvuGYWPPbnkdhcry1dI_Bj4GIuibjUzUyAr5szzum1MHL8uPzH6DNNW8Gatoa_xuclAQS1tMafEH5wHkjfEDAe-OG4Ww3vRCad87g'
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



def createPlaylists(sp, currentUserId, tracksLists):
	print (sp.user_playlist_create(currentUserId, "Test Playlist1"))




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
#	sp = authSpotipyOwner(ownerToken)
#	currentUserId = sp.current_user()['id']
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

def refreshToken():
	scope = 'user-top-read playlist-modify-public'
	client_id="22afe11d6c9a4302804622924738a872"
	client_secret="f6ab191a59de4b59af13dc44d7ec16c5"
	redirect_uri="http://127.0.0.1:8000/init/default/auth_success"
	oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
	return oauth.refresh_access_token('AQDSHea-PFwOCyu2RSB7nmqwqaGXwvFUaOQ_PIeyOsHlc2qCDJweevuk3fXPVcFFg1_Zuf_ULMa6gc7xnfmPPXdnwtal-eEE8gxkyRW4fhDepsY064159ST4xJrzFtgFbbKh3Q')


'''
sps = authSpotipy(testTokens)
sp = authSpotipyOwner(testToken)
currentUserId = sp.current_user()
createPlaylists(sp, currentUserId, [])
#tracks = getTopTracks(sps)
#getTracksByGenre(getTopGenres(tracks, sp))
#generatePlaylists(testToken, testTokens)
'''