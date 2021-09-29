import json

with open("userData.json", 'r') as file:
    data = json.load(file)
    file.close()

for user in data["users"]:
    print(data["users"][user]["name"], end='\n\t')
    for elem in data["users"][user]:
        print(f"{elem}: {data['users'][user][elem]}", end="\n\t")
    print()

for elem in data["lang"]:
    print(elem, end='\n\t')
    for nelem in data["lang"][elem]:
        print(nelem, end='\n\t')
        for nnelem in data["lang"][elem][nelem]:
            print(nnelem, end='\n\t')

print("************" * 10)
