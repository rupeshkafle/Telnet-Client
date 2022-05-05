class BdcomEpon:
    enterPrivelegedMode = b"enable\r\n"
    showInterface = b"show interface brief\r\n"
    showMacTable = b"show mac address-table\r\n"
    showActiveOnu = b"show epon active-onu\r\n"
    showInactiveOnu = b"show epon inactive-onu\r\n"
    showOnuInfo = b"show epon onu-information\r\n"
    showRejectedOnu = b"show epon rejected-onu\r\n"

    def runCommand(self, command):
        print(command)


olt = BdcomEpon()

olt.runCommand(operation)
