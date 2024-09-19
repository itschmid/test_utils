#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import rpm

DOCUMENTATION = r'''
---
module: rpm_inventory
short_description: Listet alle installierten RPM-Pakete mit Name, Version und Release auf
version_added: "1.0"
description:
    - Dieses Modul listet alle auf dem System installierten RPM-Pakete auf.
    - Es gibt eine Liste mit den Namen, Versionen und Release-Nummern der Pakete zurück.
options: {}
author:
    - Manfred Schmid <manfred.schmid@it-schmid.com>
'''

EXAMPLES = r'''
# Liste aller installierten RPM-Pakete auf dem Zielsystem
- name: Alle installierten RPM-Pakete auflisten
  rpm_inventory:
'''

RETURN = r'''
packages:
    description: Eine Liste aller installierten RPM-Pakete mit Name, Version und Release
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "name": "bash",
            "version": "4.4.23",
            "release": "1.el7"
        },
        {
            "name": "glibc",
            "version": "2.17",
            "release": "260.el7"
        }
    ]
'''

def run_module():
    # Keine Eingabeparameter nötig, da wir nur Pakete abfragen
    module_args = dict()

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

    # Wenn im Check-Modus, führen wir keine Änderungen durch
    if module.check_mode:
        module.exit_json(**result)

    # Zugriff auf die RPM-Datenbank
    ts = rpm.TransactionSet()
    mi = ts.dbMatch()

    # Liste der Pakete mit Name, Version, Release
    packages = []
    for h in mi:
        package_info = {
            'name': h['name'],
            'version': h['version'],
            'release': h['release']
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
