#!/usr/bin/env python3
# -*- coding: utf8 -*-

import logging
import smtplib
import time
from markdown import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from objects.WebhookIdentifier import Webhook

class SendMail:
    smtp_server=""
    port=25
    sender_email = "sender@mail.com"
    receiver_email = ""
    message = None
    mail_group_destination = ""
    org=""

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
        self.sender_email = cfg.get('mail','mail_from')
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = "THE HIVE 4 Alert"
        self.message["From"] = self.sender_email
        self.mail_group_destination = "SOC_manager"
        self.org = cfg.get('TheHive', 'org')


    def send(self,receiver,subject,msg1):
        self.logger.info('SendMailConnector.send')
        try:
            self.smtp_server = self.cfg.get('mail', 'smtp_server')
            self.message["Subject"] = subject
            if receiver == "SOC_manager":
                self.message["To"] = self.cfg.get('mail', 'SOC_manager')
            elif receiver == "SOC_team":
                self.message["To"] = self.cfg.get('mail', 'SOC_team')
            else:
                self.logger.warning('%s.No valid recipient error', __name__)
        except Exception as e:
            self.logger.error('No valid recipient error', exc_info=True)
            raise
        msg = MIMEText(msg1, "html")
        self.message.attach(msg)
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.ehlo()  # Can be omitted
                server.sendmail(self.message["From"], self.message["To"].split(","), self.message.as_string())
        except Exception as e:
            self.logger.error('Fail to send email', exc_info=True)
            raise

    def processWebhook(self, webhookData,cfg):
        self.logger.info('SendMailConnector.processWebhook')
        webhook = Webhook(webhookData, cfg)

        self.logger.info('SendMailConnector.processWebhook.checkingAlerts')
        self.logger.info('SendMailConnector.processWebhook.checkingCases')
        self.logger.info('webhookData op: ' + webhookData['operation'])
        if webhook.isCase() and webhookData['operation'] == "create":
            self.logger.info('ManageWebhook.case created')
            createdBy = webhookData['object']['createdBy']
            updatedBy = webhookData['object']['updatedBy']
            createdAt = int(webhookData['object']['createdAt'])
            number = str(webhookData['details']['number'])
            title = webhookData['details']['title']
            description = webhookData['details']['description']
            owner = webhookData['object']['owner']
            subject = "The Hive4 - " + self.org + " - CASE CREATED --" + title
            msg = "Korisnik: " + self.org + "<br>"
            msg = msg + "Time: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(createdAt)) + "<br>"
            msg = msg + "Case number: " + number + "<br>"
            msg = msg + "Owner: " + owner + "<br>"
            msg = msg + "Created by: " + createdBy + "<br>"
            msg = msg + "Updated by: " + updatedBy + "<br>"
            msg = msg + "Title: " + title + "<br>"
            msg = msg + "Description:<br><code>" + markdown(description,extensions=['markdown.extensions.tables','markdown.extensions.extra']) + "</code><br>"
            mail_group_destination = "SOC_manager"
            self.send(mail_group_destination,subject, msg)
        if webhook.isCase() and webhookData['details']['status'] == "Resolved":
            self.logger.info('ManageWebhook.case closed')
            print(webhookData)
            createdBy = webhookData['object']['createdBy']
            createdAt = int(webhookData['object']['createdAt'])
            caseId = str(webhookData['object']['caseId'])
            title = webhookData['object']['title']
            reason = webhookData['details']['summary']
            description = webhookData['object']['description']
            createdBy = webhookData['object']['createdBy']
            updatedBy = webhookData['object']['updatedBy']
            owner = webhookData['object']['owner']
            subject = "The Hive4 - " + self.org + " - CASE CLOSED --" + title
            msg = "Korisnik: " + self.org + "<br>"
            msg = msg + "Time: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(createdAt)) + "<br>"
            msg = msg + "Case number: " + caseId + "<br>"
            msg = msg + "Owner: " + owner + "<br>"
            msg = msg + "Created by: " + createdBy + "<br>"
            msg = msg + "Updated by: " + updatedBy + "<br>"
            msg = msg + "Title: " + title + "<br>"
            msg = msg + "<b> " + "Reason for close: " + "</b>" +  reason + "<br>"
            msg = msg + "Description:<br><code>" + markdown(description,extensions=['markdown.extensions.tables','markdown.extensions.extra']) + "</code><br>"
            mail_group_destination = "SOC_manager"
            self.send(mail_group_destination,subject, msg)
        if webhook.isAlert() and webhookData['operation'] == "delete":
            title = webhookData['object']['title']
            self.logger.info('ManageWebhook.alert deleted')
            subject = "The Hive4 - " + self.org  + " - Alert deleted !"
            msg = "Time: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(webhookData['startDate']))) + "<br>"
            msg = msg + "Korisnik: <b>" + self.org + "</b>"
            mail_group_destination = "SOC_manager"
            self.send(mail_group_destination,subject, msg)
        elif webhook.isAlert() and webhookData['object']['status'] == "New":
            title = webhookData['object']['title']
            self.logger.info('ManageWebhook.alert new')
            subject = "The Hive4 - " + self.org   +  " - NEW ALERT !" + " --" + title
            msg = ""
            msg = "Time: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(webhookData['startDate']))) + "<br>"
            msg = msg + "Alert reference: " + webhookData['object']['sourceRef'] + "<br>"
            msg = msg + "Korisnik: <b>" + self.org + "</b><br>"
            msg = msg + "Source: " + webhookData['object']['source'] + "<br>"
            msg = msg + "Title: " + webhookData['object']['title'] + "<br>"
            msg = msg + "Description:<br> " + markdown(webhookData['object']['description'],extensions=['markdown.extensions.tables','markdown.extensions.extra']) + "<br>"
            print(msg)
            mail_group_destination = "SOC_manager"
            self.send(mail_group_destination,subject, msg)
        elif webhook.isAlert() and webhookData['object']['status'] == "Ignored":
            title = webhookData['object']['title']
            self.logger.info('ManageWebhook.alert ignored')
            subject = "The Hive4 - " + self.org + " - Alert ignored !"
            msg = "Time: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(webhookData['object']['createdAt']))) + "<br>"
            msg = msg + "Alert reference: " + webhookData['object']['sourceRef'] + "<br>"
            msg = msg + "Korisnik: " + self.org + "<br>"
            msg = msg + "Source: " + webhookData['object']['source'] + "<br>"
            msg = msg + "Title: " + webhookData['object']['title'] + "<br>"
            msg = msg + "Description:<br><code>" + markdown(webhookData['object']['description'],extensions=['markdown.extensions.tables','markdown.extensions.extra']) + "</code><br>"
            mail_group_destination = "SOC_manager"
            self.send(mail_group_destination,subject, msg)
