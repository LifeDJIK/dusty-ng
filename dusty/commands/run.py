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
    Command: run
"""

# import importlib

from dusty.tools import log
from dusty.data import constants
from dusty.models.module import ModuleModel
from dusty.models.command import CommandModel
from dusty.helpers.context import RunContext
from dusty.scanners.performer import ScanningPerformer
from dusty.processing.performer import ProcessingPerformer
from dusty.reporters.performer import ReportingPerformer


class Command(ModuleModel, CommandModel):
    """ Runs tests defined in config file """

    @staticmethod
    def get_name():
        """ Command name """
        return "run"

    @staticmethod
    def get_description():
        """ Command help message (description) """
        return "run tests according to config"

    @staticmethod
    def fill_config(data_obj):
        """ Make sample config """
        # Will implement in future

    @staticmethod
    def validate_config(config):
        """ Validate config """
        # Will implement in future

    def __init__(self, argparser):
        """ Initialize command instance, add arguments """
        argparser.add_argument(
            "-e", "--config-variable", dest="config_variable",
            help="name of environment variable with config",
            type=str, default=constants.DEFAULT_CONFIG_ENV_KEY
        )
        argparser.add_argument(
            "-c", "--config-file", dest="config_file",
            help="path to config file",
            type=str, default=constants.DEFAULT_CONFIG_PATH
        )
        argparser.add_argument(
            "-s", "--suite", dest="suite",
            help="test suite to run",
            type=str, required=True
        )

    def execute(self, args):
        """ Run the command """
        log.info("Starting")
        if args.call_from_legacy:
            log.warning("Called from legacy entry point")
        context = RunContext(args)
        scanning = ScanningPerformer(context)
        processing = ProcessingPerformer(context)
        reporting = ReportingPerformer(context)
        scanning.perform()
        processing.perform()
        reporting.perform()

        # config = {
        #     "protocol": "http",
        #     "host": "127.0.0.1",
        #     "port": 80,
        # }
        # reporter = importlib.import_module(
        #     f"dusty.reporters.html"
        # ).Reporter(context)

        # reporter.on_start()
        # scanner = importlib.import_module(
        #     f"dusty.scanners.dast.{args.suite}"
        # ).Scanner(context)
        # scanner.execute(config)
        # results = scanner.get_results()
        # reporter.on_finish(results)
