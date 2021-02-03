Ansible Role: Aerospike
=========

[![Ansible Role](https://img.shields.io/ansible/role/52934.svg)](https://galaxy.ansible.com/kishorv06/aerospike/) [![Build Status](https://travis-ci.org/kishorv06/ansible-role-aerospike.svg?branch=master)](https://travis-ci.org/kishorv06/ansible-role-aerospike)

Ansible role to install and configure [Aerospike](http://www.aerospike.com/).

Requirements
------------

* Ansible 2.3+
* Debian 9+

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main.yml):

| Variable                    | Description                                  | Default                   |
|-----------------------------|----------------------------------------------|---------------------------|
| aerospike_boot_enabled      | Start Aerospike on boot                      | true                      |
| aerospike_version           | Version of Aerospike Server                  | 5.4.0.4                   |
| aerospike_source_directory  | Localtion to unarchive Aerospike directory   | /usr/local/src            |
| aerospike_log_location      | Aerospike log location                       | /var/log/aerospike        |
| aerospike_cluster_size      | Expected number of nodes in the cluster      | 1                         |

Optional variables
------------------

| Variable                       | Description                                                                                         | Default                              |
|--------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------|
| aerospike_proto_fd_max         | Maximum number of open file descriptors opened on behalf of client connections.                     | 15000                                |
| aerospike_proto_fd_idle_ms     | Time in milliseconds to wait before reaping connections.                                            | 60000                                |
| aerospike_access_address       | IP address that is announced to clients for connecting to the cluster.                              | "{{ ansible_default_ipv4.address }}" |
| aerospike_namespaces           | Aerospace namespace configuration                                                                   | [{name: default, memory_size: 2}]]   |
| aerospike_service_threads      | The number of threads receiving client requests on the network interface.                           | 2                                    |
| aerospike_mesh_seed_addresses  | List of mesh addresses of all nodes in the heartbeat cluster. Applies only when the node is mesh.   | ['127.0.0.1']                        |
| aerospike_multicast_group      | Controls the multicast group in a multicast cluster                                                 | 239.1.99.2                           |
| aerospike_multicast_port       | Multicast port.                                                                                     | 9918                                 |
| aerospike_heartbeat_interval   | Heartbeat Interval                                                                                  | 250                                  |
| aerospike_heartbeat_timeout    | Heartbeat Timeout                                                                                   | 10                                   |

Namespace Example Configuration
-------------------------------
```yaml
aerospike_namespaces:
  - name: default
    replication_factor: 2
    memory_size: 2
    high_water_memory_pct: 60
    high_water_disk_pct: 50
    storage_ttl: 4d
    nsup_period: 30m
    storage_engine:
      devices:
        - /dev/sda
        - /dev/sdb
      files:
        - /var/lib/aerospike/file1
        - /var/lib/aerospike/file2
      filesize: 2
      scheduler_mode: noop
      write_block_size: 128k
      data_in_memory: true
```

Role Dependencies
------------

None.

Example Playbook
----------------
```yaml
---
- hosts: all
  roles:
      - kishorv06.aerospike
```

License
-------

MIT

Author Information
------------------

Original Author: Matt Plachter

Current Maintainer: Kishor V
