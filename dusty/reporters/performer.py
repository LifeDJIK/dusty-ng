#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,R0903,W0702

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
        if "reporters" not in config:
            log.error("No reporters defined in config")
            raise ValueError("No reporters configuration present")

    def __init__(self, context):
        """ Initialize instance """
        self.context = context

    def prepare(self):
        """ Prepare for action """
        log.info("Preparing")
        general_config = dict()
        if "reporters" in self.context.config["general"]:
            general_config = self.context.config["general"]["reporters"]
        config = self.context.config["reporters"]
        for reporter_name in config:
            # Merge general config
            merged_config = general_config.copy()
            merged_config.update(config[reporter_name])
            config[reporter_name] = merged_config
            try:
                # Init reporter instance
                reporter = importlib.import_module(
                    f"dusty.reporters.{reporter_name}.reporter"
                ).Reporter(self.context)
                # Validate config
                reporter.validate_config(config[reporter_name])
                # Add to context
                self.context.reporters[reporter.get_name()] = reporter
            except:
                log.exception("Failed to prepare reporter %s", reporter_name)

    def perform(self):
        """ Perform action """
        log.info("Starting reporting")
        # Run reporters
        for reporter_module_name in self.context.reporters:
            reporter = self.context.reporters[reporter_module_name]
            reporter.report()

    def on_start(self):
        """ Called when testing starts """
        log.info("Testing started")

    def on_finish(self):
        """ Called when testing ends """
        log.info("Testing finished")

    def on_scanner_start(self, scanner):
        """ Called when scanner starts """
        log.info("Started scanning with %s", scanner)

    def on_scanner_finish(self, scanner):
        """ Called when scanner ends """
        log.info("Finished scanning with %s", scanner)

    def report(self):
        """ Report """
        raise NotImplementedError()
