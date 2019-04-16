#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,R0903

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
    Reporting performer
"""

import importlib

from dusty.tools import log
from dusty.models.module import ModuleModel
from dusty.models.performer import PerformerModel
from dusty.models.reporter import ReporterModel


class ReportingPerformer(ModuleModel, PerformerModel, ReporterModel):
    """ Perform reporting """

    @staticmethod
    def get_name():
        """ Module name """
        return "reporting"

    @staticmethod
    def get_description():
        """ Module description or help message """
        raise "performs result reporting"

    @staticmethod
    def fill_config(data_obj):
        """ Make sample config """
        raise NotImplementedError()

    @staticmethod
    def validate_config(config):
        """ Validate config """
        raise NotImplementedError()

    def __init__(self, context):
        """ Initialize instance """
        self.context = context

    def prepare(self):
        """ Prepare for action """
        log.info("Preparing")

    def perform(self):
        """ Perform action """
        log.info("Starting")

    def on_start(self):
        """ Called when testing starts """
        raise NotImplementedError()

    def on_finish(self):
        """ Called when testing ends """
        raise NotImplementedError()

    def on_scanner_start(self, scanner):
        """ Called when scanner starts """
        raise NotImplementedError()

    def on_scanner_finish(self, scanner):
        """ Called when scanner ends """
        raise NotImplementedError()

    @staticmethod
    def depends_on():
        """ Return required depencies """
        raise NotImplementedError()

    @staticmethod
    def run_before():
        """ Return optional depencies """
        raise NotImplementedError()
