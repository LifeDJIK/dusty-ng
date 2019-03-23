#!/usr/bin/python3
# coding=utf-8

#   Copyright 2019 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
    Scanner: OWASP ZAP
"""

from dusty.tools import log
from dusty.models.module import ModuleModel
from dusty.models.scanner import ScannerModel


class Scanner(ModuleModel, ScannerModel):
    """ Scanner class """

    @staticmethod
    def get_name():
        """ Scanner name, such as 'OWASP ZAP' """
        return "OWASP ZAP"

    @staticmethod
    def get_description():
        """ Scanner description """
        return "OWASP Zed Attack Proxy (ZAP)"

    def __init__(self, context):
        """ Initialize scanner instance """

    def execute(self, config):
        """ Run the scanner """
        log.info("Starting")

    def results(self):
        """ Get findings """
        return []
