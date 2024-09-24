#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess
import xml.etree.ElementTree as ET

DOCUMENTATION = '''
---
module: zypper_update_status
short_description: Gathers information about available updates from Zypper
description:
  - This module collects facts about available updates from Zypper, including all updates, only patches, or security patches.
options:
  update_type:
    description:
      - Specifies the type of updates to check.
      - 'all': Lists all available updates.
      - 'patches': Lists only available patches.
      - 'security': Lists only available security patches.
    choices: ['all', 'patches', 'security']
    default: 'all'
author:
  - Your Name
'''

EXAMPLES = '''
- name: Gather all update information
  zypper_update_status:
    update_type: all

- name: Gather only patch information
  zypper_update_status:
    update_type: patches

- name: Gather only security patch information
  zypper_update_status:
    update_type: security
'''

RETURN = '''
packages:
    description: List of available updates or patches
    returned: always
    type: list
    elements: dict
    contains:
        name:
            description: Name of the package.
            type: str
            sample: "libmfx1"
        version:
            description: The new version of the package.
            type: str
            sample: "22.6.1-150500.3.5.1"
        version_old:
            description: The old version of the package.
            type: str
            sample: "22.6.1-150500.3.2.4"
        arch:
            description: The architecture of the package.
            type: str
            sample: "x86_64"
        source_url:
            description: The source URL for the package.
            type: str
            sample: "http://repo.devel.test.lan/os/sles15-updates/SUSE/Updates/SLE-Module-Packagehub-Subpackages/15-SP5/x86_64/update/"
        description:
            description: Description of the package.
            type: str
            sample: "The Intel Media SDK provides a plain C API..."
'''


def run_module():
    # Eingabeparameter: update_type für die Art der Abfrage
    module_args = dict(
        update_type=dict(type='str', choices=['all', 'patches', 'security'], default='all')
    )

    # Initialisierung des Result-Dictionarys
    result = dict(
        changed=False,
        packages=[]
    )

    # AnsibleModule erstellt das Interface zum Kommunizieren mit Ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Den Wert des übergebenen Parameters abfragen
    update_type = module.params['update_type']

    # Wähle den entsprechenden zypper-Befehl basierend auf update_type
    if update_type == 'all':
        zypper_command = ['zypper', '--xmlout', 'list-updates']
    elif update_type == 'patches':
        zypper_command = ['zypper', '--xmlout', 'list-patches']
    elif update_type == 'security':
        zypper_command = ['zypper', '--xmlout', 'list-patches', '--category', 'security']

    # Führe den zypper-Befehl aus und fange die XML-Ausgabe ab
    zypper_result = subprocess.run(zypper_command, capture_output=True, text=True)

    if zypper_result.returncode != 0:
        module.fail_json(msg="Failed to run zypper", stderr=zypper_result.stderr)

    # Parse die XML-Ausgabe
    root = ET.fromstring(zypper_result.stdout)

    # Liste der Pakete mit Name, Version, Release, Architektur und Quelle
    packages = []
    for update in root.findall('.//update'):
        package_info = {
            'name': update.get('name'),
            'version': update.get('edition'),
            'version_old': update.get('edition-old'),
            'arch': update.get('arch'),
            'source_url': update.find('source').get('url'),
            'description': update.find('description').text
        }
        packages.append(package_info)

    # Die Pakete zum Ergebnis hinzufügen
    result['packages'] = packages

    # Modul normal beenden und die Ergebnisse zurückgeben
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
