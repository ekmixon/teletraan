# Copyright 2016 Pinterest, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  
#     http://www.apache.org/licenses/LICENSE-2.0
#    
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import lockfile
import os
import traceback

from deployd import IS_PINTEREST
from deployd.common.types import DeployStatus
from deployd.common.utils import touch

log = logging.getLogger(__name__)


class EnvStatus(object):

    def __init__(self, status_fn):
        self._status_fn = status_fn
        self._lock_fn = f'{self._status_fn}.lock'
        self._lock = lockfile.FileLock(self._lock_fn)

    def load_envs(self):
        """
        open up config file
        validate that the service selected exists
        """
        envs = {}
        try:
            with self._lock, open(self._status_fn, 'r+') as config_fn:
                data = json.load(config_fn)
                log.debug(f'load status file: {data}')
                envs = {key: DeployStatus(json_value=d) for key, d in data.items()}
        except IOError:
            log.info(
                f"Could not find file {self._status_fn}. It happens when run deploy-agent the first time, or there is no deploy yet."
            )

            return {}
        except Exception:
            log.exception("Something went wrong in load_envs")
        finally:
            return envs

    def _touch_or_rm_host_type_file(self, envs, host_type, directory='/var/run/'):
        """Touches or removes the identity file for the host type.
        For now, a host type could be 'canary'.
        """
        file_path = os.path.join(directory, host_type)
        host_type_match = any(
            value.report.stageName == host_type for key, value in envs.items()
        )

        if host_type_match:
            log.debug(f'The host is a {host_type}.')
            if not os.path.isfile(file_path):
                touch(file_path)
                log.debug(f'Touched {file_path}.')
        else:
            log.debug(f'The host is not a {host_type}.')
            if os.path.isfile(file_path):
                os.remove(file_path)
                log.debug(f'Removed {file_path}.')

    def dump_envs(self, envs):
        try:
            json_data = {}
            if envs:
                json_data = {key: value.to_json() for key, value in envs.items()}
            with self._lock, open(self._status_fn, 'w') as config_output:
                json.dump(json_data, config_output, sort_keys=True,
                          indent=2, separators=(',', ': '))

            if IS_PINTEREST:
                self._touch_or_rm_host_type_file(envs, "canary")
            return True
        except IOError as e:
            log.warning(f"Could not write to {self._status_fn}. Reason: {e}")
            return False
        except Exception:
            log.error(traceback.format_exc())
            return False
