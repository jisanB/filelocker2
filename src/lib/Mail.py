# -*- coding: utf-8 -*-
from smtplib import SMTP
import cherrypy
from Cheetah.Template import Template
import logging
from Models import *

#Recipients must be a list object
        
def get_server(config):
    server = SMTP(config['smtp_server'], config['smtp_port'] )
    if self.config['smtp_start_tls']:
        server.ehlo(config['smtp_sender'])
        server.starttls()
        server.ehlo(self.config['smtp_sender'])
    if self.config['smtp_auth_required']:
        server.login(self.config['smtp_user'], self.config['smtp_pass'] )
    return server

def notify(template, varDict={}):
    config = cherrypy.request.app.config['filelocker']
    if varDict.has_key("recipient") and varDict['recipient'] is not None and varDict['recipient'] != "":
        linksObscured = False
        if self.config.has_key("smtp_obscure_links") and self.config['smtp_obscure_links']:
            linksObscured = True
            if varDict.has_key("filelockerURL"):
                varDict['filelockerURL'] = self.make_unclickable(config['root_url'])
        server = get_server()
        sender = config['smtp_sender']
        tpl = Template(file=template, searchList=[locals(),globals()])
        smtpresult = server.sendmail(config['smtp_sender'], varDict['recipient'], str(tpl))
        server.close()

def make_unclickable(self, link):
    return link.replace(".", " . ").replace("http://", "").replace("https://", "")