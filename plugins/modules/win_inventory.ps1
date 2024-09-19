#!powershell

# Copyright: (c) 2024, Manfred Schmid (manfred.schmid@it-schmid.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic

$spec = @{
    options = @{}
    supports_check_mode = $true
}

# Initialisierung des Ansible-Moduls
$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

# Sammele die Liste der installierten Software aus der Windows-Registry (64-Bit und 32-Bit)
Try {
    $SoftwList1 = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
        Where-Object { $_.DisplayName -ne $null } |
        Select-Object DisplayName, DisplayVersion, Publisher, InstallDate, InstallLocation

    $SoftwList2 = Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* |
        Where-Object { $_.DisplayName -ne $null } |
        Select-Object DisplayName, DisplayVersion, Publisher, InstallDate, InstallLocation

    $SoftwList = $SoftwList1 + $SoftwList2

    # Rückgabe der Daten an Ansible im JSON-Format
    $module.Result.software = $SoftwList

    # Ändere das "changed" Flag nicht, da keine Änderungen an der Maschine vorgenommen wurden
    $module.Result.changed = $false
}
Catch {
    # Bei Fehlern wird ein JSON-Fehler an Ansible zurückgegeben
    $module.FailJson("Fehler beim Abfragen der installierten Software: $($_.Exception.Message)", $_)
}

# Das Modul erfolgreich beenden und die Ergebnisse zurückgeben
$module.ExitJson()