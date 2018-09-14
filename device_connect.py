from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectAuthError, ConnectError
from jnpr.junos.exception import ConfigLoadError, CommitError


def device_facts():
    dev = Device(host="172.16.198.1", user="root", mode="telnet", password="", port="90011")
    try:
        #import pdb; pdb.set_trace()
        dev.open()  
    except RuntimeError as exc:
        print("entered runtime exc")
        return (f"Returned RuntimeError: {exc}")
    except ConnectError as exc:
        print("entered ConnectError exception")
        return (f"Returned ConnectError: {exc}")
    except Exception as exc:
        print("entered generel exception")
        return (f"Returned Exception: {exc}")

    print("device opened1")
    print("device opened2")
    device_facts = dev.facts
    dev.close()
    return(device_facts)

def push_config():
    dev = Device(host="172.16.198.1", user="root", mode="telnet", password="", port="9001")
    try:
        result = dev.open()
        print(result)
    except Exception as exc:
        return (f"Returned Exception: {exc}")

    try:
        cu = Config(dev)
        cu.load("set system host-name the_hulk", format = "set", merge = True)
        #import pdb; pdb.set_trace()

        cu.commit()
        print("done commit")

    except ConfigLoadError as exc:
        print("entered ConfigLoadError exception")
        #import pdb; pdb.set_trace()
        return (f"Returned ConfigLoadError: ERROR")
    except Exception as exc:
        print("entered generel exception")
        return (f"Returned general Exception: {exc}")

