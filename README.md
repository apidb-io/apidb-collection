APIDB - visualise your facts
============================

This collection contains all the roles needed to run APIDB and will allow you to visualise your infrastructure on [the apiDB dashboard](https://api.apidb.io/).
The roles are maintained by Dennis McCarthy

It includes:

 * apidb_localfacts
 * apidb_cis
 * apidb_collect
 * apidb_post


Usage
-----

Install the collection locally:
````
$ ansible-galaxy collection install apidb.apidb_collection -p ./collections
````

Requirements
------------

If your control node is Ubuntu, you may need to install ````python-requests```` to use this collection.
````
$ sudo apt-get install -y python-requests
````

Dependencies
------------

 * Ansible >= 2.7
 * Python >= 2.7

Example Playbook
----------------

** Update the ````apidb_token: "your-Token"```` with your token from the profile page of your dashboard.**

An example of how to use this role:

    ---
    - hosts: all
      collections:
        - apidb.apidb_collection
      roles:
        - role: apidb_localfacts
          tags: local_facts

        - role: apidb_cis
          tags: cis

        - role: apidb_collect
          tags: collect
    
    - hosts: localhost
      connection: local
      gather_facts: false
      vars:
        apidb_token: "your-Token" # <-- Add your TOKEN HERE inside the ""
      collections:
        - apidb.apidb_collection
      roles:
        - role: apidb_post
          tags: post

First run
---------
Initial run to check everything is working and you have connectivity. The dashboard will display a breakdown of the number of each OS by version.

````
ansible-playbook  deploy.yml --tags=collect,post
````

Second run
----------
The second run will add create some local facts. If your using AWS or Azure, the script will collect some basic metadata to display. The customFactSetup.sh script can be updated or swapped out for your own scripts to create the facts you need on each server.

````
ansible-playbook  deploy.yml --tags=local_facts,collect,post
````

Third run
---------
This run will check to see how your servers match up to the CIS controls for RHEL/OEL/CENTOS7 only. Other OS's will follow is there is demand. On the dashboard, you can see the CIS controls on each server page.

````
ansible-playbook  deploy.yml --tags=local_facts,cis,collect,post
````

Dashboard
---------
Check the APIDB dashboard for your new data.


Performance tuning
------------------
If you're running against lots of servers, you can utilise the ansible.cfg "forks" setting. The default is 5 forks but you can increase this (depending on the size of your control node. You will need to do some testing, but you should be able to double or triple the number of forks you run.

  ansible.cfg

````
[defaults]
forks = 20
````

License
-------

BSD

Author Information
------------------
This role has been create by the APIDB team. Further information and contact is available from [here](https://www.apidb.io/)
