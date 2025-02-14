import json
import boto3
import base64


# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2025-02-13-21-13-42-208'
runtime = boto3.client(service_name='sagemaker-runtime')

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    # Instantiate a Predictor, For this model the IdentitySerializer needs to be "image/png"
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType='image/png',
        Body=image
    )
    # Make a prediction:
    inferences = json.loads(response['Body'].read().decode('utf-8'))
    event["inferences"] = [float(x) for x in inferences]

    # We return the data back to the Step Function
    return {
        'statusCode': 200,
        'body': {
            "image_data": event['body']['image_data'],
            "s3_bucket": event['body']['s3_bucket'],
            "s3_key": event['body']['s3_key'],
            "inferences": inferences
        }
    }
