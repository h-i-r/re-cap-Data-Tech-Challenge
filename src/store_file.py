import csv

def store_data(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)