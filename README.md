# Ansible Collection - apidb.apidb

APIDB - visualise your facts
=========

APIDB will allow you to visualise your infrastructure on [the apiDB dashboard](http://www.apidb.io/)

Requirements
------------

Ubuntu versions may require ````python-requests```` is installed on the server running apiDB.
````
$ sudo apt-get install -y python-requests
````

Installation
------------

Using ansible-galaxy:
````
$ ansible-galaxy install apidb.apidb
````

Using ansible-galaxy to install to the current directory:
````
$ ansible-galaxy install --roles-path . apidb.apidb
````

Using requirements.yml:
```
- src: apidb.apidb
````

Using git:
````
$ git clone https://github.com/apidb-io/apidb.git
````

Role Variables
--------------

To authenticate with apidb.io you will need a TOKEN. To get yours, sign-up [here](http://www.apidb.io). Create an account and visit the ````profile```` page.
Once you have your unique TOKEN, update this variables under ````group_vars/all.yml````

````
---
# vars file for apidb-apidb

apidb_token: "your-token-here"
````

Dependencies
------------

 * Ansible >= 2.7
 * Python >= 2.7

Example Playbook
----------------

An example of how to use this role:

    ---
    - hosts: all
      gather_facts: true
          roles:
        - role: apidb-localfacts
         ` tags: local_facts
    
        - role: apidb-cis
          tags: cis
    
    #    - role: apidb-win
    #      tags: win
    #      when: ansible_distribution == "Microsoft Windows Server 2012 R2 Standard"
    
        - role: apidb-collect
          tags: collect

    - hosts: localhost
      connection: local
      gather_facts: false
      roles:
        - role: apidb-post
          tags: post

First run
---------
````
ansible-playbook  deploy.yml --tags=collect,post
````

second run
----------
````
ansible-playbook  deploy.yml --tags=local_facts,collect,post
````

third run
---------
````
ansible-playbook  deploy.yml --tags=local_facts,cis,collect,post
````

License
-------

BSD

Author Information
------------------

This role has been create by the APIDB team. Further information and contact is available from [here](http://www.apidb.io/)
