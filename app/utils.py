from google.cloud import secretmanager

def access_secret_version(project_id, secret_id, version_id="latest"):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')

# Replace 'your-project-id', 'your-secret-id', and 'latest' with your actual project ID, secret ID, and version ID.
openai_secret = access_secret_version('zobotautobot', 'OPENAI_API_KEY', 'latest')