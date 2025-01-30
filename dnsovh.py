import ovh
import sys
import argparse

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("action", help="The action to execute, either setup or teardown.", type=str)
parser.add_argument("domain", help="The domain for which to setup the record.", type=str)
parser.add_argument("challenge", help="The value of the record.", type=str)
args = parser.parse_args()

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# to get your credentials
client = ovh.Client()

## Request RO, /me API access
#ck = client.new_consumer_key_request()
#ck.add_rules(["GET", "POST"], "/domain/zone/*/record")
#ck.add_rule("DELETE", "/domain/zone/*/record/*")

# Request token
#validation = ck.request()

#print("Please visit %s to authenticate" % validation['validationUrl'])
#input("and press Enter to continue...")

if args.action == "setup":
    result = client.post('/domain/zone/' + args.domain + '/record', fieldType="TXT", subDomain="_acme-challenge", target=args.challenge, ttl=60)
    client.post('/domain/zone/' + args.domain + '/refresh')
elif args.action == "teardown":
    result = client.get('/domain/zone/' + args.domain + '/record', fieldType="TXT", subDomain="_acme-challenge")

    for id in result:
        client.delete('/domain/zone/' + args.domain + '/record/' + str(id), fieldType="TXT", subDomain="_acme-challenge")
else:
    usage()
    exit(1)

#print(result)
