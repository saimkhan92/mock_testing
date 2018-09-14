from device_connect import device_facts, push_config
import pytest
from unittest import mock
import device_connect
from jnpr.junos.exception import ConnectAuthError, ConnectError
from jnpr.junos.exception import ConfigLoadError,CommitError

def test_get_dev_info(monkeypatch):
    fake_device_class = mock.MagicMock(spec=device_connect.Device)

    fake_device_object = fake_device_class.return_value
    fake_device_object.facts={"name":"saim"}
    
    monkeypatch.setattr(device_connect, 'Device', fake_device_class)

    return_value = device_facts()
    assert return_value == {'name': 'saim'}

@mock.patch("device_connect.Device", spec = True)
def test_using_decorator_get_dev_info(fake_device_class):
    #fake_device_class = mock.MagicMock(spec=device_connect.Device) # no need for this as this was automatically created by the @patch decorator
    #import pdb; pdb.set_trace()

    fake_device_class.return_value.facts={"name":"saim"}
    #monkeypatch.setattr(device_connect, 'Device', fake_device_class) # no need for monkeypatching if you are using @patch
    return_value = device_facts()
    assert return_value == {'name': 'saim'}

def test_get_dev_exception(monkeypatch):
    fake_device = mock.MagicMock(spec_set=device_connect.Device)
    fake_device.return_value.open.side_effect = ConnectError(fake_device, msg="fake_exception_message")

    monkeypatch.setattr(device_connect, 'Device', fake_device)

    return_value = device_facts()
    assert "ConnectError" in return_value

@mock.patch("device_connect.Device", spec=True)
def test_using_decorator_get_dev_exception(fake_device_class):
    fake_device_object = fake_device_class.return_value
    #fake_device_object.open.side_effect = mock.Mock(side_effect = device_connect.ConnectError(fake_device_object, msg="fake_exception_message")) #pass mocked exception
    fake_device_object.open.side_effect = device_connect.ConnectError(fake_device_object, msg="fake_exception_message")

    return_value = device_facts()
    assert "ConnectError" in return_value

@mock.patch("device_connect.Config", spec=True)
@mock.patch("device_connect.Device", spec=True)
def test_push_config(fake_device_class,fake_config_class):
    fake_device_object = fake_device_class.return_value
    fake_device_object.open.return_value = "device_open_object"

    fake_config_object = fake_config_class.return_value
    fake_config_object.commit.side_effect = device_connect.ConfigLoadError(fake_device_object,cmd=True, errs=True) # replace fake_decce here with something useful
    #fake_config_object.commit.side_effect = mock.Mock(side_effect = device_connect.ConfigLoadError(fake_device_object,cmd=True, errs=True))
    #monkeypatch.setattr(device_connect, 'Config', fake_config_object)
    #import pdb; pdb.set_trace()
    print("entering try")
    return_value = push_config()
    print (return_value)
    assert "ConfigLoadError" in return_value