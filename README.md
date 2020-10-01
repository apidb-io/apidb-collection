APIDB - visualise your facts
============================

This collection contains all the roles needed to run APIDB and will allow you to visualise your infrastructure on [the apiDB dashboard](https://app.apidb.io/).

<img src="https://raw.githubusercontent.com/apidb-io/apidb-collection/master/apidb_screenshot3.JPG">

 * Register a new account on [the apiDB dashboard](https://app.apidb.io/).
 * Check the profile page for your TOKEN.

The roles are maintained by APIDB

Includes:

 * apidb_localfacts
 * apidb_collect
 * apidb_post
 * apidb_kubernetes

**Updates:**

 * **Added ability for users to add their own custom extensions/playbooks**
 * **API is available. Check examples below**
 * **Support for Windows servers has been added.**
 * **Support for Kubernetes has been added.**
 * **Onsite/On-Prem builds are now supported if you would like to run this in your Datacentre.**

Usage
-----

Install the collection locally:
````
$ ansible-galaxy collection install apidb.apidb_collection -p ./collections
````

Requirements
------------

Only if your control node is Ubuntu or RHEL/Centos/OEL 8, you may need to install ````python-requests```` to use this collection.
````
$ sudo apt-get install -y python-requests
````
or
````
$ yum install -y python-requests
````

Dependencies
------------

 * Ansible >= 2.7
 * Python >= 2.7

Example deployment file
-----------------------
Create your own ````deploy.yml```` file and add the contents below.

    ---
    - name: create facts from linux and windows server
      hosts: all
      collections:
        - apidb.apidb_collection
      tasks:
        - import_role:
            name: apidb_localfacts
          tags: facts
    
        - import_role:
            name: apidb_collect
          tags: collect
    
    - name: Post to APIDB
      hosts: localhost
      connection: local
      gather_facts: false
      collections:
        - apidb.apidb_collection
      roles:
        - role: apidb_post
          tags: post


Set-up the group_vars
---------------------
Run the following command to add a group_vars/all file and add the TOKEN:

 * ````mkdir group_vars````
 * Now add the TOKEN ````vi group_vars/all````
 * Add the following to the file. Your TOKEN can be found on your "profile" page on [the APIDB dashboard](https://app.apidb.io/profile)
 
````
---
apidb_token: "your-token"
````
 * Now save the file.
 
ansible.cfg
-----------
Consider adding these settings to your ansible.cfg file under ````[defaults]````

 * Forks allows to run more concurrent runs than the default of 5.
 * Inventory should point to your inventory file
 * display_skipped_hosts won't show all the "skipped" ansible code.

````
[defaults]
forks = 20
inventory = inventory
display_skipped_hosts = false
````

Security
--------
We do not collect your secure data. We use "restricted keys" to stop certain fields being sent to APIDB. You have the control to add additional keys or remove the defaults.

<img src="https://raw.githubusercontent.com/apidb-io/apidb-collection/master/apidb_screenshot4.JPG"> 

Intital run
---------
Initial run to check everything is working and you have connectivity. Once run, your dashboard will display distrubution, kernel, operatingsystem and uptime values.

````
ansible-playbook  deploy.yml --tags=collect,post
````

Adding your own Custom Facts
----------------------------
We've setup a simple way for your to run you're own custom playbooks to collect facts important to you. Follow this process:

1) Use our prepared facts from our [custom_extensions](https://github.com/apidb-io/custom_extensions) repo in github.

 * Clone the repo into the same base DIR as our collection: ````git clone https://github.com/apidb-io/custom_extensions.git````
 * Edit the main.yml ````vi custom_extensions/main.yml```` 
 * Un-hash the playbooks you would like to run
````
    - custom_extensions/extensions/tidyup.yml # Cleans out old files
#    - custom_extensions/extensions/sample_facts.yml # My own loacl fact collection populates the dashboard.
#    - custom_extensions/extensions/cis.yml # Checks CIS controls against RHEL7
#    - custom_extensions/extensions/packages.yml # adds packages intot he dashboard.
#    - custom_extensions/extensions/sysctl.yml # Add sysctl settings into the dashboard.
````
 * Run the playbook as below:

````
ansible-playbook deploy.yml
````

2) You're free to add your own playbooks into same directory once you create it and they will be picked up when the apidb collection runs.

 * In the same base DIR of the collection, create the directory: ````mkdir custom_extensions````
 * Add your own playbooks templates, files etc into this DIR.
 * Run the playbook as below:

````
ansible-playbook deploy.yml
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

<img src="https://raw.githubusercontent.com/apidb-io/apidb-collection/master/kubernetes_cluster.JPG">


 * This role will only run against Bastion host(s) - (A host that can connect to your kubernetes master).
 * Authentication: Currently only support the kubeconfig file (This will need to be updated manually).
 * Username/Password & TOKEN authentication is being developed.

Manage your kubeconfig files in the ````group_vars/all```` file. Add the location of your kubeconfig file as below. If you have multiple clusters, you can add multiple kubeconfig files.

````
kubeconfig:
  - "$HOME/.kube/test-cluster.yml"
  - "$HOME/.kube/dev-cluster.yml"
````

To use the Kubernetes role, add the following to the deploy.yml file:

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


You will need to update the ````hosts:```` to point to your bastion server.

Usage:
````
ansible-playbook  deploy.yml --tags=gather,k8s,post
````

APIDB API
---------
You also have the option to use the APIDB API to pull out server and fact information directly from the database. Here are some examples:

 * Export your APIKEY first (Found on the profile page):

    ````export apikey=1234567891011121314151617````

 * Server list:

    ````curl --silent -X GET https://app.apidb.io/api/servers   -H "Authorization: Token $apikey"  -H "Accept:application/json" | jq````

 * List all production servers:

    ````curl --silent -X GET https://app.apidb.io/api/facts/environment/production   -H "Authorization: Token $apikey" -H "Accept:application/json" | jq````

 * List all production server but only show Servername & Environment:

    ````curl --silent -X GET https://app.apidb.io/api/facts/environment/production   -H "Authorization: Token $apikey" -H "Accept:application/json" | jq '[.servers[] | {name: .fqdn, Env: .factvalue}] | group_by(.fqdn, .factvalue)'````

 * Show all CentOS 6.9 servers:
 
    ````curl --silent -X GET https://app.apidb.io/api/facts/operatingsystem/"centos 6.9"   -H "Authorization: Token $apikey" -H "Accept:application/json" | jq '[.servers[] | {name: .fqdn, Env: .factvalue}] | group_by(.fqdn, .factvalue)'````

 * List all T2.small instance types:

    ````curl --silent -X GET https://app.apidb.io/api/facts/instance_type/t2.small   -H "Authorization: Token $apikey" -H "Accept:application/json" | jq '[.servers[] | {name: .fqdn, Env: .factvalue}] | group_by(.fqdn, .factvalue)'````


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
