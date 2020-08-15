#!/bin/bash

# This file uses commands to populate local facts
# in /tmp/local/local.fact.
#
# Edit this file to add your own facts relevant
# to your environment or just it as an example for your own.
# I've added a few examples below to help get you started.

SYSPATH=`which systemctl`
CLOUD=`if [ -f /sys/hypervisor/uuid ] && [ \`head -c 3 /sys/hypervisor/uuid\` == ec2 ] || $SYSPATH is-active --quiet waagent; then echo cloud; else echo noncloud; fi`
#CPU=$(top -b -n1 | grep "Cpu(s)" | awk '{print $2 + $4}') # for demo purposes
fact_location=/tmp/local/local.fact

(
if [ $CLOUD == "cloud" ]
then
  AWS=`curl -s http://169.254.169.254/latest/dynamic/instance-identity/ | grep signature >/dev/null; echo $?`
  AZURE=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance |grep api-version >/dev/null; echo $?`

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
    #echo "SNAPSHOT_CPU_%: "$CPU
    #if [ -f /etc/redhat-release ]; then echo "OpenSSH_version: $(rpm -qa | grep openssh-clients)"; fi

    case $EC2_INSTANCE_TYPE in
          t2.micro)
           echo "environment: Production"
           echo "Support_Team: Hadoop"
           echo "Callout: 24-7"
          ;;
          t2.medium)
           echo "environment: Dev"
           echo "Support_Team: web"
           echo "Callout: 8-6"
          ;;
          t2.small)
           echo "environment: UAT"
           echo "Support_Team: Database"
           echo "Callout: 7-7"
          ;;
    esac


  elif [ $AZURE == 0 ]
  then
    AZURE_API=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance | awk -F\" '{print $8}'`
    AZURE_INSTANCE_TYPE=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance?api-version=$AZURE_API |sed -e 's/[}"]*\(.\)[{"]*/\1/g;y/,/\n/'| grep vmSize | awk -F: '{print $2}'`
    AZURE_REGION=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance?api-version=2019-11-01 | sed -e 's/[}"]*\(.\)[{"]*/\1/g;y/,/\n/' | grep location | awk -F: '{print $2}'`
    AZURE_RESOURCE_GROUP_NAME=`curl -s -H Metadata:true http://169.254.169.254/metadata/instance?api-version=2019-11-01 | sed -e 's/[}"]*\(.\)[{"]*/\1/g;y/,/\n/' | grep resourceGroupName | awk -F: '{print $2}'`

    echo "cloud: AZURE"
    echo "INSTANCE_TYPE: "$AZURE_INSTANCE_TYPE
    echo "REGION: "$AZURE_REGION
    echo "RESOURCE_GROUP_NAME: "$AZURE_RESOURCE_GROUP_NAME
    echo "environment: production"
    echo "Support_Team: database"
    echo "Callout: 24-7"
    #echo "SNAPSHOT_CPU_%: "$CPU

  else
    echo "cloud: no_cloud"
    echo "environment: Dev"
    echo "Support_Team: operations"
    echo "Callout: none"
    #echo "SNAPSHOT_CPU_%: "$CPU

  fi
fi
) >> $fact_location
