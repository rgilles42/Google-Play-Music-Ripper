import func

client = func.performoauth()
access_token = client.session._oauth_creds.access_token

var = client.get_all_songs(incremental=False)
count = 1
for i in var:
    print(str(count) + "/" + str(len(var)))
    func.get_mp3(i, access_token, 'Music')
    count += 1
