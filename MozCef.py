# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Created by Rob Tucker <rtucker@mozilla.com> July 23. 2012

import os
import syslog

class MozCef(object):

    def __init__(self, prog_name, facility=syslog.LOG_LOCAL4):
        """
            init function for MozCef
            typical usage:
                items = []
                items.append({'suser': request.user})
                items.append({'cs1Label': 'asset_tag'})
                items.append({'cs1': 'abc123'})
                items.append({'cs2Label': 'id'})
                items.append({'cs2': '1234'})
                items.append({'duser': 'theuser@domain.com'})
                mc = MozCef('TestApplication')
                mc.log_cef('Authentication Failed', 
                            'Authentication failed for user foo', items=items)
            param: prog_name - String to represent the program name in syslog
            param: facility - syslog facility type, 
                defaults to syslog.LOG_LOCAL4
        """
        self.prog_name = prog_name
        self.facility = facility


    def log_cef(self, message_name, message_description, type='LOG_INFO', items=[]):
        """
            log_cef method to actually write message to syslog
            param: message_name - Generic name of message type
            param: message_description - More verbose details of the message to 
                be logged
            param: type - A string representation of the syslog facility, 
                LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING, 
                LOG_NOTICE, LOG_INFO, LOG_DEBUG
                http://unix.superglobalmegacorp.com/Net2/newsrc/sys/syslog.h.html
            param: items - List of cef specific key/value pairs

            typical usage:

        """
        # Open a connection to syslog to the proper facility

        syslog.openlog(self.prog_name, 0, self.facility)
        label_string = ''

        # Iterating over the items list and construct the label string to send
        for row in items:
            for key, value in row.items():
                label_string = "%s%s=%s " %(label_string, str(key), str(value))
        cefmsg = 'CEF:0|Mozilla|%s|1.0|%s|%s|5|%s dhost=%s'% (self.prog_name, 
                message_name, message_description, label_string, os.uname()[1])
        try:
            syslog_level = getattr(syslog, type)
        except AttributeError:
            raise BaseException('Unable to find syslog type')
        syslog.syslog(syslog_level, cefmsg)
        syslog.closelog()
