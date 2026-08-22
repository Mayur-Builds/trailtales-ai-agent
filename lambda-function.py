import json
import boto3
from datetime import datetime, timezone

# AWS clients
s3 = boto3.client(
    "s3",
    region_name="ap-south-1"
)

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="ap-south-1"
)

# S3 bucket
BUCKET_NAME = "daily-adventure-agent-mayur-2026"

# Bedrock inference profile
MODEL_ID = "apac.amazon.nova-micro-v1:0"


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

    try:
        # Invoke Amazon Nova Micro
        response = bedrock.converse(
            modelId=MODEL_ID,
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

        # Extract generated story
        story_text = response["output"]["message"]["content"][0]["text"]

        # Prepare JSON document
        story = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "content": story_text
        }

        # Save story to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key="daily-story.json",
            Body=json.dumps(story, ensure_ascii=False),
            ContentType="application/json"
        )

        print("Adventure story successfully generated and saved to S3.")

        return {
            "statusCode": 200,
            "body": json.dumps(story, ensure_ascii=False)
        }

    except Exception as e:

        print(f"Error: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
