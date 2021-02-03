import testinfra.utils.ansible_runner
import pytest
import os

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_verify_conf_file(host):
    c_file = host.file("/etc/aerospike/aerospike.conf")
    assert c_file.exists
    assert c_file.user == "root"
    assert c_file.group == "root"


def test_verify_log_file(host):
    l_file = host.file("/var/log/aerospike/aerospike.log")
    assert l_file.exists


def test_aerospike_service(host):
    c_service = host.service("aerospike")
    assert c_service.is_running
    assert c_service.is_enabled


def test_aerospike_cluster_size(host):
    hostname = host.run("hostname").stdout
    if "aerospike-node-" in hostname:
        # Mesh cluster
        cluster_info = host.run("asinfo --no-config-file -v statistics").stdout
        assert "cluster_size=3;" in cluster_info
    else:
        # Multicast cluster
        cluster_info = host.run("asinfo --no-config-file -v statistics").stdout
        assert "cluster_size=1;" in cluster_info


@pytest.mark.parametrize(
    "nodename,local_address",
    [
        # All Aerospike nodes
        ("aerospike-", "0.0.0.0:3000"),  # Service
        ("aerospike-", "0.0.0.0:3001"),  # Fabric
        ("aerospike-", "0.0.0.0:3003"),  # Info
        # Only Aerospike mesh cluster nodes
        ("aerospike-node-", "0.0.0.0:3002"),  # Mesh Heartbeat
    ],
)
def test_aerospike_listening_ports(host, nodename, local_address):
    listening_ports = host.run("netstat -ant").stdout
    if nodename in host.run("hostname").stdout:
        assert local_address in listening_ports


@pytest.mark.parametrize(
    "nodename,teststring",
    [
        # All nodes
        ("aerospike", "file /var/log/aerospike/aerospike.log"),
        ("aerospike", "service-threads 2"),
        ("aerospike", "proto-fd-max 15000"),
        ("aerospike", "proto-fd-idle-ms 60000"),
        ("aerospike", "high-water-memory-pct 60"),
        ("aerospike", "high-water-disk-pct 50"),
        ("aerospike", "nsup-period 30m"),
        ("aerospike", "replication-factor 2"),
        ("aerospike", "interval 250"),
        ("aerospike", "timeout 10"),
        ("aerospike", "paxos-single-replica-limit 1"),
        # Multicast nodes
        ("aerospike-multicast-node", "file /opt/aerospike/data/file1"),
        ("aerospike-multicast-node", "data-in-memory false"),
        ("aerospike-multicast-node", "scheduler-mode noop"),
        ("aerospike-multicast-node", "write-block-size 128K"),
        ("aerospike-multicast-node", "mode multicast"),
        ("aerospike-multicast-node", "port 9917"),
        ("aerospike-multicast-node", "filesize 2G"),
        ("aerospike-multicast-node", "default-ttl 30d"),
        ("aerospike-multicast-node", "multicast-group 239.1.99.2"),
        ("aerospike-multicast-node", "storage-engine device"),
        # Mesh nodes
        ("aerospike-node-", "mode mesh"),
        ("aerospike-node-", "port 3002"),
        ("aerospike-node-", "address any"),
        ("aerospike-node-", "mesh-seed-address-port "),
        ("aerospike-node-", "default-ttl 4d"),
        ("aerospike-node-", "storage-engine memory"),
    ],
)
def test_aerospike_config(host, teststring, nodename):
    c_file = host.file("/etc/aerospike/aerospike.conf")
    if nodename in host.run("hostname").stdout:
        assert c_file.contains(teststring)


def test_aerospike_access_port(host):
    ip_address = host.run("hostname -I").stdout
    c_file = host.file("/etc/aerospike/aerospike.conf")
    assert c_file.contains("access-address " + ip_address)
