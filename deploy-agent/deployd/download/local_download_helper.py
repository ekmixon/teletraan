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

from deployd.common.caller import Caller
from deployd.download.download_helper import DownloadHelper
from deployd.common.status_code import Status
import logging
import os

log = logging.getLogger(__name__)


class LocalDownloadHelper(DownloadHelper):

    def _download_files(self, local_full_fn):
        download_cmd = ['curl', '-o', local_full_fn, '-ks', self._url]
        log.info(f"Running command: {' '.join(download_cmd)}")
        error_code = Status.SUCCEEDED
        output, error, status = Caller.call_and_log(download_cmd, cwd=os.getcwd())
        if output:
            log.info(output)
        if error:
            log.error(error)
        if status:
            error_code = Status.FAILED
        log.info(f'Finished downloading: {self._url} to {local_full_fn}')
        return error_code

    def download(self, local_full_fn):
        log.info(f"Start to download from local path {self._url} to {local_full_fn}")

        error = self._download_files(local_full_fn)
        if error != Status.SUCCEEDED:
            log.error(f'Failed to download the local tar ball for {local_full_fn}')
        return error
