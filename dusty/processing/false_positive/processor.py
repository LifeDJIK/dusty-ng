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
    Processor: false_positive
"""

from dusty.tools import log
from dusty.models.module import DependentModuleModel
from dusty.models.processor import ProcessorModel


class Processor(DependentModuleModel, ProcessorModel):
    """ Process results: filter false-positives """

    def __init__(self, context):
        """ Initialize processor instance """
        self.context = context
        self.errors = list()

    def execute(self):
        """ Run the processor """
        log.info("Processing false-positives")

    def get_errors(self):
        """ Get errors """
        return self.errors

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
        return []

    @staticmethod
    def get_name():
        """ Module name """
        return "false_positive"

    @staticmethod
    def get_description():
        """ Module description """
        return "False-positive processor"
