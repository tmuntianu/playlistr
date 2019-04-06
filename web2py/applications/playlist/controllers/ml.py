import spotipy
testToken = 'BQDKqL5z7gDn9ocYfBooOqEfxda5CupMn9QCJ66IQJpOhftLblXPrzxEpXoNP6AHzCShBAPZM66drem__N3uTmf91ONU0-rx1RUmfv5vcGuN80CQ_B1d8VKmYHgSfMuZag1IT4EN9UDYvqcCgukmAcwT'
testTokens = []
testTokens.append(testToken)
def getTopTracks(sps):



def getTopGenres(tracks):
	counter = {}
	for track in tracks:








def generatePlaylists(ownerToken, tokens):
	sps = authSpotipy(tokens)
	tracks = getTopTracks(sps) #put all the top tracks into one list
	genres = getTopGenres(tracks) # get the top 3 genres
	tracksByGenre = getTracksByGenre(tracks, genres) #return dictionary of genre names to tracks
	featureVectors = getFeatureVectors(tracksByGenre) #returns a dictionary of genre names to feature vectors
	playlists = getTracksFromSeed(featureVectors) #returns a dictionary of genre name to track array
	createPlaylists(ownerToken, playlists) #creates playlists in the owner's account



def authSpotipy(tokens):
	sps = []
	for token in tokens
		sps.append(spotipy.Spotify(auth=token))
	return sps



generatePlaylists(testToken, testTokens)