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
    Processing performer
"""

# import importlib

from dusty.tools import log
from dusty.models.module import ModuleModel
from dusty.models.performer import PerformerModel


class ProcessingPerformer(ModuleModel, PerformerModel):
    """ Process results """

    @staticmethod
    def get_name():
        """ Module name """
        return "processing"

    @staticmethod
    def get_description():
        """ Module description or help message """
        raise "performs result processing"

    @staticmethod
    def fill_config(data_obj):
        """ Make sample config """
        raise NotImplementedError()

    @staticmethod
    def validate_config(config):
        """ Validate config """
        if "processing" not in config:
            log.warning("No processing defined in config")

    def __init__(self, context):
        """ Initialize instance """
        self.context = context

    def prepare(self):
        """ Prepare for action """
        log.info("Preparing")

    def perform(self):
        """ Perform action """
        log.info("Starting")