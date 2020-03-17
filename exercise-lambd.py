import boto3
import pickle
import json, ast
import botocore

ACCESS_KEY = "XXXXXXXXXXXXXXXXXXXX"
SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# configure your ssm client here, such as AWS key or region
session = boto3.Session(
     region_name="us-west-2",
     aws_access_key_id=ACCESS_KEY,
     aws_secret_access_key=SECRET_KEY
 )

# Fetch the SSM config param details and copy it in to a file
ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name='UserName')
ssm_param_dict = {(parameter['Parameter']['Name']):(parameter['Parameter']['Value'])}
ssmfile = open('ssm_param_file', 'ab')
ssm_param_dict = ast.literal_eval(json.dumps(ssm_param_dict))
print (ssm_param_dict)
pickle.dump(ssm_param_dict, ssmfile)
ssmfile.close()

# Upload the SSM config param file to S3 bucket
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
uploaded = upload_to_aws('ssm_param_file', 'l3bucket', 'ssm_param_file')
