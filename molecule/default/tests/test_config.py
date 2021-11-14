import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_config(host):
    f = host.file("/etc/shorewall/shorewall.conf")

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o640
    assert f.contains("STARTUP_ENABLED=Yes")


def test_zones(host):
    f = host.file("/etc/shorewall/zones")

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o640
    assert f.contains("pub   ipv4")


def test_interfaces(host):
    f = host.file("/etc/shorewall/interfaces")

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o640
    assert f.contains("pub   enp0s3   nosmurfs,routefilter=2,tcpflags,dhcp")


def test_policy(host):
    f = host.file("/etc/shorewall/policy")

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o640
    assert f.contains("pub   all   DROP")
    assert f.contains("all   all   REJECT   info")


def test_rules(host):
    f = host.file("/etc/shorewall/rules")

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o640

    # default rule: wireguard mesh network
    assert f.contains("ACCEPT pub local udp,tcp 51819")
    # rule template: monitoring server prometheus
    assert f.contains("ACCEPT local mesh tcp 10999")
    # custom rule: vagrant ssh
    assert f.contains("ACCEPT pub local tcp 22,2200,2222")
