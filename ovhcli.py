import ovh

from tabulate import tabulate

# https://eu.api.ovh.com/createApp/
# to get your credentials
client = ovh.Client()

ck = client.new_consumer_key_request()
ck.add_rules(ovh.API_READ_ONLY, "/me")

ck.add_rules(ovh.API_READ_ONLY, "/me/api/credential")
ck.add_rules(ovh.API_READ_ONLY, "/me/api/credential/*")
ck.add_rule("DELETE", "/me/api/credential/*")

ck.add_rule("GET", "/me/api/application")
ck.add_rule("GET", "/me/api/application/*")
ck.add_rule("DELETE", "/me/api/application/*")

# Request token
validation = ck.request()

print("Please visit %s to authenticate" % validation['validationUrl'])
input("and press Enter to continue...")

# Print nice welcome message
print("Welcome", client.get('/me')['firstname'])

while True:
    action = input("Enter 'a' for apps or 'c' for credentials: ")

    if action == 'a':
        apps = client.get('/me/api/application')

        table = []

        for app_id in apps: 
            app_method = '/me/api/application/' + str(app_id)
            app = client.get(app_method)

            table.append([
                app_id,
                '[%s] %s' % (app['status'], app['name']),
                app['description'],
                app['applicationKey'],
            ])
        print(tabulate(table, headers=['ID', 'App Name', 'Description', 'App key']))

        while (id := input("Enter the ID of the apps to delete, or nothing to quit... ")) != "":
            print("Deleting", id, ".")
            client.delete('/me/api/application/' + id)

    elif action == 'c':
        credentials = client.get('/me/api/credential', status='validated')

        table = []
        for credential_id in credentials:
            credential_method = '/me/api/credential/' + str(credential_id)
            credential = client.get(credential_method)

            app_name = "-"
            app_desc = "<app deleted>"
            app_status = "deleted"

            try:
                application = client.get(credential_method + '/application')
                app_name = application["name"]
                app_desc = application["description"]
                app_status = application["status"]
            except:
                pass

            table.append([
                credential_id,
                '[%s] %s' % (app_status, app_name),
                app_desc,
                credential['creation'],
                credential['expiration'],
                credential['lastUse'],
            ])
        print(tabulate(table, headers=['ID', 'App Name', 'Description',
                               'Token Creation', 'Token Expiration', 'Token Last Use']))

        while (id := input("Enter the ID of the credentials to delete, or nothing to quit... ")) != "":
            print("Deleting", id, ".")
            client.delete('/me/api/credential/' + id)

    elif action == "":
        exit(0)
