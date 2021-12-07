import base64
import io
import json
from PIL import Image
from google.cloud import aiplatform

PROJECT_ID = ""
LOCATION = "us-central1"
ENDPOINT_ID = ""

client_options = {"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

endpoint = client.endpoint_path(
  project=PROJECT_ID, location=LOCATION, endpoint=ENDPOINT_ID
)

# Load image and make request body
with open('kiss.jpg', 'rb') as f:
  encoded_contents = base64.urlsafe_b64encode(f.read())
instances = [{"b64": encoded_contents.decode('UTF-8')}]

# Send request
response = client.predict(
  endpoint=endpoint, instances=instances
)

# Decode response
output_dict = dict(response.predictions[0])
decoded_bytes = base64.urlsafe_b64decode(output_dict['b64'])
img_bytes = io.BytesIO(decoded_bytes)
img = Image.open(img_bytes).convert('RGB')
img.save('kiss_anime.jpg')
