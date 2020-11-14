import pytest
import os

import testinfra.utils.ansible_runner

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

# import pprint
# pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def get_vars(host):
    """

    """
    defaults_files = "file=../../defaults/main.yml name=role_defaults"
    vars_files     = "file=../../vars/main.yml name=role_vars"
    test_files     = "file=./group_vars/all/vars.yml name=test_vars"

    ansible_vars = host.ansible(
        "include_vars",
        defaults_files)["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        vars_files)["ansible_facts"]["role_vars"])

    ansible_vars.update(host.ansible(
        "include_vars",
        test_files)["ansible_facts"]["test_vars"])

    templar = Templar(loader = DataLoader(), variables = ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

#    pprint.pprint(result)
    return result


def test_installed_packages(host):
    """

    """
    package = "monitoring-plugins-common"

    if(host.system_info.distribution == "centos" or host.system_info.distribution == "redhat"):
        package = "nagios-plugins"

    p = host.package(package)
    assert p.is_installed
    assert p.version.startswith("2")


def test_blacklisted_packages(host, get_vars):
    """

    """
    blacklist = get_vars.get('monitoring_plugins_blacklist')

    if(len(blacklist) != 0):
        p = host.package(blacklist[0])
        assert not p.is_installed
