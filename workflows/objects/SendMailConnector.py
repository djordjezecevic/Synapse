#!/usr/bin/env python3
# -*- coding: utf8 -*-

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendMail:
    smtp_server="smtp.saga.co.yu"
    port=25
    sender_email = "infosec@saga.co.yu"
    receiver_email = "djordje.zecevic@saga.rs"
    message = None
    def __init__(self, cfg):
        """
            Class constuctor

            :param cfg: synapse configuration
            :type cfg: ConfigParser

            :return:
            :rtype:
        """

        self.logger = logging.getLogger('workflows.' + __name__)
        smtp_server="smtp.saga.co.yu"
        port=25
        sender_email = "infosec@saga.co.yu"
        receiver_email = "djordje.zecevic@saga.rs;nemanja.joksimovic@saga.rs"
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = "THE HIVE 4 Alert"
        self.message["From"] = sender_email

    def send(self,receiver_email,msg1):
        self.message["To"] = receiver_email
        msg = MIMEText(msg1, "plain")
        self.message.attach(msg)
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo()  # Can be omitted
            server.sendmail(self.sender_email, self.receiver_email, self.message.as_string())

#S1 = SendMail("")
#S1.send("djordje.zecevic@saga.rs", "It is alert and sending email to SOC manager and SOC team")
