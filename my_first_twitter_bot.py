import tweepy
import time

print("this is my 1st twitter bot", flush=True)

# You have to get a twiter developer account to get this custom information
CONSUMER_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
CONSUMER_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
ACCESS_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Authorization to consumer key and consumer secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# Access to user's access key and access secret
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
# Calling api
api = tweepy.API(auth)

#two file names, one for each task
#there is probably a better way
FILE_NAME1 = 'last_seen_id.txt'
FILE_NAME2 = 'last_seen_id2.txt'

#retrieve the last seen id to prevent messaging users twice
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = f_read.read().strip()
    if last_seen_id == '':
        last_seen_id = 0
    f_read.close()
    return last_seen_id
#stores the last id messaged to prevent resending messages
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# Function to extract tweets based on the user target and desired behavior
# searching = 1     "oh hi user"
# searching = 2     "what a story trump!"
def get_tweets(username,searching):
    print('Retrieving tweets...')
    if searching == 1:
        last_seen_id = retrieve_last_seen_id(FILE_NAME1)
        print("last_seen_id=" + str(last_seen_id))
        tweets = api.mentions_timeline(last_seen_id, tweet_mode='extended')
        return tweets
    elif searching == 2:
        last_seen_id = retrieve_last_seen_id(FILE_NAME2)
        print("last_seen_id=" + str(last_seen_id))

    # 100 tweets to be extracted
    number_of_tweets=20
    #tweets = api.user_timeline(screen_name=username,since_id=last_seen_id,count=number_of_tweets)
    tweets = api.user_timeline(screen_name=username,count=number_of_tweets)

    length = len(tweets)
    # create array of tweet information: username,
    # tweet id, date/time, text
    tweets_for_id  = [tweet.id for tweet in tweets]
    tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created
    for j in range(length):
        print(str(tweets_for_id[j]) + ": " + tweets_for_csv[j])

    # Returns a string of tweet IDs
    return tweets

#Respond to Trumps tweets with Jonny's favorite catch phrase
def what_a_story(tweets):
    print('replying to tweets...', flush=True)

    for twt in tweets:
        #print(str(mention) + ' - ' + mention.full_text, flush=True)
        print('responding to ID: ' + str(twt.id))
        last_seen_id = twt.id
        store_last_seen_id(last_seen_id, FILE_NAME2)

        print('')
        try:
            api.update_status('@' + twt.user.screen_name +' Ah ha ha ha. What a story Trump!', twt.id)
        except tweepy.TweepError as error:
            if error.api_code == 187:
                print('duplicate message')
            else:
                raise error
#gathers recent tweets sent to user and checks if they are using any of the mentioned
#greetings and responds back with a greeting
def oh_hi(tweets):
    for twt in reversed(tweets):
        print(str(twt.id) + ' - ' + twt.full_text, flush=True)
        last_seen_id = twt.id
        store_last_seen_id(last_seen_id, FILE_NAME1)
        if ('hi'           in twt.full_text.lower() or
            'hello'        in twt.full_text.lower() or
            'sup'          in twt.full_text.lower() or
            'hey'          in twt.full_text.lower() or
            'whats up'     in twt.full_text.lower() or
            'good morning' in twt.full_text.lower() or
            'good night'   in twt.full_text.lower() or
            'greetings'    in twt.full_text.lower()):
            print('found hi or hello or sup')
            print('responding back...')
            api.update_status('Oh hi @' + twt.user.screen_name, twt.id)

# Driver code
if __name__ == '__main__':

  # Here goes the twitter handle for the user
  # whose tweets are to be extracted.
  # get_tweets("@MrRobott0")
  while True:
      #tweets = get_tweets("@xxxxxxxxxxx", 1)
      #oh_hi(tweets)
      #time.sleep(15)
      tweets = get_tweets("@realDonaldTrump", 2)
      what_a_story(tweets)
      time.sleep(15)
