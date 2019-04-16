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
    Scanning performer
"""

import importlib

from dusty.tools import log
from dusty.models.module import ModuleModel
from dusty.models.performer import PerformerModel


class ScanningPerformer(ModuleModel, PerformerModel):
    """ Runs scanners """

    @staticmethod
    def get_name():
        """ Module name """
        return "scanning"

    @staticmethod
    def get_description():
        """ Module description or help message """
        raise "performs scanning"

    @staticmethod
    def fill_config(data_obj):
        """ Make sample config """
        raise NotImplementedError()

    @staticmethod
    def validate_config(config):
        """ Validate config """
        if "scanners" not in config:
            log.error("No scanners defined in config")
            raise ValueError("No scanners configuration present")

    def __init__(self, context):
        """ Initialize instance """
        self.context = context

    def prepare(self):
        """ Prepare for action """
        log.info("Preparing")
        general_config = dict()
        if "scanners" in self.context.config["general"]:
            general_config = self.context.config["general"]["scanners"]
        config = self.context.config["scanners"]
        for scanner_type in config:
            for scanner_name in config[scanner_type]:
                # Merge general config
                if scanner_type in general_config:
                    merged_config = general_config[scanner_type].copy()
                    merged_config.update(config[scanner_type][scanner_name])
                    config[scanner_type][scanner_name] = merged_config
                # Init scanner instance
                scanner = importlib.import_module(
                    f"dusty.scanners.{scanner_type}.{scanner_name}.scanner"
                ).Scanner(self.context)
                self.context.scanners[scanner.get_name()] = scanner
                # Validate config
                scanner.validate_config(config[scanner_type][scanner_name])

    def perform(self):
        """ Perform action """
        log.info("Starting")
        for scanner_module_name in self.context.scanners:
            scanner = self.context.scanners[scanner_module_name]
            log.info(f"Running {scanner.get_name()} ({scanner.get_description()})")
            scanner.execute()
