# ovhcli
The file ovhcli.py is a cli to interact with the OVH API. It can manage credentials and applications.

The file dnsovh.py can setup and teardown TXT records. It is mainly intended for automating dns-01 ACME challenges.

## Configuration
Create a file ovh.conf

```toml
[default]
endpoint=ovh-eu

[ovh-eu]
; Generate the keys here https://eu.api.ovh.com/createApp/
application_key=<appkey>
application_secret=<appsecret>
;consumer_key=<conskey>
```

## Dependencies
ovh
tabulate
