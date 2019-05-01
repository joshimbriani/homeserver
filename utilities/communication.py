import click
import sendgrid
from sendgrid.helpers.mail import *
from twilio.rest import Client

# Communication.py allows modules to communicate
# sendEmail, sendText, call


class Communication:

    class __Communication:
        twilioSid = ""
        twilioAuthToken = ""
        sendgridAPIKey = ""
        credsSet = False
        twilioClient = ""
        sgClient = ""

        def __init__(self, sid, authToken, apiKey):
            self.twilioSid = sid
            self.twilioAuthToken = authToken
            self.sendgridAPIKey = apiKey
            self.twilioClient = Client(sid, authToken)
            self.sgClient = sendgrid.SendGridAPIClient(apiKey)

        def sendEmail(self, subject, contents):
            if self.sgClient == "":
                click.echo(
                    "No SendGrid client available. Call setCreds with an sid and auth token before.")
                return
            message = Mail(
                from_email="joshimbriani+homeserver@gmail.com",
                to_emails="joshimbriani@gmail.com",
                subject=subject,
                html_content=contents
            )
            try:
                response = self.sgClient.send(message)
            except Exception as e:
                print(e.message)

        def sendText(self, contents):
            if self.twilioClient == "":
                click.echo(
                    "No Twilio client available. Call setCreds with an sid and auth token before.")
                return
            self.twilioClient.api.account.messages.create(
                to="+16144620631",
                from_="+13132543471",
                body=contents
            )

        def call(self, contents):
            if self.twilioClient == "":
                click.echo(
                    "No Twilio client available. Call setCreds with an sid and auth token before.")
                return
            # Need to set up an outgoing web server for this.
            # Spike until later
            return

        def setCreds(self, sid, authToken, apiKey):
            self.twilioSid = sid
            self.twilioAuthToken = authToken
            self.sendgridAPIKey = apiKey
            self.twilioClient = Client(sid, authToken)
            self.sgClient = sendgrid.SendGridAPIClient(apikey=apiKey)

    instance = None

    def __new__(cls, sid, authToken, apiKey):  # __new__ always a classmethod
        if not Communication.instance:
            Communication.instance = Communication.__Communication(
                sid, authToken, apiKey)
        return Communication.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

    def sendEmail(self, subject, contents):
        self.instance.sendEmail(subject, contents)

    def sendText(self, contents):
        self.instance.sendText(contents)

    def call(self, contents):
        self.instance.call(contents)
