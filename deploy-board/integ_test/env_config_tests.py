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
import unittest
import commons
import json

builds_helper = commons.get_build_helper()
environs_helper = commons.get_environ_helper()
systems_helper = commons.get_system_helper()
schedules_helper = commons.get_schedule_helper()


class TestEnvirons(unittest.TestCase):
    envName = ""
    stageName = ""

    @classmethod
    def setUpClass(cls):
        cls.envName = f"test-config-{commons.gen_random_num()}"
        cls.stageName = "prod"
        data = {
            "description": """foo's \"big deal\".""",
            "envName": cls.envName,
            "stageName": cls.stageName,
        }

        environs_helper.create_env(commons.REQUEST, data)

    @classmethod
    def tearDownClass(cls):
        environs_helper.delete_env(commons.REQUEST, cls.envName, cls.stageName)

    def testGets(self):
        stages = environs_helper.get_all_env_stages(commons.REQUEST, TestEnvirons.envName)
        self.assertTrue(len(stages) == 1)

        names = environs_helper.get_all_env_names(commons.REQUEST, index=1, size=1)
        self.assertTrue(len(names) == 1)

    def testBasicConfigs(self):
        oldBuildName = environs_helper.get_env_by_stage(commons.REQUEST, TestEnvirons.envName,
                                                        TestEnvirons.stageName)['buildName']
        self.assertEquals(oldBuildName, TestEnvirons.envName)
        environs_helper.update_env_basic_config(commons.REQUEST, TestEnvirons.envName,
                                                TestEnvirons.stageName, {"buildName": "foo"})
        newBuildName = environs_helper.get_env_by_stage(commons.REQUEST, TestEnvirons.envName,
                                                        TestEnvirons.stageName)['buildName']
        self.assertEquals(newBuildName, "foo")

    def testCapacityConfigs(self):
        hosts = environs_helper.get_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                                 TestEnvirons.stageName, capacity_type="HOST")
        self.assertEquals(len(hosts), 0)
        groups = environs_helper.get_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                                  TestEnvirons.stageName, capacity_type="GROUP")
        self.assertEquals(len(groups), 0)
        hosts = ["host1", "host2"]
        groups = ["group"]
        environs_helper.update_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                            TestEnvirons.stageName, capacity_type="HOST",
                                            data=hosts)
        environs_helper.update_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                            TestEnvirons.stageName, data=groups)
        new_hosts = environs_helper.get_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                                     TestEnvirons.stageName, capacity_type="HOST")
        self.assertEquals(hosts, new_hosts)
        new_groups = environs_helper.get_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                                      TestEnvirons.stageName)
        self.assertEquals(groups, new_groups)

        # delete them, otherwise we could not delete the environ
        hosts = []
        groups = []
        environs_helper.update_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                            TestEnvirons.stageName, capacity_type="HOST",
                                            data=hosts)
        environs_helper.update_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                            TestEnvirons.stageName, data=groups)
        new_hosts = environs_helper.get_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                                     TestEnvirons.stageName, capacity_type="HOST")
        self.assertEquals(len(new_hosts), 0)
        new_groups = environs_helper.get_env_capacity(commons.REQUEST, TestEnvirons.envName,
                                                      TestEnvirons.stageName)
        self.assertEquals(len(new_groups), 0)

    def testAdvancedConfigs(self):
        oldConfigs = environs_helper.get_env_agent_config(commons.REQUEST, TestEnvirons.envName,
                                                          TestEnvirons.stageName)
        self.assertTrue(len(oldConfigs) == 0)

        # firsttime, should be a create
        configs = {"foo1": "bar1", "foo2": "bar2"}
        environs_helper.update_env_agent_config(commons.REQUEST, TestEnvirons.envName,
                                                TestEnvirons.stageName, configs)
        newConfigs = environs_helper.get_env_agent_config(commons.REQUEST, TestEnvirons.envName,
                                                          TestEnvirons.stageName)
        self.assertEquals(configs, newConfigs)

        configs = {"foo1": "bar2", "foo3": "bar3"}
        environs_helper.update_env_agent_config(commons.REQUEST, TestEnvirons.envName,
                                                TestEnvirons.stageName, configs)
        newConfigs = environs_helper.get_env_agent_config(commons.REQUEST, TestEnvirons.envName,
                                                          TestEnvirons.stageName)
        self.assertEquals(configs, newConfigs)

    def testScriptConfigs(self):
        oldConfigs = environs_helper.get_env_script_config(commons.REQUEST, TestEnvirons.envName,
                                                           TestEnvirons.stageName)
        self.assertTrue(len(oldConfigs) == 0)

        configs = {"foo1": "bar1", "foo2": "bar2"}
        environs_helper.update_env_script_config(commons.REQUEST, TestEnvirons.envName,
                                                 TestEnvirons.stageName, configs)
        newConfigs = environs_helper.get_env_script_config(commons.REQUEST, TestEnvirons.envName,
                                                           TestEnvirons.stageName)
        self.assertEquals(configs, newConfigs)

        configs = {"foo1": "bar2", "foo3": "bar3"}
        environs_helper.update_env_script_config(commons.REQUEST, TestEnvirons.envName,
                                                 TestEnvirons.stageName, configs)
        newConfigs = environs_helper.get_env_script_config(commons.REQUEST, TestEnvirons.envName,
                                                           TestEnvirons.stageName)
        self.assertEquals(configs, newConfigs)

    def testAlarmsConfigs(self):
        oldAlarms = environs_helper.get_env_alarms_config(commons.REQUEST, TestEnvirons.envName,
                                                          TestEnvirons.stageName)
        self.assertTrue(len(oldAlarms) == 0)

        newAlarm = {
            'name': "alarm1",
            'alarmUrl': "www1.pinterest1.com",
            'metricsUrl': "www2.pinterest1.com",
        }

        alarms = [newAlarm]
        environs_helper.update_env_alarms_config(commons.REQUEST, TestEnvirons.envName,
                                                 TestEnvirons.stageName, alarms)
        newAlarms = environs_helper.get_env_alarms_config(commons.REQUEST, TestEnvirons.envName,
                                                          TestEnvirons.stageName)
        self.assertEquals(alarms, newAlarms)

        newAlarm = {
            'name': "alarm2",
            'alarmUrl': "www2.pinterest1.com",
            'metricsUrl': "www2.pinterest1.com",
        }

        alarms.append(newAlarm)
        environs_helper.update_env_alarms_config(commons.REQUEST, TestEnvirons.envName,
                                                 TestEnvirons.stageName, alarms)
        newAlarms = environs_helper.get_env_alarms_config(commons.REQUEST, TestEnvirons.envName,
                                                          TestEnvirons.stageName)
        self.assertEquals(alarms, newAlarms)

    def testMetricsConfigs(self):
        oldMetrics = environs_helper.get_env_metrics_config(commons.REQUEST, TestEnvirons.envName,
                                                            TestEnvirons.stageName)
        self.assertTrue(len(oldMetrics) == 0)

        metSpec = {"color": "blue", "min": 0, "max": 98}
        metSpecs = [metSpec]
        metSpec["color"] = "green"
        metSpec["min"] = 99
        metSpec["max"] = 100
        metSpecs.append(metSpec)

        metConfig = {
            "title": "TestTitle",
            "url": "www.pinterest.com",
            "specs": metSpecs,
        }

        metrics = [metConfig]
        environs_helper.update_env_metrics_config(commons.REQUEST, TestEnvirons.envName,
                                                  TestEnvirons.stageName, metrics)
        newMetrics = environs_helper.get_env_metrics_config(commons.REQUEST, TestEnvirons.envName,
                                                            TestEnvirons.stageName)
        self.assertEquals(metrics, newMetrics)

        metSpec["color"] = "blue"
        metSpec["min"] = 1
        metSpec["max"] = 2
        metSpecs.append(metSpec)

        metConfig["title"] = "TestTitle2"
        metConfig["url"] = "www.pinterest2.com"
        metConfig["specs"] = metSpecs
        metrics.append(metConfig)

        environs_helper.update_env_metrics_config(commons.REQUEST, TestEnvirons.envName,
                                                  TestEnvirons.stageName, metrics)
        newMetrics = environs_helper.get_env_metrics_config(commons.REQUEST, TestEnvirons.envName,
                                                            TestEnvirons.stageName)
        self.assertEquals(metrics, newMetrics)

    def testHooksConfigs(self):
        oldHooks = environs_helper.get_env_hooks_config(commons.REQUEST, TestEnvirons.envName,
                                                        TestEnvirons.stageName)
        self.assertTrue(oldHooks["preDeployHooks"] is None)

        newHook = {
            'method': "GET",
            'url': "www1.pinterest1.com",
            'version': "HTTP/1.1",
            'headers': None,
            'body': None,
        }

        hooks = {"preDeployHooks": [newHook], "postDeployHooks": [newHook]}
        environs_helper.update_env_hooks_config(commons.REQUEST, TestEnvirons.envName,
                                                TestEnvirons.stageName, hooks)
        newHooks = environs_helper.get_env_hooks_config(commons.REQUEST, TestEnvirons.envName,
                                                        TestEnvirons.stageName)
        self.assertEquals(hooks, newHooks)

        newHook = {
            'method': "POST",
            'url': "www1.pinterest1.com",
            'version': None,
            'headers': None,
            'body': None,
        }

        newHooks2 = [newHook]
        newHook['method'] = "POST"
        newHook['url'] = "www1.pinterest1.com"
        newHook['version'] = None
        newHook['headers'] = None
        newHook['body'] = None

        newHooks2.append(newHook)
        hooks["postDeployHooks"] = newHooks2
        environs_helper.update_env_hooks_config(commons.REQUEST, TestEnvirons.envName,
                                                TestEnvirons.stageName, hooks)
        newHooks = environs_helper.get_env_hooks_config(commons.REQUEST, TestEnvirons.envName,
                                                        TestEnvirons.stageName)
        self.assertEquals(hooks, newHooks)

    def testScheduleConfigs(self):
        schedule = {
            "cooldownTimes": "20,30,40",
            "hostNumbers": "30,50,70",
            "totalSessions": 3,
        }

        schedules_helper.update_schedule(commons.REQUEST, TestEnvirons.envName, TestEnvirons.stageName, schedule)

        scheduleId = environs_helper.get_env_by_stage(commons.REQUEST, TestEnvirons.envName,
                                                        TestEnvirons.stageName)['scheduleId']
        envSchedule = schedules_helper.get_schedule(commons.REQUEST, TestEnvirons.envName, TestEnvirons.stageName, scheduleId)

        newSchedule = {
            'cooldownTimes': '20,30,40',
            'hostNumbers': '30,50,70',
            'totalSessions': 3,
            'state': 'NOT_STARTED',
            'id': scheduleId,
            'currentSession': 0,
            'stateStartTime': envSchedule[u'stateStartTime'],
        }

        self.assertEquals(newSchedule, envSchedule)

if __name__ == '__main__':
    unittest.main()
