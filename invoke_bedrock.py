import boto3

# Initialize the Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Specify the model ID for Claude 4 Sonnet
model_id = "arn:aws:bedrock:us-east-1:805914070127:application-inference-profile/13gxeil0knhx"

# Define the conversation messages
messages = [
    {
        "role": "user",
        "content": [{"text": "Are you Claude Sonnet 4, the model released on May 14th, 2025? What’s your model ID?"}]
    }
]

# Define inference parameters
inference_config = {
    "maxTokens": 512,
    "temperature": 0.7,
    "topP": 0.9
}

# Send the request using the Converse operation
response = client.converse(
    modelId=model_id,
    messages=messages,
    inferenceConfig=inference_config
)

# Extract and print the response text
response_text = response["output"]["message"]["content"][0]["text"]
print(response_text)