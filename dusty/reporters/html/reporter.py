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
    Reporter: html
"""

from dusty.tools import log
from dusty.models.module import DependentModuleModel
from dusty.models.reporter import ReporterModel


class Reporter(DependentModuleModel, ReporterModel):
    """ Report results from scanners """

    @staticmethod
    def get_name():
        """ Reporter name """
        return "html"

    @staticmethod
    def get_description():
        """ Reporter description """
        return "HTML reporter"

    @staticmethod
    def fill_config(data_obj):
        """ Make sample config """
        raise NotImplementedError()

    @staticmethod
    def validate_config(config):
        """ Validate config """
        log.debug(f"Config: {config}")

    @staticmethod
    def depends_on():
        """ Return required depencies """
        return []

    @staticmethod
    def run_before():
        """ Return optional depencies """
        return ["email"]

    def __init__(self, context):
        """ Initialize reporter instance """
        self.context = context

    def report(self):
        """ Report """
        log.info("Reporting")

    def get_errors(self):
        """ Get errors """
        return list()

    def on_start(self):
        """ Called when testing starts """
        log.info("Testing started")

    def on_finish(self):
        """ Called when testing ends """
        log.info(f"Testing finished")

    def on_scanner_start(self, scanner):
        """ Called when scanner starts """
        log.info("Scanner %s started", scanner)

    def on_scanner_finish(self, scanner):
        """ Called when scanner ends """
        log.info("Scanner %s finished", scanner)
