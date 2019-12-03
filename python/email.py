import os
import json
from jinja2 import Environment, FileSystemLoader
from .db import DbOps
import uuid
import smtplib
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



class Email_AWS(object):
    default_sender = 'Datapare <no-reply@datapare.com>'
    CHARSET = "UTF-8"
    def __init__(self):
        self.CHARSET = "UTF-8"
        self.client = boto3.client('ses', aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                                    region_name=config.AWS_DEFAULT_REGION)


    def send(self, receipent, sender,  subject="Datapare Notification", body=""):
        
        response = self.client.send_email(
            Destination={
                'ToAddresses': receipent.split(',')
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': self.CHARSET,
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': self.CHARSET,
                    'Data': subject,
                },
            },
            Source=sender,
        )

class Email_Sendgrid(object):
    default_sender = 'Datapare <no-reply@datapare.com>'
    def __init__(self):
        with open(os.path.dirname(__file__) + '/../config.json','r') as my_file:
            self.config = json.load(my_file)

    def send(self, receipent, sender,  subject="Datapare Notification", body=""):
        message = Mail(
            from_email='info@datapare.com',
            to_emails='serkanuz@datapare.com',
            subject=subject,
            html_content=body)
        try:
            sg = SendGridAPIClient("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")
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
       

class TemplateEngine(object):
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TEMPLATES_DIR = os.path.join(self.BASE_DIR, 'email_templates')

    def render(self, template_name, params):
        #email=params["email"]
        
        unsubscribe_token = self.get_token(params)
        
        const = {
            "url_top_logo": "https://dataparestorage.blob.core.windows.net/dp-web-assets/logo_mail.png",
            "url_dashboard": "https://www.datapare.com/login",
            "url_website": "https://datapare.com/",
            "url_contact": "https://datapare.com/contact/",
            "url_unsubscribe":"https://auth.datapare.com/unsubscribe/{0}".format(unsubscribe_token),
            "email_support": "info@datapare.com",
            "address": "Datapare, 175 Varick Street - New York, NY, USA - 10014",
            "template_name":template_name, 
            "params":params,
            
        }
        #data = {**const, **params} # Hata aldım. TypeError: 'list' object is not a mapping

        j2_env = Environment(loader=FileSystemLoader(self.TEMPLATES_DIR), trim_blocks=True)
        j2 = j2_env.get_template(template_name)

        self.html = j2.render(const)
        return self.html
    
    def get_token(self, params):
        try:
            email = params["email"]
            sql = """
                    select token
                    from general_user u
                    inner join general_tokens t on t.user_id = u.id
                    where t.id = (select max(id) from general_tokens where token_type=4 and user_id=u.id and is_expired=0) and u.email='{0}'
                  """.format(email)
            row = MysqlOps().execute_sql_return_results(sql)
            if row:
                token = row[0][0]

            else:
                token = uuid.uuid4()
                sql = """
                        select id
                        from general_user
                        where email='{0}'                      
                      """.format(email)
                user_id = MysqlOps().execute_sql_return_results(sql)[0][0]
                sql = """
                        insert into general_tokens(token, token_type, created_at, expire_at, is_expired, user_id)
                        values('{0}', 4, now(), now() + interval 10 year, 0, {1})
                      """.format(token, user_id)
                MysqlOps().execute_sql(sql)
            return token
    
        except Exception as e:
            print(e)
            pass
    
