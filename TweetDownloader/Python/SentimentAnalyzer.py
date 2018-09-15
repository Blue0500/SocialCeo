import textblob

def Analyze():
    blob = TextBlob("this is a good day")
    return blob.sentiment