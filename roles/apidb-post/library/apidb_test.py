from ansible.module_utils.basic import *
import os
import json
import requests
import subprocess

def getkeys(p):
    API_KEY =  p["apidbtoken"]    
    API_ENDPOINT = "https://" + p["apidbendpoint"] + ".apidb.io/api/ansiblerestrictedkeys"
    headers = {
    'Authorization': "Token " + API_KEY,
    'Content-Type': 'text/json',
    'Accept':'application/json'
    }
    r = requests.get(url = API_ENDPOINT, headers=headers)
    result = r.json()
    with open('apidb-post/library/keys_to_sanitise.json', 'wb') as file:
        file.write(result)




def sanitiseDict(d):
  
    sankeys = open("apidb-post/library/keys_to_sanitise.json", 'rb').read()
    keys = json.loads(sankeys)
    keys_to_sanitise = keys['keys_to_sanitise']

    #keys_to_sanitise = ['ansible_all_ipv4_addresses','ansible_machine','ansible_bios_version','ansible_domain','environment','ansible_all_ipv6_addresses','ansible_default_ipv4','ipv4','ipv6','all_ipv4_addresses','default_ipv4','all_ipv6_addresses','playbook_dir']
    for k in keys_to_sanitise:
        if k in d.keys():
            d.update({k: 'EXCLUDED'})
    for v in d.values():
        if isinstance(v, dict):
            sanitiseDict(v)
    return d


def postdata(p):
    statuscode = ''
    result = ''
    debugstatus = ''
    is_error = False
    has_changed = False
    meta = {"statuscode" : statuscode, "response" : result, "debug" : debugstatus}
    directory='/tmp/facts/'
    for filename in os.listdir(directory):
        API_KEY =  p["apidbtoken"]
        
        API_ENDPOINT = "https://" + p["apidbendpoint"] + ".apidb.io/api/ansiblefacts"
        headers = {
        'Authorization': "Token " + API_KEY,
        'Content-Type': 'text/json',
         'Accept':'application/json'
        }
        data = open(directory + filename, 'rb').read()
        
        #keys_to_sanitise = ['ansible_all_ipv4_addresses','kernel']
        getkeys(p)
        jdata = sanitiseDict(json.loads(data))
        r = requests.post(url = API_ENDPOINT, headers=headers, data=json.dumps(jdata))
        result = r.text
        statuscode = r.status_code
       # meta = {"statuscode" : statuscode, "response" : result, "keys_to_sanitise" : keys_to_sanitise}
        meta = {"statuscode" : statuscode, "keys_to_sanitise" : 'key', "endpoint": API_ENDPOINT}
       # os.system("rm -rf /tmp/facts/" + filename) # Need some logic here to check if it was successful before deleting (we could also not do a for loop and pass the hostname and filename
    return is_error, has_changed, meta
    


def main():
    
    fields = {
        "apidbtoken": {"default": "apikey", "type": "str"},
        "apidbendpoint": {"default": "app", "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)

    is_error, has_changed, result = postdata(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error", meta=result)


    

if __name__ == '__main__':
    main()
