
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
import pytest
import os
import testinfra.utils.ansible_runner

import pprint
pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def base_directory():
    cwd = os.getcwd()

    if('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


@pytest.fixture()
def get_vars(host):
    """

    """
    base_dir, molecule_dir = base_directory()
    distribution = host.system_info.distribution

    if distribution in ['debian', 'ubuntu']:
        os = "debian"
    elif distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        os = "redhat"
    elif distribution in ['arch']:
        os = "archlinux"

    print(" -> {} / {}".format(distribution, os))

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(base_dir)
    file_vars = "file={}/vars/main.yml name=role_vars".format(base_dir)
    file_molecule = "file={}/group_vars/all/vars.yml name=test_vars".format(molecule_dir)
    file_distibution = "file={}/vars/{}.yaml name=role_distibution".format(base_dir, os)

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    distibution_vars = host.ansible("include_vars", file_distibution).get("ansible_facts").get("role_distibution")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(distibution_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def test_installed_packages(host):
    """

    """
    package = "monitoring-plugins-common"

    # pp.pprint()

    distribution = host.system_info.distribution

    if distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        package = "nagios-plugins"
    if distribution == 'arch':
        package = "monitoring-plugins"

    p = host.package(package)
    assert p.is_installed
    assert p.version.startswith("2")


def test_blacklisted_packages(host, get_vars):
    """

    """
    blacklist = get_vars.get('monitoring_plugins_blacklist')

    if(blacklist and len(blacklist) != 0):
        p = host.package(blacklist[0])
        assert not p.is_installed


def test_generic_directory(host):

    distribution = host.system_info.distribution
    d = host.file("/usr/lib/monitoring-plugins")

    assert d.exists

    if(distribution == 'arch'):
        assert d.is_directory
    else:
        assert d.is_symlink
