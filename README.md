APIDB - visualise your facts
============================

This collection contains all the roles needed to run APIDB and will allow you to visualise your infrastructure on [the apiDB dashboard](https://app.apidb.io/).

<img src="https://raw.githubusercontent.com/apidb-io/apidb-collection/master/apidb_screenshot3.JPG">

 * Register a new account on [the apiDB dashboard](https://app.apidb.io/).
 * Check the profile page for your TOKEN.

The roles are maintained by APIDB

Includes:

 * apidb_localfacts
 * apidb_cis
 * apidb_collect
 * apidb_post

**Updates:**
 * Support for Windows servers has been added.
 * Support for Kubernetes has been added.
 * Onsite/On-Prem builds are now supported if you would like to run this in your Datacentre.

Usage
-----

Install the collection locally:
````
$ ansible-galaxy collection install apidb.apidb_collection -p ./collections
````

Requirements
------------

Only if your control node is Ubuntu, you may need to install ````python-requests```` to use this collection.
````
$ sudo apt-get install -y python-requests
````

Dependencies
------------

 * Ansible >= 2.7
 * Python >= 2.7

Example deployment file
-----------------------
Create your own ````deploy.yml```` file and add the contents below.

** Update the ````apidb_token: "your-Token"```` with your token from the profile page of your dashboard.**

    ----
    - name: create facts from linux and windows server
      hosts: collection
      collections:
        - apidb.apidb_collection
      tasks:
        - import_role:
            name: apidb_localfacts
          tags: facts
          when: '"facts" in ansible_run_tags'
    
        - import_role:
            name: apidb_cis
          tags: cis
          when: '"cis" in ansible_run_tags'
    
        - import_role:
            name: apidb_collect
          tags: collect
          when: '"collect" in ansible_run_tags'
      tags: run
    
    - name: Post to APIDB
      hosts: localhost
      connection: local
      gather_facts: false
      collections:
        - apidb.apidb_collection
      roles:
        - role: apidb_post
          tags: post

ansible.cfg
-----------
Consider adding these settings to your ansible.cfg file under ````[defaults]````

````
[defaults]
forks = 30                      # See Performance below for more details
inventory = inventory           # This should point to your inventory file
display_skipped_hosts = false   # This removes the "skipping messages from the ansible run"
````

Security
--------
We do not collect your secure data. We use "restricted keys" to stop certain fields being sent to APIDB. You have the control to add additional keys or remove the defaults.

<img src="https://raw.githubusercontent.com/apidb-io/apidb-collection/master/apidb_screenshot4.JPG"> 

First run
---------
Initial run to check everything is working and you have connectivity. The dashboard will display a breakdown of the number of each OS by version.

````
ansible-playbook  deploy.yml --tags=run,collect,post
````

Second run
----------
The second run will create some local facts (in /tmp). If your using AWS or Azure, the script will also collect some basic metadata to display. The sampleFacts.sh script can be updated or swapped out for your own scripts to create the facts you need on each server.

 * You'll need to customise the local_facts for your environments. We're happy to provide support to get you up and running.
 * If you require additional help to configure facts for your infrastructure, we provide consultancy to get you displaying the information you need.
 
````
ansible-playbook  deploy.yml --tags=run,facts,collect,post
````

Third run
---------
This run will check to see how your servers match up to the CIS controls for RHEL/OEL/CENTOS7 only. Other OS's will follow is there is demand. On the dashboard, you can see the CIS controls on each server page.

 * CIS facts currently only run on RHEL7 based servers (RHEL,Centos,OEL)

````
ansible-playbook  deploy.yml --tags=run,facts,cis,collect,post
````

Dashboard
---------
Check the APIDB dashboard for your new data.

Performance tuning
------------------
If you're running against lots of servers, you can utilise the ````ansible.cfg```` "forks" setting. The default is 5 forks but you can increase this (depending on the size of your control node). You will need to do some testing, but you should be able to double or triple the number of forks you run.

I.E.
````
[defaults]
forks = 20
````

Experimental Kubernetes role
---------------------------
This role is currently under development but is available for you to test.
Expectations/limitations:

 * This role will only run against Bastion host(s) - (A host that can connect to your kubernetes master).
 * Authentication: CUrrently only support the kubeconfig file (This will need to be updated manually).
 * Username/Password & TOKEN authentication is being delevoped.

To use the Kubernetes role, add the following to the deploy.yml file:

````
    - name: Sample kubernetes data collection
      hosts: localhost
      connection: local
      gather_facts: false
      collections:
        - apidb.apidb_collection
      tasks:
        - import_role:
            name: apidb_kubernetes
          tags: k8s
          when: '"k8s" in ansible_run_tags'
      tags: gather
````

You will need to update the ````hosts:```` to point to your bastion server.

Usage:
````
ansible-playbook  deploy.yml --tags=gather,k8s
````

License
-------
BSD

Author Information
------------------
This role has been create by the APIDB team. Further information and contact is available from [here](https://www.apidb.io/)

Disclaimer
----------
The ansible facts you send to APIDB will be stored in our DB. This will be remote from your company datacentre. Only send facts you are happy to send and make use of the "Resticted Keys" functionality. We also offer an onsite solution where we can setup APIDB within your own Datacentre, removing many security concerns.

Contact us for pricing and setup information.
