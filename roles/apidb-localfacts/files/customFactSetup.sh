#!/bin/bash

# This file uses commands to populate local facts
# in /etc/ansible/facts.d/local.fact.
#
# Edit this file to add your own facts relevant
# to your environment.
# I've added a few examples below to help get you started.
#cat /dev/null > /etc/ansible/facts.d/local.fact

AWS=`curl -s http://169.254.169.254/latest/dynamic/instance-identity/ | grep signature >/dev/null; echo $?`
AZURE=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance |grep api-version >/dev/null; echo $?`
fact_location=/tmp/local/local.fact

(
if [ $AWS == 0 ]
then
  EC2_INSTANCE_TYPE=`curl -s http://169.254.169.254/latest/meta-data/instance-type`
  EC2_AVAIL_ZONE=`curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone`
  EC2_REGION="`echo \"$EC2_AVAIL_ZONE\" | sed 's/[a-z]$//'`"
  AMI_ID=`curl -s http://169.254.169.254/latest/meta-data/ami-id`

  echo "cloud: AWS"
  echo "INSTANCE_TYPE: "$EC2_INSTANCE_TYPE
  echo "AVAIL_ZONE: "$EC2_AVAIL_ZONE
  echo "REGION: "$EC2_REGION
  echo "AMI_ID: "$AMI_ID
  echo "environment: Dev"
  echo "Support_Team: web"
  echo "Callout: 8-6"

elif [ $AZURE == 0 ]
then
  AZURE_API=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance | awk -F\" '{print $8}'`
  AZURE_INSTANCE_TYPE=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance?api-version=$AZURE_API |sed -e 's/[}"]*\(.\)[{"]*/\1/g;y/,/\n/'| grep vmSize | awk -F: '{print $2}'`
  AZURE_REGION=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance?api-version=2019-11-01 | sed -e 's/[}"]*\(.\)[{"]*/\1/g;y/,/\n/' | grep location | awk -F: '{print $2}'`
  AZURE_RESOURCE_GROUP_NAME=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance?api-version=2019-11-01 | sed -e 's/[}"]*\(.\)[{"]*/\1/g;y/,/\n/' | grep resourceGroupName | awk -F: '{print $2}'`

  echo "cloud: AZURE"
  echo "INSTANCE_SIZE: "$AZURE_INSTANCE_TYPE
  echo "REGION: "$AZURE_REGION
  echo "RESOURCE_GROUP_NAME: "$AZURE_RESOURCE_GROUP_NAME
  echo "environment: production"
  echo "Support_Team: database"
  echo "Callout: 24-7"

else
  echo "cloud: no_cloud"
  echo "environment: Dev"
  echo "Support_Team: operations"
  echo "Callout: none"
fi
) >> $fact_location


#########################
# Add in case statements to select specific regions
# Examples below.
#########################
#case $EC2_AVAIL_ZONE in
#        eu-west-1a)
#         echo "environment: Production" >> /etc/ansible/facts.d/local.fact
#         echo "Support_Team: Hadoop" >> /etc/ansible/facts.d/local.fact echo "Callout: 24-7" >> /etc/ansible/facts.d/local.fact
#        ;;
#        eu-west-1b)
#         echo "environment: Dev" >> /etc/ansible/facts.d/local.fact
#         echo "Support_Team: web" >> /etc/ansible/facts.d/local.fact
#         echo "Callout: 8-6" >> /etc/ansible/facts.d/local.fact
#        ;;
#esac

#case $AZURE_REGION in
#        uksouth)
#         echo "environment: production" >> /etc/ansible/facts.d/local.fact
#         echo "Support_Team: database" >> /etc/ansible/facts.d/local.fact echo "Callout: 24-7" >> /etc/ansible/facts.d/local.fact
#         echo "Callout: 24-7" >> /etc/ansible/facts.d/local.fact
#        ;;
#        ukwest)
#         echo "environment: Dev" >> /etc/ansible/facts.d/local.fact
#         echo "Support_Team: web" >> /etc/ansible/facts.d/local.fact
#         echo "Callout: 8-6" >> /etc/ansible/facts.d/local.fact
#        ;;
#esac
