
import os
import cv2
import json
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import boto3

os.environ['TORCH_HOME'] = '/tmp/'
mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) 
resnet = InceptionResnetV1(pretrained='vggface2').eval() 

def face_recognition_function(key_path):
    # Face extraction
    img = cv2.imread(key_path, cv2.IMREAD_COLOR)
    boxes, _ = mtcnn.detect(img)

    # Face recognition
    key = os.path.splitext(os.path.basename(key_path))[0].split(".")[0]
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    face, prob = mtcnn(img, return_prob=True, save_path=None)
    saved_data = torch.load('/tmp/data.pt') 
    if face != None:
        emb = resnet(face.unsqueeze(0)).detach()  
        embedding_list = saved_data[0]  
        name_list = saved_data[1]  
        dist_list = []  
        for idx, emb_db in enumerate(embedding_list):
            dist = torch.dist(emb, emb_db).item()
            dist_list.append(dist)
        idx_min = dist_list.index(min(dist_list))

        with open("/tmp/" + key + ".txt", 'w+') as f:
            f.write(name_list[idx_min])
        return "/tmp/" + key + ".txt"
    else:
        print(f"No face is detected")
    return

def lambda_handler(event, context):
    print("Received event:", event)
    bucket_name = event['bucket_name']
    image_file_name = event['image_file_name']

    key_path = f"/tmp/{image_file_name}"

    s3_client = boto3.client('s3')
    s3_client.download_file(bucket_name, image_file_name, key_path)

    # Download the embeddings file from S3 to /tmp directory
    embeddings_file_path = '/tmp/data.pt'
    s3_client.download_file('plibrary', 'data.pt', embeddings_file_path)

    recognized_name_file = face_recognition_function(key_path)

    print(recognized_name_file)

    if recognized_name_file is not None:
        # Upload result file to output bucket
        output_bucket = 'output'
        s3_client.upload_file(recognized_name_file, output_bucket, os.path.basename(recognized_name_file))
        return recognized_name_file
    else:
        return "No face detected"