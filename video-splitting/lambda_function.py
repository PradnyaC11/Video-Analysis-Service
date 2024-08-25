import os
import subprocess
import math
import boto3
import json
import time

# Initialize S3 client
s3_client = boto3.client('s3', 
                  aws_access_key_id="AWS_ACCESS_KEY_ID",
                  aws_secret_access_key="AWS_SECRET_ACCESS_KEY",
                  region_name='us-east-1')

def video_splitting_cmdline(video_filename):
    filename = os.path.basename(video_filename)
    outdir = os.path.join("/tmp",os.path.splitext(filename)[0]) + ".jpg"

    split_cmd = '/opt/python/ffmpeg -ss 0 -r 1 -i ' +video_filename+ ' -vf fps=1/10 -start_number 0 -vframes 1 ' + outdir + ' -y'
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)

    return outdir

def lambda_handler(event, context):
    print("Received event:", event)
    s3_input_bucket = event['Records'][0]['s3']['bucket']['name']
    video_filename = event['Records'][0]['s3']['object']['key']
    print("video filename -" + video_filename)

    local_file_path = '/tmp/' + os.path.basename(video_filename)
    s3_client.download_file(s3_input_bucket, video_filename, local_file_path)

    output_directory = video_splitting_cmdline(local_file_path)
    print("Frames are stored in:", output_directory)

    key = os.path.basename(output_directory)
    s3_client.upload_file(output_directory, "stage-1", key)
    
    invoke_face_recognition(key)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete successfully')
    }
    
def invoke_face_recognition(filename):
    lambda_client = boto3.client('lambda')
    function_name = 'face-recognition'
    invocation_type = 'Event' 
    payload = {
        'bucket_name': 'stage-1',
        'image_file_name': filename
    }

    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(payload)
        )
        if response['StatusCode'] == 200:
            print("Face recognition function invoked successfully")
        else:
            print("Error invoking face recognition function:", response['FunctionError'])
    except Exception as e:
        print("Error invoking face recognition function:", str(e))
