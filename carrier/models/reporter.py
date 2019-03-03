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
    Reporter model
"""


class ReporterModel(object):
    """ Reporter base class """

    @staticmethod
    def get_name():
        """ Reporter name, such as 'html' """
        raise NotImplementedError()

    @staticmethod
    def get_description():
        """ Reporter description """
        raise NotImplementedError()

    @staticmethod
    def depends_on():
        """ Return required depencies """
        raise NotImplementedError()

    @staticmethod
    def run_before():
        """ Return optional depencies """
        raise NotImplementedError()

    def on_start(self):
        """ Called when testing starts """
        raise NotImplementedError()

    def on_finish(self):
        """ Called when testing ends """
        raise NotImplementedError()

    def on_scanner_start(self):
        """ Called when scanner starts """
        raise NotImplementedError()

    def on_scanner_finish(self):
        """ Called when scanner ends """
        raise NotImplementedError()
