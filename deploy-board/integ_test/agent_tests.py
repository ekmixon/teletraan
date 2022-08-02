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

# -*- coding: utf-8 -*-
'''
This is a positive ping test to go through a success deploy
'''

import unittest
import time
import commons
import threading

systems_helper = commons.get_system_helper()
environs_helper = commons.get_environ_helper()
deploys_helper = commons.get_deploy_helper()
envName = f"agent-test-env-{commons.gen_random_num()}"
stageName = "prod"
commit = commons.gen_random_num(32)
hostNamePrefix = "agent-test-host-"
group = f"agent-test-group-{commons.gen_random_num()}"


class TestPings(unittest.TestCase):
    def setUp(self):
        commons.create_env(envName, stageName)
        environs_helper.update_env_capacity(commons.REQUEST, envName, stageName,
                                            data=[group])
        environs_helper.update_env_basic_config(commons.REQUEST, envName, stageName,
                                                {"maxParallel": 5})
        environs_helper.update_env_script_config(commons.REQUEST, envName, stageName,
                                                 {"s-c-n": "s-c-v"})
        environs_helper.update_env_agent_config(commons.REQUEST, envName, stageName,
                                                {"a-c-n": "a-c-v"})
        self.build = commons.publish_build("ping-test", "master", commit=commit)
        self.deploy = deploys_helper.deploy(commons.REQUEST, envName, stageName, self.build['id'])

    def tearDown(self):
        commons.delete_env(envName, stageName)
        commons.delete_build(self.build['id'])
        commons.delete_deploy(self.deploy['id'])

    def _empty_ping(self, idx, groups):
        host = hostNamePrefix + idx
        ip = f"{idx}.{idx}.{idx}.{idx}"
        pingRequest = {
            'hostId': host,
            'hostName': host,
            'hostIp': ip,
            'groups': groups,
            'reports': [],
        }

        systems_helper.ping(commons.REQUEST, pingRequest)

    def _ping(self, idx, groups):
        host = hostNamePrefix + idx
        ip = f"{idx}.{idx}.{idx}.{idx}"
        reports = {}

        while True:
            pingRequest = {
                'hostId': host,
                'hostName': host,
                'hostIp': ip,
                'groups': groups,
                'reports': reports.values(),
            }

            pingResponse = systems_helper.ping(commons.REQUEST, pingRequest)
            pingRequest['reports'] = reports.values()

            pingResponse = systems_helper.ping(commons.REQUEST, pingRequest)
            if pingResponse['opCode'] == "NOOP":
                continue
            goal = pingResponse['deployGoal']
            report = {
                'envId': goal['envId'],
                'deployId': goal['deployId'],
                'agentStatus': "SUCCEEDED",
                'deployStage': goal['deployStage'],
            }

            reports[goal['envId']] = report

            # verifications
            if goal['deployStage'] == 'DOWNLOADING':
                self.assertEquals(goal['build']['commit'], commit)
            if goal['deployStage'] == 'PRE_DOWNLOAD':
                self.assertEquals(goal['scriptVariables']['s-c-n'], 's-c-v')
            self.assertEquals(goal['agentConfigs']['a-c-n'], 'a-c-v')

            if goal['deployStage'] == 'SERVING_BUILD':
                return

    def _check_deploy_complete(self):
        env = environs_helper.get_env_by_stage(commons.REQUEST, envName, stageName)
        deploy = deploys_helper.get(commons.REQUEST, env["deployId"])
        if deploy['state'] == 'SUCCEEDING':
            print "Deploy has compelted successfully!"
            return True
        print "Deploy has not compelted yet, success rate is %d/%d" % (deploy['successTotal'],
                                                                       deploy['total'])
        return False

    def test_pings(self):
        n = 10
        groups = [group]
        for x in xrange(n):
            self._empty_ping(str(x), groups)

        threads = []
        for x in xrange(n):
            t = threading.Thread(target=self._ping, args=(str(x), groups))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        while not self._check_deploy_complete():
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
