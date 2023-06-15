import boto3
import json

def get_secret(secret_name):
    secret_name = secret_name
    region_name = "eu-west-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

# Get credentials from AWS Secrets Manager
credentials = get_secret('summarise-gpt-prod')

# Log the keys of the credentials dictionary (not the values, for security)
print(f"Credentials keys: {list(credentials.keys())}")
