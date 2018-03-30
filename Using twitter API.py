#using twtiier API 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey = 'consumer key'
csecret = 'consumer secret'
atoken = 'access token'
asecret = 'secret access token'

#all keys are based off of personal developer account 

class listener(StreamListener):

    def on_data(self, raw_data):
        def on_data(self, raw_data):
            print(raw_data) #this will print out raw JSON format tweets 
            #see https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object for twitter JSON object documentation 

        saveFile = open('filename.csv', 'a') #appending 
        saveFile.write(raw_data)
        saveFile.close()
        return True

    def on_error(self, status_code):
        print(status_code)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#declare the keywords you would like to filter for tweets
twitterStream.filter(track=["Duke","Loyola","Texas Tech"])


