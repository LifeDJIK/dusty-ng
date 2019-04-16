#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,E0401,W0702

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
    Scanner: OWASP ZAP
"""

import time
import subprocess
from zapv2 import ZAPv2

from dusty.tools import log
from dusty.models.module import ModuleModel
from dusty.models.scanner import ScannerModel


class Scanner(ModuleModel, ScannerModel):
    """ Scanner class """

    @staticmethod
    def get_name():
        """ Module name """
        return "OWASP ZAP"

    @staticmethod
    def get_description():
        """ Module description or help message """
        raise "OWASP Zed Attack Proxy (ZAP)"

    @staticmethod
    def fill_config(data_obj):
        """ Make sample config """
        raise NotImplementedError()

    @staticmethod
    def validate_config(config):
        """ Validate config """
        log.debug(f"Config: {config}")
        # if "scanners" not in config:
        #     log.error("No scanners defined in config")
        #     raise ValueError("No scanners configuration present")

    def __init__(self, context):
        """ Initialize scanner instance """
        self._context = context
        self._results = list()
        self._zap_daemon = None
        self._zap = None

    def execute(self):
        """ Run the scanner """
        raise NotImplementedError()

    def get_results(self):
        """ Get results """
        return self._results

    def get_errors(self):
        """ Get errors """
        raise NotImplementedError()

    def _execute(self, config):
        """ Run the scanner """
        log.info("Starting")
        try:
            self._start_zap()
            self._create_zap_client()
            self._wait_zap_start()
            #
            target = "{}://{}".format(
                config.get("protocol"),
                config.get("host"),
            )
            proto = config.get("protocol")
            port = config.get("port")
            if (proto == "http" and int(port) != 80) or \
                    (proto == "https" and int(port) != 443):
                target = f"{target}:{port}"
            log.info("Using target %s", target)
            #
            raise RuntimeError("Error")
        except:
            log.exception("Error during ZAP scanning")
        try:
            pass
        except:
            log.exception("Error during ZAP finalizing")
        finally:
            self._stop_zap()

        # Spider
        # log.info("Spidering target %s", target)
        # scan_id = zap.spider.scan(target)
        # while int(zap.spider.status(scan_id)) < 100:
        #     log.info(
        #         "Spidering progress %d%%", int(zap.spider.status(scan_id))
        #     )
        #     time.sleep(3)
        # Wait for passive scan
        # while int(zap.pscan.records_to_scan) > 0:
        #     log.info(
        #         "Passive scan queue %d", int(zap.pscan.records_to_scan)
        #     )
        #     time.sleep(2)
        # AjaxSpider
        # zap.ajaxSpider.scan(target)
        # while zap.ajaxSpider.status == "running":
        #     log.info(
        #         "AjaxSpider %s %d",
        #         zap.ajaxSpider.status, int(zap.ajaxSpider.number_of_results)
        #     )
        #     time.sleep(5)
        # Wait for passive scan
        # while int(zap.pscan.records_to_scan) > 0:
        #     log.info(
        #         "Passive scan queue %d", int(zap.pscan.records_to_scan)
        #     )
        #     time.sleep(2)
        # Active scan
        # log.info("Active scan against target %s", target)
        # scan_id = zap.ascan.scan(target)
        # while int(zap.ascan.status(scan_id)) < 100:
        #     log.info(
        #         "Active scan progress %d%%", int(zap.ascan.status(scan_id))
        #     )
        #     time.sleep(5)
        # Wait for passive scan
        # while int(zap.pscan.records_to_scan) > 0:
        #     log.info(
        #         "Passive scan queue %d", int(zap.pscan.records_to_scan)
        #     )
        #     time.sleep(2)
        # Get report
        # log.info("Scan finished. Processing results")
        # self._results.append(zap.core.jsonreport())
        # Stop zap
        # self._stop_zap()

    def _start_zap(self):
        log.info("Starting ZAP daemon")
        self._zap_daemon = subprocess.Popen([
            "/usr/bin/java", "-Xmx499m",
            "-jar",
            "".join([
                "/Users/lifedjik",
                "/Vault/Projects/Job/EPAM/zap",
                "/ZAP_D-2019-02-25/zap-D-2019-02-25.jar"
            ]),
            "-daemon", "-port", "8091", "-host", "0.0.0.0",
            "-config", "api.key=dusty",
            "-config", "api.addrs.addr.regex=true",
            "-config", "api.addrs.addr.name=.*",
            "-config", "ajaxSpider.browserId=htmlunit"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _stop_zap(self):
        if self._zap_daemon is not None:
            log.info("Stopping ZAP daemon")
            self._zap_daemon.kill()
            self._zap_daemon.wait()
            self._zap_daemon = None

    def _create_zap_client(self):
        self._zap = ZAPv2(
            apikey="dusty",
            proxies={
                "http": "http://127.0.0.1:8091",
                "https": "http://127.0.0.1:8091"
            }
        )

    def _wait_zap_start(self):
        zap_started = False
        for _ in range(600):
            try:
                log.info("Started ZAP %s", self._zap.core.version)
                zap_started = True
                break
            except IOError:
                time.sleep(1)
        if not zap_started:
            raise RuntimeError("ZAP failed to start")
