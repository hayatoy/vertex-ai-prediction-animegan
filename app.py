import os
import io
import json
import base64
import torch
from flask import Flask, request, Response
from PIL import Image

model2 = torch.hub.load(
  "bryandlee/animegan2-pytorch:main",
  "generator",
  pretrained=True,
  device="cpu",
  progress=False
)
face2paint = torch.hub.load(
  'bryandlee/animegan2-pytorch:main', 'face2paint', 
  size=512, device="cpu"
)

# Creation of the Flask app
app = Flask(__name__)

# Flask route for Liveness checks
@app.route("/healthcheck")
def healthcheck():
  status_code = Response(status=200)
  return status_code

# Flask route for predictions
@app.route('/predict',methods=['GET','POST'])
def predict():
  # Decode image
  request_json = request.get_json(silent=True, force=True)
  data = request_json['instances']
  decoded = base64.urlsafe_b64decode(data[0]["b64"])
  img_in_bytes = io.BytesIO(decoded)
  img = Image.open(img_in_bytes).convert('RGB')
  
  # Generate Anime image
  img_anime = face2paint(model=model2, img=img)

  # Encode image for response
  img_bytes = io.BytesIO()
  img_anime.save(img_bytes, format='JPEG')
  enc_out = base64.urlsafe_b64encode(img_bytes.getvalue())
  return json.dumps({"predictions": [{"b64": enc_out}]})

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=8080)  