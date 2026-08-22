# TrailTales Architecture

TrailTales uses an event-driven serverless architecture.

## Architecture Flow

EventBridge Scheduler  
↓  
AWS Lambda — Daily Adventure Agent  
↓  
Amazon Bedrock — Nova Micro  
↓  
Amazon S3 — daily-story.json

## Components

### Amazon EventBridge Scheduler
Triggers the Lambda function automatically once every day.

### AWS Lambda
Runs the application logic and prepares the creative prompt.

### Amazon Bedrock
Provides access to Amazon Nova Micro for generating the adventure story.

### Amazon S3
Stores the generated story as daily-story.json.

### AWS IAM
Provides the required permissions between the AWS services.
