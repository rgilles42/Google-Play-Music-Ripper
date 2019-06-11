import func

client = func.performoauth()
access_token = client.session._oauth_creds.access_token
func.get_mp3(func.search_storeid_track(input("Enter keywords (Title, Artist...) of the song you'd like to download: "),
                                       access_token), access_token, 'Fetched')
