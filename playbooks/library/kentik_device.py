#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: kentik_device

short_description: This is a module that will perform idempoent operations on kentik device management

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: The module will gather the current list of devices from Kentik and create the device if it is not in the list. 

options:
    device_name:
        description: The name of the device.
        required: true
        type: str
    device_description:
        description: The device description.
        required: false
        type: str
    device_subtype:
        description: The device subtype.
        choices: router, host-nprobe-dns-www, aws-subnet, azure_subnet, cisco_asa, gcp-subnet, istio_beta, open_nms, paloalto, silverpeak
        required: true
        type: str
        default: "router"
    cdn_attr:
        description: If this is a DNS server, you can contribute its queries to Kentik's CDN attribution database. 
        Valid values: "None" or "Y" or "N". ** cdn_attr is required when the device subtype's parent type is "host-nprobe-dns-www"
        required: false
        default: "none"
    device_sample_rate:
        description: The rate at which the device is sampling flows.
        required: true
        type: int
        default: 1
    plan_id:
        description: The ID of the plan to which this device is assigned.
        required: true
        type: int
    site_id:
        description: The ID of the site (if any) to which this device is assigned.
        required: false
        type: str
    sending_ips:
        description: IP addresses from which the device is sending flow.
        required: true
        type: list
    minimize_snmp:
        description: IP addresses from which the device is sending flow.
        required: false
        type: bool
        default: False
    device_snmp_ip:
        description: IP address from which the device is listening on snmp.
        required: false
        type: str
    device_snmp_community:
        description: The SNMP community to use when polling the device.
        required: false
        type: str
    device_snmp_v3_conf:
        username:
            description: The user name to use to authenticate via SNMP v3. 
            required: false
            type: str
        authentication_protocol:
            description: The auth protocol to use via SNMP v3.
            choices: "NoAuth" or "MD5" or "SHA"
            required: false
            type: str
        authentication_passphrase:
            description: AuthenticationPassphrase - the passphrase to use for SNMP v3.
            required: false
            type: str
        privacy_protocol:
            description: PrivacyProtocol - the privacy protocol to use to authenticate via SNMP v3.
            choices: "NoPriv" or "DES" or "AES"
            required: false
            type: str
        privacy_passphrase:
            description: PrivacyPassphrase - the passphrase to use for SNMP v3 privacy protocol.
            required: false
            type: str
    device_bgp_type:
        description: BGP (device_bgp_type) - Device bgp type. 
        Valid values: "none" (use generic IP/ASN mapping), "device" (peer with the device itself), "other_device" (share routing table of existing peered device).
        required: true
        type: str
        default: none
    device_bgp_neighbor_ip:
        description: Your IPv4 peering address.
        required: false
        type: str
    device_bgp_neighbor_ip6:
        description: Your IPv6 peering address.
        required: false
        type: str
    device_bgp_neighbor_asn:
        description: The valid AS number (ASN) of the autonomous system that this device belongs to.
        required: false
        type: str
    device_bgp_password:
        description: Optional BGP MD5 password.
        required: false
        type: str
    use_bgp_device_id:
        description: The ID of the device whose BGP table should be shared with this device.
        required: false
        type: int
    device_bgp_flowspec:
        description: Toggle BGP Flowspec Compatibility for device.
        required: false
        type: bool
    region:
        description: The reqion that your Kentik portal is located in. 
        required: false
        type: str
        default: US
        choices:
            - US
            - EU
    nms:
        description: A dictionary for adding NMS SNMP or streaming telemetry to a device.
        required: false
        type: dict
            agentId:
                description: ID of the agent that is monitoring this device.
                required: true
                type: string
            ipAddress:
                description: Local IP address of this device.
                required: true
                type: string
            snmp:
                description: SNMP Config for NMS
                required: false
                type: dict
                    credentialName:
                        description: Name of the SNMP credentials from the credential vault.
                        required: true
                        type: string
                    port:
                        description: SNMP port, to override default of 161.
                        required: false
                        type: int
                    timeout:
                        description: Timeout, to override default of 2s.
                        required: false
                        type: string
            st:
                description: Steaming telemetry config for NMS
                required: false
                type: dict
                    credentialName:
                        description: Name of the SNMP credentials from the credential vault.
                        required: true
                        type: string
                    port:
                        description: SNMP port, to override default of 161.
                        required: false
                        type: int
                    timeout:
                        description: Timeout, to override default of 2s.
                        required: false
                        type: string
                    secure:
                        description: Use SSL to connect to this device.
                        required: true
                        type: bool





# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Ethan Angele (@kentikethan)
"""

EXAMPLES = r"""
# Pass in a message
- name: Create a device
  kentik_device:
    name: edge_la1_001
    description: Edge router 1 in la data center
    sampleRate: 10
    type: router
    planId: 12345
    siteId: 12345
    flowSendingIp: 192.168.0.1
    snmpVersion: v2c
    snmpIp: 192.168.0.1
    snmpCommunity: myPreciousCommunity
    bgpType: device
    bgpNeighborIp: 192.168.0.1
    bgpNeighborAsn: 65001
    deviceBgpPassword: myPreciousPassword
    deviceBgpFlowspec: True
    region: EU


# fail the module
- name: Test failure of the module
  kentik_device:
    name: just_the_name_nothing_else_fail
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
"""

import json
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
import requests
from kentik_site import gather_sites, compare_site
from kentik_label import gather_labels


def build_labels(base_url, api_version, auth, module):
    """Function to build the list of labels to be added to a device"""
    api_version = "v202210"
    current_labels = gather_labels(base_url, api_version, auth, module)
    label_ids = []
    for label in module.params["labels"]:
        if label in current_labels:
            label_ids.append(current_labels[label])
        elif label == "":
            continue
        else:
            module.fail_json(msg=f"Label {label} does not exist.")
    return label_ids


def build_payload(base_url, auth, module):
    """Function to build the device object payload by removing unnecessary items."""
    payload = module.params
    del payload["email"]
    del payload["token"]
    del [payload["state"]]
    payload["title"] = module.params["siteName"]
    del [payload["siteName"]]
    # REMEMBER TO PASS THE CORRECT API VERSION FOR SITES HERE
    site_list = gather_sites(base_url, "/site/v202211", auth, module)
    site_id = compare_site(site_list, module)
    if site_id is False:
        module.fail_json(msg=f"Site {payload['title']} does not exist.")
    payload["siteId"] = int(site_id)
    plan_dict = gather_plans(auth, module)
    plan_id = compare_plan(plan_dict, module)
    payload["planId"] = int(plan_id)
    del [payload["planName"]]
    del [payload["labels"]]
    del [payload["title"]]
    del [payload["region"]]
    none_keys = []
    for key in payload:
        if payload[key] is None:
            none_keys.append(key)
    for key in none_keys:
        del [payload[key]]
    if "nms" in payload:
        if "port" in payload["nms"]["snmp"]:
            payload["nms"]["snmp"]["port"] = int(payload["nms"]["snmp"]["port"])
    return payload


def gather_plans(auth, module):
    """Function to gather a list of existing plans"""
    if module.params["region"] == "EU":
        url = "https://api.kentik.eu/api/v5/plans"
    else:
        url = "https://api.kentik.com/api/v5/plans"
    payload = {}
    headers = auth
    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=20
        )
        if response.status_code == 200:
            plan_data = response.json()
        else:
            module.fail_json(function="gatherPlans", msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    plan_dict = {}
    for plan in plan_data["plans"]:
        plan_dict[plan["name"]] = plan["id"]
    return plan_dict


def compare_plan(plan_dict, module):
    """Function to determine whether the plan exists"""
    plan = module.params["planName"]
    if plan in plan_dict:
        print("Plan exists")
    else:
        print("Plan does not exists")
        module.fail_json(msg=f"Plan {plan} does not exist.")
    return plan_dict[plan]


def gather_devices(base_url, api_version, auth, module):
    """Function to gather a list of devices for comparison"""
    url = f"{base_url}/device/{api_version}/device"
    payload = {}
    headers = auth

    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=20
        )
        device_data = response.json()
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    device_dict = {}
    for device in device_data["devices"]:
        device_dict[device["deviceName"]] = device["id"]

    return device_dict


def compare_device(device_list, module):
    """Function to determine whether a device already exists"""
    device = module.params["deviceName"]
    if device in device_list:
        print("Device exists")
        function_return = device_list[device]
    else:
        print(f"Device, {device} does not exists")
        function_return = False
    return function_return


def compare_labels(base_url, api_version, auth, module, device_id, labels):
    """Function to compare labels on a device to determine if it needs updated."""
    url = f"{base_url}/device/{api_version}/device/{device_id}"
    payload = {}
    headers = auth
    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=20
        )
        if response.status_code == 200:
            device_data = response.json()
            device_labels = []
            for device_label in device_data["device"]["labels"]:
                device_labels.append(device_label["id"])
            if labels == device_labels:
                function_return = False
            else:
                function_return = labels
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(function="compareLables", msg=to_text(exc))
    return function_return


def delete_device(base_url, api_version, auth, device_id, module):
    """Function to delete a device from Kentik"""
    print("Deleting Site...")
    url = f"{base_url}/device/{api_version}/device/{device_id}"
    payload = {}
    headers = auth
    try:
        response = requests.request(
            "DELETE", url, headers=headers, data=payload, timeout=20
        )
        if response.status_code == 200:
            print("Device deleted successfully")
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))


def create_device(base_url, api_version, auth, module, device_object):
    """Function to add a device to kentik"""
    print("Creating Device...")
    url = f"{base_url}/device/{api_version}/device"
    payload = json.dumps({"device": device_object})
    headers = auth
    try:
        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=20
        )
        if response.status_code == 200:
            device_data = response.json()
        else:
            module.fail_json(
                function="create_device",
                stats_code=response.status_code,
                msg=response.text,
            )
    except ConnectionError as exc:
        module.fail_json(function="create_device", msg=to_text(exc))

    return device_data["device"]["id"]


def update_device_labels(base_url, api_version, auth, module, device_id, labels):
    """Function to add or update device labels"""
    print("Updating Device Labels...")
    url = f"{base_url}/device/{api_version}/device/{device_id}/labels"
    headers = auth
    labels_list = []
    for label in labels:
        label_dict = {"id": int(label)}
        labels_list.append(label_dict)
    payload = json.dumps({"id": device_id, "labels": labels_list})
    try:
        response = requests.request(
            "PUT", url, headers=headers, data=payload, timeout=20
        )
        if response.status_code == 200:
            device_data = response.json()
        else:
            module.fail_json(function="update_device_labels", msg=response.text)
    except ConnectionError as exc:
        module.fail_json(function="update_device_labels", msg=to_text(exc))
    return device_data["device"]["id"]

def update_check(base_url, api_version, auth, module, device_id, device_object):
    """Function to check whether a device needs to be updated"""
    print("Checking device update...")
    url = f"{base_url}/device/{api_version}/device/{device_id}"
    headers = auth
    device_data = {}
    payload = {}
    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=20
        )
        if response.status_code == 200:
            device_data = response.json()
        else:
            module.fail_json(function="update_device_labels", msg=response.text)
    except ConnectionError as exc:
        module.fail_json(function="update_device_labels", msg=to_text(exc))

    if "nms" in device_object:
        print("NMS will be configured...")
        if "port" in device_object["nms"]["snmp"]:
            print("Port is configured in nms settings...")
            device_object["nms"]["snmp"]["port"] = int(device_object["nms"]["snmp"]["port"])
        elif "nms" in device_data["device"]:
            del [device_data["device"]["nms"]["snmp"]["port"]]
    return_bool = False
    if int(device_data["device"]["site"]["id"]) != int(device_object["siteId"]):
        print("Site does not match...updating...")
        return_bool = True
    elif int(device_data["device"]["plan"]["id"]) != int(device_object["planId"]):
        print("Plan IDs don't match...updating")
        return_bool = True
    else:
        del [device_object["siteId"]]
        del [device_object["planId"]]
        del [device_object["deviceSnmpCommunity"]]
        for key in device_object:
            if key not in device_data["device"]:
                print(f"Configured {key}: {device_object[key]} is not yet configured.")
                return_bool = True
            else:
                if str(device_data["device"][key]) != str(device_object[key]):
                    print(f"Configured {key}: {device_object[key]} does not match returned {key}: {device_data["device"][key]}")
                    return_bool = True
    if return_bool is False:
        print("Device is up to date...")
    return return_bool

def update_device(base_url, api_version, auth, module, device_id, device_object):
    """Function to update a device to kentik"""
    print("Updating Device...")
    url = f"{base_url}/device/{api_version}/device/{device_id}"
    device_object['id'] = device_id
    payload = json.dumps({"device": device_object})
    headers = auth
    try:
        response = requests.request(
            "PUT", url, headers=headers, data=payload, timeout=20
        )
        if response.status_code == 200:
            device_data = response.json()
        else:
            module.fail_json(
                function="update_device",
                stats_code=response.status_code,
                msg=response.text,
            )
    except ConnectionError as exc:
        module.fail_json(function="create_device", msg=to_text(exc))

    return device_data["device"]["id"]


def main():
    """The main function of the program"""
    base_url = "https://grpc.api.kentik.com"
    argument_spec = dict(
        deviceName=dict(type="str",required= True),
        deviceDescription=dict(type="str", required=False, default="Added by Ansible"),
        deviceSubtype=dict(
            type="str",
            required=False,
            default="router",
            choices=[
                "router",
                "host-nprobe-dns-www",
                "aws-subnet",
                "azure_subnet",
                "cisco_asa",
                "gcp-subnet",
                "istio_beta",
                "open_nms",
                "paloalto",
                "silverpeak",
            ],
        ),
        cdnAttr=dict(type="str", required=False, choices=["y", "n"]),
        deviceSampleRate=dict(type="int", required=False, default=1),
        planName=dict(type="str", required=True),
        siteName=dict(type="str", required=False),
        sendingIps=dict(type="list", required=True),
        minimizeSnmp=dict(type="bool", required=False, default=False),
        deviceSnmpIp=dict(type="str", required=False),
        deviceSnmpCommunity=dict(type="str", required=False),
        deviceSnmpV3Conf=dict(type="dict", required=False),
        deviceBgpType=dict(
            type="str",
            required=False,
            choices=["none", "device", "other_device"],
            default="none",
        ),
        deviceBgpNeighborIp=dict(type="str", required=False),
        deviceBgpNeighborIp6=dict(type="str", required=False),
        deviceBgpNeighborAsn=dict(type="str", required=False),
        deviceBgpPassword=dict(type="str", required=False, no_log=True),
        useBgpDeviceId=dict(type="int", required=False),
        deviceBgpFlowspec=dict(type="bool", required=False),
        nms=dict(type="dict", required=False),
        labels=dict(type="list", required=False),
        email=dict(type="str", required=False, default=os.environ["KENTIK_EMAIL"]),
        token=dict(
            type="str", no_log=True, required=False, default=os.environ["KENTIK_TOKEN"]
        ),
        region=dict(type="str", required=False, default=os.environ["KENTIK_REGION"]),
        state=dict(default="present", choices=["present", "absent"]),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    result = {"changed": False}
    state = module.params["state"]
    auth = {
        "X-CH-Auth-Email": module.params["email"],
        "X-CH-Auth-API-Token": module.params["token"],
        "Content-Type": "application/json",
    }
    if module.params["region"] == "EU":
        base_url = "https://grpc.api.kentik.eu"
    else:
        base_url = "https://grpc.api.kentik.com"
    api_version = "v202308beta1"
    if module.params["labels"]:
        print("Labels found")
        labels = build_labels(base_url, api_version, auth, module)
    else:
        print("No Labels found")
        labels = False
    device_object = build_payload(base_url, auth, module)
    result = {"changed": False}
    device_list = gather_devices(base_url, api_version, auth, module)
    device_id = compare_device(device_list, module)

    if device_id:
        labels = compare_labels(base_url, api_version, auth, module, device_id, labels)
        needs_updated = update_check(base_url, api_version, auth, module, device_id, device_object)
        if state == "present" and needs_updated:
            update_device(base_url, api_version, auth, module, device_id, device_object)
            result["changed"] = True
        elif state == "present":
            result["changed"] = False
        elif state == "absent":
            delete_device(base_url, api_version, auth, device_id, module)
            result["changed"] = True
    else:
        if state == "present":
            device_id = create_device(
                base_url, api_version, auth, module, device_object
            )
            result["changed"] = True
            result["device_id"] = device_id
        elif state == "absent":
            result["changed"] = False
    if labels and len(labels) > 0:
        update_device_labels(base_url, api_version, auth, module, device_id, labels)
        result["changed"] = True
    module.exit_json(**result)


if __name__ == "__main__":
    main()
