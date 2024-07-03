import os
from export_to_csv import export_to_csv
from imap_tools import MailBox, AND

# class for relevant transaction info
class Transaction:
    def __init__(self, sender_name, amount_paid, date_paid, note):
        self.sender_name = sender_name
        self.amount_paid = amount_paid
        self.date_paid = date_paid
        self.note = note

# reads emails to extract relevant payment information
def get_venmo_payment_details():

    email_address = os.getenv("EMAIL_USER") # enter email
    password = os.getenv("EMAIL_PASSWORD") # enter email account password
    message_box = "Inbox" # box to check
    server = "imap.gmail.com"
    transactions = []

    if not email_address or not password:
        raise ValueError("Email credentials are not set in environment variables")

    with MailBox(server).login(email_address, password, message_box) as mailbox:
        sender_email = 'venmo@venmo.com'
        emails = mailbox.fetch(AND(from_=sender_email, seen=False))

        for msg in emails:

            if not msg.subject.startswith('You ') and not msg.subject.startswith('Your '):
                subject = msg.subject.split(" ")

                sender_name = ""
                for word in subject:
                    if word == "paid":
                        break
                    sender_name += word + " "

                if subject[-1] == "request":
                    amount_paid = subject[len(subject) - 2]
                else: 
                    amount_paid = subject[-1]

                date_paid = str(msg.date).split(" ")[0]

                html = msg.html.split("\n")

                for i in range(len(html)):
                    html[i] = html[i].strip()                  

                note_index = html.index('<!-- note -->') + 2
                note_div = html[note_index]
                note = note_div[3:len(note_div) - 4]

                new_transaction = {"sender_name": sender_name, "amount_paid": amount_paid, "date_paid": date_paid, "note": note}
                transactions.append(new_transaction)

                mailbox.flag(msg.uid, '\\Seen', True)
            else: 
                mailbox.flag(msg.uid, '\\Seen', False)

    return transactions
