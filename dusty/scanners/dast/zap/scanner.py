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
from dusty.data import constants
from dusty.models.module import DependentModuleModel
from dusty.models.scanner import ScannerModel


class Scanner(DependentModuleModel, ScannerModel):
    """ Scanner class """

    def __init__(self, context):
        """ Initialize scanner instance """
        self.context = context
        self.results = list()
        self.errors = list()
        self._zap_daemon = None
        self._zap_api = None

    def execute(self):
        """ Run the scanner """
        try:
            self._start_zap()
        finally:
            self._stop_zap()

    def get_results(self):
        """ Get results """
        return self.results

    def get_errors(self):
        """ Get errors """
        return self.errors

    def _start_zap(self):
        """ Start ZAP daemon, create API client """
        log.info("Starting ZAP daemon")
        self._zap_daemon = subprocess.Popen([
            "/usr/bin/java", "-Xmx499m",
            "-jar", constants.ZAP_PATH,
            "-daemon", "-port", "8091", "-host", "0.0.0.0",
            "-config", "api.key=dusty",
            "-config", "api.addrs.addr.regex=true",
            "-config", "api.addrs.addr.name=.*",
            "-config", "ajaxSpider.browserId=htmlunit"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self._zap_api = ZAPv2(
            apikey="dusty",
            proxies={
                "http": "http://127.0.0.1:8091",
                "https": "http://127.0.0.1:8091"
            }
        )

    def _wait_for_zap_start(self):
        for _ in range(600):
            try:
                log.info("Started ZAP %s", self._zap_api.core.version)
                return True
            except IOError:
                time.sleep(1)
        return False

    def _stop_zap(self):
        if self._zap_daemon:
            log.info("Stopping ZAP daemon")
            self._zap_daemon.kill()
            self._zap_daemon.wait()
            self._zap_daemon = None




        # # ZAP wrapper
        # tool_name = "ZAP"
        # results = list()
        # # Start ZAP daemon in background (no need for supervisord)

        # # Wait for zap to start

        # if not zap_started:
        #     logging.error("ZAP failed to start")
        #     zap_daemon.kill()
        #     zap_daemon.wait()
        #     return tool_name, results

        # # Format target URL
        # proto = config.get("protocol")
        # host = config.get("host")
        # port = config.get("port")
        # target = f"{proto}://{host}"
        # if (proto == "http" and int(port) != 80) or \
        #         (proto == "https" and int(port) != 443):
        #     target = f"{target}:{port}"
        # logging.info("Scanning target %s", target)
        # # Setup context
        # logging.info("Preparing context")
        # zap_context_name = "dusty"
        # zap_context = zap_api.context.new_context(zap_context_name)
        # # Setup context inclusions and exclusions
        # zap_api.context.include_in_context(zap_context_name, f".*{re.escape(host)}.*")
        # for include_regex in config.get("include", list()):
        #     zap_api.context.include_in_context(zap_context_name, include_regex)
        # for exclude_regex in config.get("exclude", list()):
        #     zap_api.context.exclude_from_context(zap_context_name, exclude_regex)
        # if config.get("auth_script", None):
        #     # Load our authentication script
        #     zap_api.script.load(
        #         scriptname="zap-selenium-login.js",
        #         scripttype="authentication",
        #         scriptengine="Oracle Nashorn",
        #         filename=pkg_resources.resource_filename(
        #             "dusty", "templates/zap-selenium-login.js"
        #         ),
        #         scriptdescription="Login via selenium script"
        #     )
        #     # Enable use of laoded script with supplied selenium-like script
        #     zap_api.authentication.set_authentication_method(
        #         zap_context,
        #         "scriptBasedAuthentication",
        #         urllib.parse.urlencode({
        #             "scriptName": "zap-selenium-login.js",
        #             "Script": base64.b64encode(
        #                 json.dumps(
        #                     config.get("auth_script")
        #                 ).encode("utf-8")
        #             ).decode("utf-8")
        #         })
        #     )
        #     # Add user to context
        #     zap_user = zap_api.users.new_user(zap_context, "dusty_user")
        #     zap_api.users.set_authentication_credentials(
        #         zap_context,
        #         zap_user,
        #         urllib.parse.urlencode({
        #             "Username": config.get("auth_login", ""),
        #             "Password": config.get("auth_password", ""),
        #             "type": "UsernamePasswordAuthenticationCredentials"
        #         })
        #     )
        #     # Enable added user
        #     zap_api.users.set_user_enabled(zap_context, zap_user, True)
        #     # Setup auth indicators
        #     if config.get("logged_in_indicator", None):
        #         zap_api.authentication.set_logged_in_indicator(
        #             zap_context, config.get("logged_in_indicator")
        #         )
        #     if config.get("logged_out_indicator", None):
        #         zap_api.authentication.set_logged_out_indicator(
        #             zap_context, config.get("logged_out_indicator")
        #         )
        # # Setup scan policy
        # scan_policy_name = "Default Policy"
        # scan_policies = [
        #     item.strip() for item in config.get("scan_types", "all").split(",")
        # ]
        # # Disable globally blacklisted rules
        # for item in c.ZAP_BLACKLISTED_RULES:
        #     zap_api.ascan.set_scanner_alert_threshold(
        #         id=item,
        #         alertthreshold="OFF",
        #         scanpolicyname=scan_policy_name
        #     )
        #     zap_api.pscan.set_scanner_alert_threshold(
        #         id=item,
        #         alertthreshold="OFF"
        #     )
        # if "all" not in scan_policies:
        #     # Disable all scanners first
        #     for item in zap_api.ascan.scanners(scan_policy_name):
        #         zap_api.ascan.set_scanner_alert_threshold(
        #             id=item["id"],
        #             alertthreshold="OFF",
        #             scanpolicyname=scan_policy_name
        #         )
        #     # Enable scanners from suite
        #     for policy in scan_policies:
        #         for item in c.ZAP_SCAN_POCILICES.get(policy, []):
        #             zap_api.ascan.set_scanner_alert_threshold(
        #                 id=item,
        #                 alertthreshold="DEFAULT",
        #                 scanpolicyname=scan_policy_name)
        # # Spider
        # logging.info("Spidering target: %s", target)
        # if config.get("auth_script", None):
        #     scan_id = zap_api.spider.scan_as_user(
        #         zap_context, zap_user, target, recurse=True, subtreeonly=True
        #     )
        # else:
        #     scan_id = zap_api.spider.scan(target)
        # _wait_for_completion(
        #     lambda: int(zap_api.spider.status(scan_id)) < 100,
        #     lambda: int(zap_api.spider.status(scan_id)),
        #     "Spidering progress: %d%%"
        # )
        # # Wait for passive scan
        # _wait_for_completion(
        #     lambda: int(zap_api.pscan.records_to_scan) > 0,
        #     lambda: int(zap_api.pscan.records_to_scan),
        #     "Passive scan queue: %d items"
        # )
        # # Ajax Spider
        # logging.info("Ajax spidering target: %s", target)
        # if config.get("auth_script", None):
        #     scan_id = zap_api.ajaxSpider.scan_as_user(
        #         zap_context_name, "dusty_user", target, subtreeonly=True
        #     )
        # else:
        #     scan_id = zap_api.ajaxSpider.scan(target)
        # _wait_for_completion(
        #     lambda: zap_api.ajaxSpider.status == 'running',
        #     lambda: int(zap_api.ajaxSpider.number_of_results),
        #     "Ajax spider found: %d URLs"
        # )
        # # Wait for passive scan
        # _wait_for_completion(
        #     lambda: int(zap_api.pscan.records_to_scan) > 0,
        #     lambda: int(zap_api.pscan.records_to_scan),
        #     "Passive scan queue: %d items"
        # )
        # # Active scan
        # logging.info("Active scan against target %s", target)
        # if config.get("auth_script", None):
        #     scan_id = zap_api.ascan.scan_as_user(
        #         target, zap_context, zap_user, recurse=True,
        #         scanpolicyname=scan_policy_name
        #     )
        # else:
        #     scan_id = zap_api.ascan.scan(
        #         target,
        #         scanpolicyname=scan_policy_name
        #     )
        # _wait_for_completion(
        #     lambda: int(zap_api.ascan.status(scan_id)) < 100,
        #     lambda: int(zap_api.ascan.status(scan_id)),
        #     "Active scan progress: %d%%"
        # )
        # # Wait for passive scan
        # _wait_for_completion(
        #     lambda: int(zap_api.pscan.records_to_scan) > 0,
        #     lambda: int(zap_api.pscan.records_to_scan),
        #     "Passive scan queue: %d items"
        # )
        # # Get report
        # logging.info("Scan finished. Processing results")
        # zap_report = zap_api.core.jsonreport()
        # if os.environ.get("debug", False):
        #     with open("/tmp/zap.json", "wb") as report_file:
        #         report_file.write(zap_report.encode("utf-8"))
        # # Stop zap
        # zap_daemon.kill()
        # zap_daemon.wait()
        # # Parse JSON
        # results.extend(ZapJsonParser(zap_report, tool_name).items)
        # pkg_resources.cleanup_resources()
        # return tool_name, results

    # def _execute(self, config):
    #     """ Run the scanner """
    #     log.info("Starting")
    #     try:
    #         self._start_zap()
    #         self._create_zap_client()
    #         self._wait_zap_start()
    #         #
    #         target = "{}://{}".format(
    #             config.get("protocol"),
    #             config.get("host"),
    #         )
    #         proto = config.get("protocol")
    #         port = config.get("port")
    #         if (proto == "http" and int(port) != 80) or \
    #                 (proto == "https" and int(port) != 443):
    #             target = f"{target}:{port}"
    #         log.info("Using target %s", target)
    #         #
    #         raise RuntimeError("Error")
    #     except:
    #         log.exception("Error during ZAP scanning")
    #     try:
    #         pass
    #     except:
    #         log.exception("Error during ZAP finalizing")
    #     finally:
    #         self._stop_zap()

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

    # def _start_zap(self):
    #     log.info("Starting ZAP daemon")
    #     self._zap_daemon = subprocess.Popen([
    #         "/usr/bin/java", "-Xmx499m",
    #         "-jar",
    #         "".join([
    #             "/Users/lifedjik",
    #             "/Vault/Projects/Job/EPAM/zap",
    #             "/ZAP_D-2019-02-25/zap-D-2019-02-25.jar"
    #         ]),
    #         "-daemon", "-port", "8091", "-host", "0.0.0.0",
    #         "-config", "api.key=dusty",
    #         "-config", "api.addrs.addr.regex=true",
    #         "-config", "api.addrs.addr.name=.*",
    #         "-config", "ajaxSpider.browserId=htmlunit"
    #     ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # def _stop_zap(self):
    #     if self._zap_daemon is not None:
    #         log.info("Stopping ZAP daemon")
    #         self._zap_daemon.kill()
    #         self._zap_daemon.wait()
    #         self._zap_daemon = None

    # def _create_zap_client(self):
    #     self._zap = ZAPv2(
    #         apikey="dusty",
    #         proxies={
    #             "http": "http://127.0.0.1:8091",
    #             "https": "http://127.0.0.1:8091"
    #         }
    #     )

    # def _wait_zap_start(self):
    #     zap_started = False
    #     for _ in range(600):
    #         try:
    #             log.info("Started ZAP %s", self._zap.core.version)
    #             zap_started = True
    #             break
    #         except IOError:
    #             time.sleep(1)
    #     if not zap_started:
    #         raise RuntimeError("ZAP failed to start")

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
        return "OWASP ZAP"

    @staticmethod
    def get_description():
        """ Module description or help message """
        return "OWASP Zed Attack Proxy (ZAP)"
