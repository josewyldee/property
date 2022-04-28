# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        for row in data:
            # print("(((((((((((((((((((((((((()))))))))))))))))))")
            # print(data)
            document=None
            if row['document']:
                document = "<br> <strong>(This email has an attachment)<strong>"
            subject, from_email, to = row['subject'], 'noreply@example.com', row['to']
            text_content = f"Hey {row['name']},{row['body']}."
            # html_content = render_to_string('email_templates/message.html', {'name': row['name'],'body':row['body'],'property':row['property'],'from':row['from'],'document':document})
            if row['subject']=="Lease created":
                html_content = render_to_string( row['template'], {'name': row['name'],'color':row['color'],'body':row['body'],'property':row['property'],'from':row['from'],'unit':row['unit'],'document':document,'lease_type':row['lease_type'],'lease_from':row['lease_from'],'lease_to':row['lease_to']})
            if row['subject']=="Lease termination":
                html_content = render_to_string( row['template'], {'name': row['name'],'color':row['color'],'body':row['body'],'property':row['property'],'from':row['from'],'unit':row['unit'],'document':document,'lease_type':row['lease_type'],'lease_from':row['lease_from'],'reason':row['reason'],'description':row['description']})
            else:
                html_content = render_to_string( row['template'], {'name': row['name'],'color':row['color'],'body':row['body'],'property':row['property'],'from':row['from'],'amount':row['amount'],'document':document,'href':row['href']})

            email = EmailMultiAlternatives(subject, text_content, from_email, [to])
            email.attach_alternative(html_content, "text/html")
           
            
            if row['document']:
                for f in row['document']:
                    # print("----------------------",f['name'])
                    # eeeee
                    email.attach(f['name'], f['read'], f['type'])
            EmailThread(email).start()


        