import os
import json
from jinja2 import Environment, FileSystemLoader
from .db import DbOps
import uuid
import smtplib
import os, boto3
from . import filesystem



class Email_AWS(object):
    default_sender = 'Datapare <no-reply@datapare.com>'
    CHARSET = "UTF-8"
    fs = filesystem.FileSystemOps()
    def __init__(self):
        config = self.fs.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
        self.CHARSET = "UTF-8"
        self.client = boto3.client('ses', aws_access_key_id=config["aws"]["access_key"],
                                   aws_secret_access_key=config["aws"]["secret_key"],
                                    region_name=config["aws"]["default_region"])


    def send(self, obj):
        email = obj["email"]
        sender = "info@datapare.com"
        subject="Datapare Notification"
        params = obj["items"]
        template_name = obj["email_template"]
        te = TemplateEngine()
        body = te.render(template_name, params)
        response = self.client.send_email(
            Destination={
                'ToAddresses': email.split(',')
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
        print(self.TEMPLATES_DIR)
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
            row = DbOps().execute_sql_return_results(sql)
            if row:
                token = row[0][0]

            else:
                token = uuid.uuid4()
                sql = """
                        select id
                        from general_user
                        where email='{0}'                      
                      """.format(email)
                user_id = DbOps().execute_sql_return_results(sql)[0][0]
                sql = """
                        insert into general_tokens(token, token_type, created_at, expire_at, is_expired, user_id)
                        values('{0}', 4, now(), now() + interval 10 year, 0, {1})
                      """.format(token, user_id)
                MysqlOps().execute_sql(sql)
            return token
    
        except Exception as e:
            print(e)
            pass
    
