from imgur import Imgur


client = Imgur(config_file='./tests/imgur.json')
client.authorize()
