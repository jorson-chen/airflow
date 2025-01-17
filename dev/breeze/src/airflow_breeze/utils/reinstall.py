# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import subprocess
import sys
from pathlib import Path

from airflow_breeze import NAME
from airflow_breeze.utils.confirm import Answer, user_confirm
from airflow_breeze.utils.console import console


def reinstall_breeze(breeze_sources: Path):
    """
    Reinstalls Breeze from specified sources.
    :param breeze_sources: Sources where to install Breeze from.
    """
    # Note that we cannot use `pipx upgrade` here because we sometimes install
    # Breeze from different sources than originally installed (i.e. when we reinstall airflow
    # From the current directory.
    console.print(f"\n[bright_blue]Reinstalling Breeze from {breeze_sources}\n")
    subprocess.check_call(
        [
            "pipx",
            "install",
            "-e",
            str(breeze_sources),
            "--force",
            "--pip-args=--upgrade",
            "--pip-args=--upgrade-strategy=eager",
        ]
    )
    console.print(
        f"\n[bright_blue]Breeze has been reinstalled from {breeze_sources}. Exiting now.[/]\n\n"
        f"[bright_yellow]Please run your command again[/]\n"
    )
    sys.exit(0)


def ask_to_reinstall_breeze(breeze_sources: Path):
    """
    Ask the user to reinstall Breeze (and do so if confirmed).
    :param breeze_sources: breeze sources to reinstall Breeze from.
    """
    answer = user_confirm(
        f"Do you want to reinstall Breeze from {breeze_sources.parent.parent}?",
        timeout=3,
        default_answer=Answer.NO,
    )
    if answer == Answer.YES:
        reinstall_breeze(breeze_sources)
    elif answer == Answer.QUIT:
        sys.exit(1)


def warn_non_editable():
    console.print(
        "\n[red]Breeze is installed in a wrong way.[/]\n"
        "\n[red]It should only be installed in editable mode[/]\n\n"
        "[bright_yellow]Please go to Airflow sources and run[/]\n\n"
        f"     {NAME} self-upgrade --force --use-current-airflow-sources\n"
    )


def warn_different_location(installation_airflow_sources: Path, current_airflow_sources: Path):
    console.print(
        f"\n[bright_yellow]WARNING! Breeze was installed from "
        f"different location![/]\n\n"
        f"Breeze installed from   : {installation_airflow_sources}\n"
        f"Current Airflow sources : {current_airflow_sources}\n\n"
        f"[bright_yellow]This might cause various problems!![/]\n\n"
        f"If you experience problems - reinstall Breeze with:\n\n"
        f"    {NAME} self-upgrade --force --use-current-airflow-sources\n\n"
    )


def warn_dependencies_changed():
    console.print(
        f"\n[bright_yellow]WARNING! Breeze dependencies changed since the installation![/]\n\n"
        f"[bright_yellow]This might cause various problems!![/]\n\n"
        f"If you experience problems - reinstall Breeze with:\n\n"
        f"    {NAME} self-upgrade --force\n\n"
    )
