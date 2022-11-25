import json
import boto3
from urllib.parse import unquote_plus


def extract_text(response, extract_by="LINE"):
    line_text = []
    str1 = "\n"
    for block in response["Blocks"]:
    if block["BlockType"] == extract_by:
    line_text.append(block["Text"])
    return str1.join(line_text)


def lambda_handler(event, context):
    textract = boto3.client("textract")
    if event:
    file_obj = event["Records"][0]
    bucketname = str(file_obj["s3"]["bucket"]["name"])

    filename = unquote_plus(str(file_obj["s3"]["object"]["key"]))
    print(f"Bucket: {bucketname} ::: Key: {filename}")
    response = textract.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": bucketname,
                "Name": filename,
            }
        }
    )
    print(json.dumps(response))

    # change LINE by WORD if you want word level extraction
    raw_text = extract_text(response, extract_by="LINE")
    print(raw_text)
    s3 = boto3.client("s3")
    bucket = "sjcomprehendbucket"
    with open("/tmp/raw_text.txt", "w") as f:
    f.write(str(raw_text))
    client = boto3.resource("s3")
    client.meta.client.upload_file("/tmp/raw_text.txt", bucket, "raw_text.txt")
    return {
        "statusCode": 200,
        "body": json.dumps("Document processed successfully!"),
    }

    return {"statusCode": 500, "body": json.dumps("There is an issue!")}
