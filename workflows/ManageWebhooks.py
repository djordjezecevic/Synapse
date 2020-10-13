#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, sys
import logging

from datetime import date


current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = current_dir + '/..'
sys.path.insert(0, current_dir)

from common.common import getConf
from objects.WebhookIdentifier import Webhook
from objects.WebhookActuator import Actuator
from objects.SendMailConnector import SendMail

def manageWebhook(webhookData):
    """
        Filter webhooks received from TheHive and initiate actions like:
            - closing offense in QRadar
    """
    logger = logging.getLogger(__name__)
    logger.info('%s.ManageWebhook starts', __name__)
    report = dict()
    cfg = getConf()
    logger.info('---------------------------------------')
    webhook = Webhook(webhookData, cfg)
    mailSender = SendMail(cfg)
    mailSender.processWebhook(webhookData,cfg)

    actuator = Actuator(cfg)

    print(webhookData)

    #we are only interrested in update webhook at the moment
    if webhook.isUpdate():
        severity = 0
        try:
            severity = webhookData['object']['severity']
            print(severity)
        except Exception as e:
            self.logger.error('Ne postoji severity, ostaje 0')
        report['action'] = 'Update'
        if webhook.isQRadarAlertMarkedAsRead():
            actuator.closeOffense(webhook.offenseId,severity)
            report['action'] = 'closeOffense'
            loger.info("is readed")
        elif webhook.isClosedQRadarCase():
            actuator.closeOffense(webhook.offenseId,severity)
            report['action'] = 'closeOffense'
            loger.info("is closed")

    else:
        #is not update or not a QRadar alert marked as read or not a closed QRadar case
        report['action'] = 'None'

    report['success'] = True
    return report

if __name__ == '__main__':
    print('Please run from API only')
