import json
def lambda_handler(event, context):
import codecs
from boto3 import Session
from boto3 import resource
session = Session(region_name="us
-east
-1")
polly = session.client("polly")
s3 = resource('s3')
bucket_name = "sjpollybucket"
bucket = s3.Bucket(bucket_name)
filename = "audio.mp3"
myText = """
Hello
"""
response = polly.synthesize_speech(
Text=myText,
25
OutputFormat="mp3",
VoiceId="Matthew")
stream = response["AudioStream"]
bucket.put_object(Key=filename, Body=stream.read())