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
    Scanner: html
"""

from dusty.tools import log
from dusty.models.module import ModuleModel
from dusty.models.reporter import ReporterModel


class Reporter(ModuleModel, ReporterModel):
    """ Report results from scanners """

    @staticmethod
    def get_name():
        """ Reporter name """
        return "html"

    @staticmethod
    def get_description():
        """ Reporter description """
        return "HTML reporter"

    def __init__(self, context):
        """ Initialize reporter instance """

    def on_start(self):
        """ Called when testing starts """
        log.info("Testing started")

    def on_finish(self, results):
        """ Called when testing ends """
        log.info(f"Testing done, got {len(results)} results")
