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

from dusty.tools import log
from dusty.models.performer import PerformerModel
from dusty.models.reporter import ReporterModel


class ReportingPerformer(PerformerModel, ReporterModel):
    """ Perform reporting """

    def __init__(self, context):
        """ Initialize instance """
        self.context = context

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
