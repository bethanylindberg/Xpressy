import json


output_file = "C:\\Users\\skavy\\Desktop\\Updated Xpressy\\examples\\Stock_Images\\Gallery\\output.txt"


location_data = []
with open(output_file) as f:
    for line in f:
        line = line.split()
        print(line)
        location_data.append({"Image_ID": line[0],"score1":90,"score2":10})

    location_data = {"location_data": location_data}
output=json.dumps(location_data)
with open('no.txt', 'w') as txtfile:
    json.dump(location_data, txtfile)


