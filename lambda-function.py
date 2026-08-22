import json
import boto3
from datetime import datetime

s3 = boto3.client("s3")

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="ap-south-1"
)

BUCKET_NAME = "daily-adventure-agent-mayur-2026"

def lambda_handler(event, context):

    prompt = """
Create today's unique short adventure story.

Requirements:
- 150 words maximum
- Set the adventure in Maharashtra, India
- Include a trekking or exploration theme
- Give the story a creative title
- Make it different and interesting
- Return only the title and story
"""

    response = bedrock.converse(
      modelId="apac.amazon.nova-micro-v1:0",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    )

    story_text = response["output"]["message"]["content"][0]["text"]

    story = {
        "generated_at": datetime.utcnow().isoformat(),
        "content": story_text
    }

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="daily-story.json",
        Body=json.dumps(story),
        ContentType="application/json"
    )

    return {
        "statusCode": 200,
        "body": json.dumps(story)
    }
