#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# See LICENSE.txt included in this distribution for the specific
# language governing permissions and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at LICENSE.txt.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright (c) 2018, Oracle and/or its affiliates. All rights reserved.
#

from ..utils.command import Command
from .repository import Repository
from shutil import which


class CVSRepository(Repository):
    def __init__(self, logger, path, project, command, env, hooks, timeout):

        super().__init__(logger, path, project, command, env, hooks, timeout)

        if command:
            self.command = command
        else:
            self.command = which("cvs")

        if not self.command:
            self.logger.error("Cannot get cvs command")
            raise OSError

    def reposync(self):
        hg_command = [self.command, "update", "-dP"]
        cmd = self.getCommand(hg_command, work_dir=self.path,
                              env_vars=self.env, logger=self.logger)
        cmd.execute()
        self.logger.info(cmd.getoutputstr())
        if cmd.getretcode() != 0 or cmd.getstate() != Command.FINISHED:
            self.logger.error("failed to perform update: command {}"
                              "in directory {} exited with {}".
                              format(hg_command, self.path, cmd.getretcode()))
            return 1

        return 0
