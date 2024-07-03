import csv

def export_to_csv(rows):
    
    with open("transactions.csv", mode='a') as csvfile:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for row in rows:
            writer.writerow(row)
        
        csvfile.close()
                
    return
