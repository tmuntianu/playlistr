import spotipy
testToken = 'BQDKqL5z7gDn9ocYfBooOqEfxda5CupMn9QCJ66IQJpOhftLblXPrzxEpXoNP6AHzCShBAPZM66drem__N3uTmf91ONU0-rx1RUmfv5vcGuN80CQ_B1d8VKmYHgSfMuZag1IT4EN9UDYvqcCgukmAcwT'
testTokens = []
testTokens.append(testToken)
def getTopTracks(sps):

    topList = []

    for sp in sps:
        topList.append(sp.current_user_top_tracks(limit = 50, offset = 0, time_range = 'medium_term'))
                       
    return topList

def getAlbum(track, sp):
	return sp.album(track["album"]["id"])

def getTopGenres(tracks, sp):
	genres = {}
	for track in tracks:
		genre = getAlbum(track, sp).genres[0]
		if genre in genres:
			genres[genre] +=1
		else:
			genres[genre] = 1

	firstCount = 0
	secondCount = 0
	thirdCount = 0

	bestArray = []

	for key in genres.keys:
		if genres[key] >= firstCount:
			bestArray.insert(0, key)
		elif genres[key] >= secondCount:
			bestArray.insert(1, key)
		elif genres[key] >= thirdCount:
			bestArray.insert(2, key)

	return bestArray[0:3]
	


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
print (getTopGenres(tracks, sp))
#generatePlaylists(testToken, testTokens)

