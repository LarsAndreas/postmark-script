import requests

class Server:
    def __init__(self, id, name, tokens):
        self.id = id
        self.name = name
        self.tokens = tokens

def get_server_tokens(postmarkAccountToken: str):
    headers = {
        "Accept": "application/json",
        "X-Postmark-Account-Token": postmarkAccountToken,
    }

    response = requests.get("https://api.postmarkapp.com/servers?count=500&offset=0", headers=headers)
    servers = response.json()['Servers']

    api_tokens = []
    for server in servers:
        api_tokens.append(Server(server["ID"], server["Name"], server["ApiTokens"]))

    return api_tokens

def get_sent_count(postmarkServerToken: str):
    headers = {
        "Accept": "application/json",
        "X-Postmark-Server-Token": postmarkServerToken,
    }
    response = requests.get("https://api.postmarkapp.com/stats/outbound", headers=headers)
    return response.json()['Sent']

def get_sent_count_past_three_months(postmarkServerToken: str):
    headers = {
        "Accept": "application/json",
        "X-Postmark-Server-Token": postmarkServerToken,
    }

    response = requests.get("https://api.postmarkapp.com/stats/outbound?fromdate=2022-06-13&todate=2022-09-13", headers=headers)

    return response.json()['Sent']

def get_sent_count_from_server(server: Server):
        count = 0
        for token in server.tokens:
            count += get_sent_count(token)
        return count

def get_sent_count_from_server_past_three_months(server: Server):
        count = 0
        for token in server.tokens:
            count += get_sent_count_past_three_months(token)
        return count

def get_sent_count_from_servers(servers: list[Server]):
    result = []
    for server in servers:
        count = get_sent_count_from_server(server)
        count_past_three_months = get_sent_count_from_server_past_three_months(server)
        entry = (server.name, count, count_past_three_months, f"https://account.postmarkapp.com/servers/{server.id}/streams")
        print(entry)
        result.append(entry)

    return result

if __name__ == "__main__":
    postmarkAccountToken = input("Enter your postmark account token: ")
    servers = get_server_tokens()
    result = get_sent_count_from_servers(servers)
    csv = "\n".join(list(map(lambda x: f"{x[0]},{x[1]},{x[2]},{x[3]}", result)))
    with open("postmark-outbound-count.csv", "w") as text_file:
        text_file.write(csv)