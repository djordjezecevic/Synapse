#!/usr/bin/env python3
# -*- coding: utf8 -*-

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendMail:
    smtp_server=""
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
        self.cfg = cfg
        smtp_server="smtp.saga.co.yu"
        port=25
        sender_email = "infosec@saga.co.yu"
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = "THE HIVE 4 Alert"
        self.message["From"] = sender_email

    def send(self,receiver,msg1):
        try:
            self.smtp_server = self.cfg.get('mail', 'smtp_server')
            if receiver == "SOC_manager":
                self.message["To"] = self.cfg.get('mail', 'SOC_manager')
            elif receiver == "SOC_team":
                self.message["To"] = self.cfg.get('mail', 'SOC_team')
            else:
                self.logger.warning('%s.No valid recipient error', __name__)
        except Exception as e:
            self.logger.error('No valid recipient error', exc_info=True)
            raise
        msg = MIMEText(msg1, "plain")
        self.message.attach(msg)
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.ehlo()  # Can be omitted
                server.sendmail(self.message["From"], self.message["To"].split(","), self.message.as_string())
        except Exception as e:
            self.logger.error('Fail to send email', exc_info=True)
            raise
