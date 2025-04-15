import routeros_api
from mac_vendor_lookup import MacLookup

# the fucking IDE autocomplete
try:
    from netbox.extras.scripts import *
except ImportError:
    from ...netbox.netbox.extras.scripts import *



class Update(Script):
    host = StringVar(...)
    username = StringVar(...)
    passwd = StringVar(...)

    class Meta:
        ...

    def run(self, data, commit=True):
        host = data['host']
        username = data['username']
        passwd = data['passwd']
        connection = routeros_api.RouterOsApiPool(
            host,
            username=username,
            password=passwd,
            port=8729,
            plaintext_login=False,
            use_ssl=True,
            ssl_verify=True,
            ssl_verify_hostname=True,
            ssl_context=None,
        )
        api = connection.get_api()

        leases = api.get_resource('/ip/dhcp-server/lease').get()
        connection.disconnect()
        for row in leases:
            if 'active-mac-address' in row:
                mac = row['active-mac-address'].lower()
                ip = row['active-address']
                device_hostname = row.get('host-name','')
                try:
                    vendor = MacLookup().lookup(mac)
                except:
                    vendor = "Unknown"