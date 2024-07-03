from get_payments import get_venmo_payment_details
from export_to_csv import export_to_csv
from upload import upload_CSV

USING_GOOGLE_SHEET = True # set to false if you just want a csv file

def main():
    print("reading emails for transactions...")
    rows = get_venmo_payment_details()

    if rows:
        print("exporting to CSV...")
        export_to_csv(rows)
        
        if USING_GOOGLE_SHEET:
            print("exporting to Google Sheet...")
            upload_CSV()

        print("Done!")
    else:
        print("nothing to update!")

if __name__ == '__main__':
    main()
