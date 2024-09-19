#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import der benötigten Bibliotheken
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: win_inventory
short_description: Listet alle installierten Softwarepakete auf einem Windows-System auf
version_added: "1.0"
description:
    - Dieses Modul listet alle installierten Softwarepakete eines Windows-Systems auf, indem es die Windows-Registry abfragt.
    - Es verwendet ein PowerShell-Skript, um diese Daten zu sammeln.
options: {}
author:
    - Manfred Schmid (manfred.schmid@it-schmid.com)
'''

EXAMPLES = r'''
# Liste aller installierten Softwarepakete auf einem Windows-System
- name: Installierte Software auflisten
  win_inventory:
'''

RETURN = r'''
software:
    description: Liste der installierten Softwarepakete
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "name": "Google Chrome",
            "version": "85.0.4183.121",
            "publisher": "Google LLC",
            "install_date": "20200923",
            "install_location": "C:\\Program Files (x86)\\Google\\Chrome\\Application"
        },
        ...
    ]
'''

def main():
    module = AnsibleModule(argument_spec=dict())

    # Resultat: Da die Funktionalität in PowerShell implementiert ist, ist hier nichts zu tun.
    result = dict(
        changed=False
    )

    # Normalerweise übergibt Ansible den Prozess an das PowerShell-Skript
    module.exit_json(**result)


if __name__ == '__main__':
    main()
