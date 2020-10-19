import random, os,json
import boto3
from . import filesystem

class AWSOps(object):

    fs = filesystem.FileSystemOps()
    def __init__(self):
        self.config = self.fs.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
        
    def autoscaling_group_set_desired_capacity(self, group_name, capacity):
        client = boto3.client('autoscaling', 
            aws_access_key_id=self.config["aws"]["access_key"], 
            aws_secret_access_key=self.config["aws"]["secret_key"],
            region_name=self.config["aws"]["default_region"])

        response = client.update_auto_scaling_group(
            AutoScalingGroupName=group_name,
            MinSize=capacity,
            MaxSize=capacity,
            DesiredCapacity=capacity
        )
    
    def upload_string_to_s3(self, string, bucket_name, file_name):
        client = boto3.client('s3', 
            aws_access_key_id=self.config["aws"]["access_key"], 
            aws_secret_access_key=self.config["aws"]["secret_key"],
            region_name=self.config["aws"]["default_region"])
        
        try:
            client.Object(bucket_name, file_name).put(Body=string)
        except ClientError as e:
            logging.error(e)
            return False
        return True
        