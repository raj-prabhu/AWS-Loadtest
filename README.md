# AWS-Loadtest
>Load testing using Amazon AWS Services

##Description
The given [python script](https://github.com/raj-prabhu/AWS-Loadtest/blob/master/aws-loadtest.py) can be used to test how many concurrent users a server can handle. Load testing tools such as [ab] (https://httpd.apache.org/docs/2.4/programs/ab.html)
can also be used, but the drawback of these is that they can only be done from your local machine. 

In order to simulate multiple users across various regions of the world, AWS services come in 
handy. They enable us to launch [instances] (http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Instances.html) (remote machines)
in different regions of the world, run the required number of players on the new instances, return back the logs and finally terminate the
instances.

![alt tag](https://github.com/raj-prabhu/AWS-Loadtest/blob/master/aws_picture.JPG)

##Prerequisites	
- Python 2.7
- [Boto EC2] (http://boto.cloudhackers.com/en/latest/ref/ec2.html) - It can be installed by using the following command:
```
$ pip install boto
```
- [Amazon Web Services] (http://aws.amazon.com/) (AWS) account (One year free trial is available)
  * AWS Security Credentials
  * Key pair for each region
  * Amazon S3 bucket for storing the players (eg. HLS Player) as well as the logs to be collected

##Usage
- Run:
```
$ python aws-loadtest.py
```
- The program will first read the [csv file](https://github.com/raj-prabhu/AWS-Loadtest/blob/master/regions.csv) containing the details about the number of instances to be launched.  
- It will then start the required number of instances.
- Next, it will transfer the players from the S3 bucket to the instance and run them.
- The output of the players will then be copied to a text file. The text file (logs) for each of the instances will be sent back to S3 bucket.
- Once everything is completed, the instances will be terminated automatically.
