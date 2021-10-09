#!/usr/bin/env python
import argparse
import requests
import sys

url_base = "http://127.0.0.1:8080/ESCManager/internal/dynamic_mapping/"
EXCEPTION_CODE = 101
EXIT_400 = 40
EXIT_404 = 44
EXIT_409 = 49
EXIT_415 = 15  # currently JSON support not turned on for some of the APIs, this status code may be returned for those

desc = " DMAM - Dynamic Mapping Actions and Metrics Util to Create/Delete Metrics/Actions on ESC via REST"
usage_str = 'dmam.py [exec_type] [ "--name arg" | " --payload_xml path_to_xml ] " ' + '\n' + 'e.g' + '\n' + 'create-action --payload_xml /home/my_act.xml ' + '\n' + 'delete-metric --name cpu_load_5'

parser = argparse.ArgumentParser(description=desc, usage=usage_str)

# define arguments
parser.add_argument("exec_type", help="set exec type to determine what dynamic mapping event to do", type=str, choices=["create-action","create-metric","delete-metric","delete-action"])
group = parser.add_mutually_exclusive_group()
group.add_argument("--name", type=str, help= "The name of the metric/action to delete", metavar='Metric/Action Name', default=None)
group.add_argument("--payload_xml", type=str, help="The XML Payload to create the metric/action", metavar='PAYLOAD', default=None)
group.add_argument("--payload_json", type=str, help="The JSON Payload to create the metric/action", metavar='PAYLOAD', default=None)

creates = ["create-action","create-metric"]
deletes = ["delete-metric","delete-action"]



def do_post(exec_type, is_xml, path_to_payload):

    if exec_type == 'create-action':
        type_to_use = 'actions'
    elif exec_type == 'create-metric':
        type_to_use = 'metrics'
    else:
        print "Invalid exec_type for POST : " + str(exec_type)
        sys.exit(EXCEPTION_CODE)

    headers = {'Content-Type':'application/json', 'Accept':'application/json'}
    if is_xml:
        headers['Content-Type'] = 'application/xml'
        headers['Accept'] = 'application/xml'
    url = url_base + type_to_use

    data = None
    try:
        with open(path_to_payload, 'r') as f:
            data = f.read()
    except IOError:
        print "Failed to read payload to send"
        sys.exit(EXCEPTION_CODE)

    try:
        response = requests.post(url=url, headers=headers, data=data, timeout=60)

        if response.status_code != 200:
            print "POST request status code : " + str(response.status_code)
            exit_code = response.status_code
            if response.status_code == 400:
                exit_code = EXIT_400
            elif response.status_code == 409:
                exit_code = EXIT_409
            elif response.status_code == 415:
                exit_code = EXIT_415

            sys.exit(exit_code)

    except Exception as e:
        print e
        sys.exit(EXCEPTION_CODE)

    return

def do_delete(exec_type, name):
    if exec_type == 'delete-action':
        type_to_use = 'actions'
    elif exec_type == 'delete-metric':
        type_to_use = 'metrics'
    else:
        print "Invalid exec_type for DELETE : " + str(exec_type)
        sys.exit(EXCEPTION_CODE)

    if name is None :
        print ' Name not provided! '
        sys.exit(EXCEPTION_CODE)

    url_to_use = url_base + type_to_use + '/' + str(name)

    try:
        response = requests.delete(url=url_to_use, timeout=60)

        if response.status_code not in [200,204]:
            print "DELETE request status code : " + str(response.status_code)
            exit_code = response.status_code
            if response.status_code == 400:
                exit_code = EXIT_400
            elif response.status_code == 404:
                exit_code = EXIT_404

            sys.exit(exit_code)
    except Exception as e:
        print e
        sys.exit(EXCEPTION_CODE)

    return


args = parser.parse_args()

# LOGIC to determine what to do
if args.exec_type in creates:
    print 'Executing  ' + args.exec_type
    if args.payload_xml is not None:
        print ' Payload =>  ' + args.payload_xml
        do_post(args.exec_type, True, args.payload_xml)
    elif args.payload_json is not None:
        print ' Payload =>  ' + args.payload_json
        do_post(args.exec_type, False, args.payload_json)
        print 'OK'
    else:
        parser.print_usage()

elif args.exec_type in deletes:
    if args.name is not None:
        print 'Executing  ' + args.exec_type
        print ' Name =>  ' + args.name
        do_delete(args.exec_type, args.name)
        print 'OK'
    else:
        parser.print_usage()

else:
    parser.print_usage()

