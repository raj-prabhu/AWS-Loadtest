#!/usr/bin/python

import boto.ec2
import csv

# list containing keys of all regions
keys = ['useast1key','uswest1key','uswest2key','euwest1key','eucentral1key','apnortheast1key','apnortheast2key','apsoutheast1key','apsoutheast2key','saeast1key']

# list containing AMIs of all regions
amis = ['ami-fce3c696','ami-06116566','ami-9abea4fb','ami-f95ef58a','ami-87564feb','ami-a21529cc','ami-09dc1267','ami-25c00c46','ami-6c14310f','ami-0fb83963']

# reading csv file containing number of instances in each region required       
f = open('regions.csv')
readCSV = csv.reader(f)

given_regions = []
number_of_instances = []

# storing information given in csv file in lists 
for row in readCSV:
	region = row[0]
	number = int(row[1])

	given_regions.append(region)
	number_of_instances.append(number)

i = 0
for region in given_regions:
	# choosing appropriate AMI and key for given region
	if region == 'us-east-1':
		ami = amis[0]
		my_key = keys[0]
	if region == 'us-west-1':
                ami = amis[1]
                my_key = keys[1]
	if region == 'us-west-2':
                ami = amis[2]
                my_key = keys[2]
	if region == 'eu-west-1':
                ami = amis[3]
                my_key = keys[3]
	if region == 'eu-central-1':
                ami = amis[4]
                my_key = keys[4]
	if region == 'ap-northeast-1':
                ami = amis[5]
                my_key = keys[5]
	if region == 'ap-northeast-2':
                ami = amis[6]
                my_key = keys[6]
	if region == 'ap-southeast-1':
                ami = amis[7]
                my_key = keys[7]
	if region == 'ap-southeast-2':
                ami = amis[8]
                my_key = keys[8]
	if region == 'sa-east-1':
                ami = amis[9]
                my_key = keys[9]
	
	for j in range(int(number_of_instances[i])):
		# connecting to the required region
		conn = boto.ec2.connect_to_region(region)
		# commands to be executed on the command line of an instance  
# Explanation of data_string:
# Lines 74-82: Installing awscli on the instance
# Lines 86-90: AWS Security Credentials 		
# Line 94: Transferring players from S3 bucket to the instance 
# Lines 96-98: Copying the output given out after running the players into a text file
# Line 100: Transferring the logs(text file) to the S3 bucket
# Lines 104-106: Terminating the instance
  
		data_string="""#!/bin/bash
sudo apt-get -y update

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"

sudo apt-get -y install python-pip

sudo pip install awscli

cd /home/ubuntu



export AWS_ACCESS_KEY_ID=<your AWS_ACCESS_KEY_ID here>

export AWS_SECRET_ACCESS_KEY=<your AWS_SECRET_ACCESS_KEY here> 

export AWS_DEFAULT_REGION="""+region+"""



aws s3 cp s3://yourS3bucketname/hello_world.py hello_world.py

chmod +x hello_world.py

./hello_world.py >> """+region+"""_"""+str(j+1)+"""_hello_world.txt

aws s3 cp /home/ubuntu/"""+region+"""_"""+str(j+1)+"""_hello_world.txt s3://yourS3bucketname



EC2_INSTANCE_ID="$(wget -q -O - http://instance-data/latest/meta-data/instance-id)"

aws ec2 terminate-instances --instance-ids $EC2_INSTANCE_ID


"""
		# spinning up the instances
		reservation = conn.run_instances(
			ami,
      	  		key_name= my_key,
      	  		instance_type='t2.micro',
			security_groups=['example_group'],
			user_data = data_string

		)
		
		instance = reservation.instances[0]
		# naming the instance
		instance.add_tag('Name','AWS-Loadtest')
		print "Spinning up instance (%s) " % (region)	
	i+=1                              
