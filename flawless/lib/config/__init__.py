#!/usr/bin/env python
#
# Copyright (c) 2011-2013, Shopkick Inc.
# All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# ---
# Author: John Egan <john@shopkick.com>

import collections
import ConfigParser
import os.path

FlawlessOption = collections.namedtuple("FlawlessOption", ["name", "default", "type", "description"])

OPTIONS = [
  # Hostnames & ports
  FlawlessOption("port", 9028, int, "The port to listen on"),
  FlawlessOption("hostname", "localhost", str,
                 "The host:port to connect to for the flawless backend service. This is used for "
                 "generating URLs in the emails that are sent out"),

  # Email domain name
  FlawlessOption("email_domain_name", "example.com", str, "Domain name used to send emails"),
  FlawlessOption("ignore_vcs_email_domain", False, bool,
                 "Version control systems sometimes report bogus email domains, set this if"
                 "the email domain from the version control system should be ignored and if"
                 "email_domain_name should be used instead"),

  # SMTP host setup
  FlawlessOption("smtp_host", "localhost:25", str, "The host responsbile for sending email"),
  FlawlessOption("smtp_user", None, str, "Username for smtp server (if required)"),
  FlawlessOption("smtp_password", None, str, "Password for smtp server (if required)"),

  # Directory paths
  FlawlessOption("data_dir_path", "/tmp/", str, "Path to where flawless can store state to disk"),
  FlawlessOption("config_dir_path", None, str, "Path to where flawless config files can be found"),

  # Control when errors get reported
  FlawlessOption("report_runtime_package_directory_name", "site-packages", str,
                 "The site-packages directory name"),
  FlawlessOption("report_only_after_minimum_date", "1970-1-1", str,
                 "Ignore errors occurring in old code that was last modified prior to this date"),
  FlawlessOption("report_error_threshold", 3, int,
                 "Number of times an error should occur before generating an alert"),
  FlawlessOption("report_exclude_filepaths_containing", "", lambda s: s.split(","),
                 "When assigning blame to a file, you can explicity prevent blame from "
                 "getting assigned to files whose filepath matches any pattern on this CSV list"),
  FlawlessOption("report_include_filepaths_containing", "", lambda s: s.split(","),
                 "Only use this in conjunction with report_exclude_filepaths_containing. If a "
                 "file whose filepath matches a pattern on this CSV list, then it will be eligible "
                 "for being blamed, even if it also matches a parttern on "
                 "report_exclude_filepaths_containing"),

  # Repository info
  FlawlessOption("git_cli_path", "git", str, "Path to the git command line utility"),
  FlawlessOption("repo_type", "git", str, "Options: git"),
  FlawlessOption("repo_dir", "/tmp/flawless_repo", str, "The path to the repo directory"),
  FlawlessOption("repo_url", None, str, "URL of the remote repo, including username and "
                 "password credentials"),
  FlawlessOption("repo_branch_pattern", None, str, "Regular expressions to identify release branches"),

  # Client settings
  FlawlessOption("flawless_hostport", None, str, "Host:port of the flawless backend"),
  FlawlessOption("client_timeout", 10, int, "The number of seconds before requests should timeout"),

  # Logging
  FlawlessOption("log_level", "INFO", str, "The logging level"),
]


class FlawlessConfig(object):
  def __init__(self, dict):
    self.__dict__ = dict

  def __str__(self):
    return str(self.__dict__)


RUNTIME_CONFIG = FlawlessConfig(
    dict((o.name, o.type(o.default) if o.default is not None else None) for o in OPTIONS)
)


default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../config/flawless.cfg"))

def get():
  return RUNTIME_CONFIG


def init_config(filepath):
  setattr(RUNTIME_CONFIG, "config_dir_path", os.path.dirname(filepath))
  parser = ConfigParser.SafeConfigParser()
  parser.read(filepath)
  for option in OPTIONS:
    if parser.has_option("flawless", option.name):
      value = parser.get("flawless", option.name)
      setattr(RUNTIME_CONFIG, option.name, option.type(value))


