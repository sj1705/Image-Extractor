
import boto3
from pprint import pprint


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    bucket = "sjcomprehendbucket"
    key = "raw_text.txt"
    file = s3.get_object(Bucket=bucket, Key=key)
    paragraph = str(file["Body"].read())
    comprehend = boto3.client("comprehend")
    # Extracting sentiments using comprehend
    sentiment = comprehend.detect_sentiment(Text=paragraph, LanguageCode="en")
    sentiment = str(sentiment)
    print(sentiment)
    emotion = sentiment[15:23]
    s3 = boto3.client("s3")
    bucket = "sjcomprehendbucket"
    with open("/tmp/emotion.csv", "w") as f:



f.write(str(emotion))
client = boto3.resource("s3")
client.meta.client.upload_file("/tmp/emotion.csv", bucket, "emotion.csv")

s3 = boto3.client("s3")
bucket = "sjpollybucket"
with open("/tmp/raw_text.txt", "w") as f:
    f.write(str(paragraph))
    client = boto3.resource("s3")
    client.meta.client.upload_file("/tmp/raw_text.txt", bucket, "raw_text.txt")
    return "Thanks"
