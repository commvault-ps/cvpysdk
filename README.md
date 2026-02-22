# CVPySDK

[![Lint](https://github.com/commvault-ps/cvpysdk/actions/workflows/lint.yml/badge.svg)](https://github.com/commvault-ps/cvpysdk/actions/workflows/lint.yml)
[![Tests](https://github.com/commvault-ps/cvpysdk/actions/workflows/test.yml/badge.svg)](https://github.com/commvault-ps/cvpysdk/actions/workflows/test.yml)

CVPySDK is a Python Package for Commvault Software.

CVPySDK uses REST APIs to perform CommCell operations.

## Requirements

- Python 3.9 and above
- [requests](https://pypi.python.org/pypi/requests/) Python package
- [xmltodict](https://pypi.python.org/pypi/xmltodict) Python package
- Commvault Software v11 SP7 or later release with WebConsole installed

## Installing CVPySDK

CVPySDK can be installed directly from PyPI using uv:

```python
uv pip install cvpysdk
```

CVPySDK is available on GitHub [here](https://github.com/Commvault/cvpysdk)

It can also be installed from source.

After downloading, from within the `cvpysdk` directory, execute:

```python
uv pip install .
```

## Using CVPySDK

Login to Commcell:

```python
from cvpysdk.commcell import Commcell
commcell = Commcell(webconsole_hostname, commcell_username, commcell_password)
```

Print all clients:

```python
print(commcell.clients)
```

Get a client:

```python
client = commcell.clients.get(client_name)
```

Get an agent:

```python
agent = client.agents.get(agent_name)
```

Get an instance:

```python
instance = agent.instances.get(instance_name)
```

Browsing content at instance level:

```python
paths, dictionary = instance.browse(path='c:\\', show_deleted=True)
```

Browsing content of a instance in a specific time range:

```python
paths, dictionary = instance.browse(path='f:\\', from_time='2010-04-19 02:30:00', to_time='2014-12-20 12:00:00')
```

Searching a file in instance backup content:

```python
paths, dictionary = instance.find(file_name="*.csv")
```

Get a backupset:

```python
backupset = instance.backupsets.get(backupset_name)
```

Run backup for a backupset:

```python
job = backupset.backup()
```

Browsing content at backupset level:

```python
paths, dictionary = backupset.browse(path='c:\\', show_deleted=True)
```

Browsing content of a backupset in a specific time range:

```python
paths, dictionary = backupset.browse(path='f:\\', from_time='2010-04-19 02:30:00', to_time='2014-12-20 12:00:00')
```

Searching a file in backupset backup content:

```python
paths, dictionary = backupset.find(file_name="*.csv")
```

Get a subclient:

```python
subclient = backupset.subclients.get(subclient_name)
```

Run backup for a subclient:

```python
job = subclient.backup(backup_level, incremental_backup, incremental_level)
```

Browsing content at subclient level:

```python
paths, dictionary = subclient.browse(path='c:\\', show_deleted=True)
```

Browsing content of a subclient in a specific time range:

```python
paths, dictionary = subclient.browse(path='f:\\', from_time='2010-04-19 02:30:00', to_time='2014-12-20 12:00:00')
```

Searching a file in subclient backup content:

```python
paths, dictionary = subclient.find(file_name="*.txt")
```

Run restore in place job for a subclient:

```python
job = subclient.restore_in_place(paths, overwrite, restore_data_and_acl)
```

Run restore out of place job for a subclient:

```python
job = subclient.restore_out_of_place(client, destination_path, paths, overwrite, restore_data_and_acl)
```

Job Operations:

```python
job.pause()         # Suspends the Job
job.resume()        # Resumes the Job
job.kill()          # Kills the Job
job.status          # Current Status the Job  --  Completed / Pending / Failed / .... / etc.
job.is_finished     # Job finished or not     --  True / False
job.delay_reason    # Job delay reason (if any)
job.pending_reason  # Job pending reason (if any)
```

## Uninstalling

On Windows, if CVPySDK was installed using an `.exe` or `.msi`
installer, simply use the uninstall feature of "**Add/Remove Programs**" in the
Control Panel.

Alternatively, you can uninstall using **uv**:

```python
uv pip uninstall cvpysdk
```

## Subclient Support

Subclient operations are currently supported for the following Agents:

1. File System
2. Virtual Server
3. Cloud Apps
4. SQL Server
5. NAS / NDMP
6. SAP HANA
7. ORACLE
8. Sybase
9. SAP ORACLE
10. Exchange Database
11. Exchange Mailbox
12. Informix
13. Notes Database
14. MySQL
15. PostgreS
16. Big Data Apps

## Documentation

To get started, please see the [full documentation for this library](https://commvault.github.io/cvpysdk/)

## Contribution Guidelines

1. We welcome all the enhancements from everyone although we request the developer to follow some guidelines while interacting with the `CVPySDK` codebase.
2. Before adding any enhancements/bug-fixes, we request you to open an Issue first.
3. The SDK team will go over the Issue and notify if it is required or already been worked on.
4. If the Issue is approved, the contributor can then make the changes to their fork and open a pull request.

### Pull Requests

- CVPySDK has 2 active branches, namely:
    - **master**
    - **dev**
- The contributor should *Fork* the **dev** branch, and make their changes on top of it, and open a *Pull Request*
- The **master** branch will then be updated with the **dev** branch, once everything is verified

**Note:** The SDK team will not accept any *Pull Requests* on the **master** branch

### Coding Considerations

- All python code should be **PEP8** compliant.
- All changes should be consistent with the design of the SDK.
- The code should be formatted using **autopep8** with line-length set to **99** instead of default **79**.
- All changes and any new methods/classes should be properly documented.
- The doc strings should be of the same format as existing docs.

### Code of Conduct

Everyone interacting in the **CVPySDK** project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the
[PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

## License

**CVPySDK** and its contents are licensed under [Commvault License](https://raw.githubusercontent.com/Commvault/cvpysdk/master/LICENSE.txt)

## About Commvault

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Commvault_logo.svg/320px-Commvault_logo.svg.png" alt="Commvault">
</p>

[Commvault](https://www.commvault.com/)
(NASDAQ: CVLT) is a publicly traded data protection and information management software company headquartered in Tinton Falls, New Jersey.

It was formed in 1988 as a development group in Bell Labs, and later became a business unit of AT&T Network Systems. It was incorporated in 1996.

Commvault software assists organizations with data backup and recovery, cloud and infrastructure management, and retention and compliance.
