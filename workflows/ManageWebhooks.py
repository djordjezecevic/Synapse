#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, sys
import logging
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
    webhook = Webhook(webhookData, cfg)
    # mail sender objekat. Djordje
    mailSender = SendMail(cfg)
#    actuator = Actuator(cfg)
    #we are only interrested in update webhook at the moment

    # dodati da li je alert ili case
    hookType = webhook.webhookType()
    # pa poslati mail
    if hookType=="alert":
#       print("It is alert !")
        mailSender.send("djordje.zecevic@saga.rs", "It is alert !")
    if hookType=="case":
#        print("It is case !")
        mailSender.send("djordje.zecevic@saga.rs", "It is case !")

    if webhook.isUpdate():
        report['action'] = 'Update'
#        if webhook.isQRadarAlertMarkedAsRead():
#            actuator.closeOffense(webhook.offenseId)
#            report['action'] = 'closeOffense'
#        elif webhook.isClosedQRadarCase():
#            actuator.closeOffense(webhook.offenseId)
#            report['action'] = 'closeOffense'
    else:
        #is not update or not a QRadar alert marked as read or not a closed QRadar case
        report['action'] = 'None'

    report['success'] = True
    return report

if __name__ == '__main__':
    print('Please run from API only')
