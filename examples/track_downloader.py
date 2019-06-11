from context import gmusicripper

client = gmusicripper.performoauth()
access_token = client.session._oauth_creds.access_token
gmusicripper.get_mp3(gmusicripper.search_storeid_track(input("Enter keywords (Title, Artist...) of the song you'd like to download: "),
                                       access_token), access_token, 'Fetched')
