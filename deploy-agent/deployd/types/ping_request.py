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
from deployd.types.deploy_stage import DeployStage
from deployd.types.agent_status import AgentStatus


class PingRequest(object):

    def __init__(self, hostId=None, hostName=None, hostIp=None, groups=None, reports=None,
                agentVersion=None, autoscalingGroup=None, availabilityZone=None, stageType=None):
        self.hostId = hostId
        self.hostName = hostName
        self.hostIp = hostIp
        self.groups = groups
        self.reports = reports
        self.agentVersion = agentVersion
        self.autoscalingGroup = autoscalingGroup
        self.availabilityZone = availabilityZone
        self.stageType = stageType

    def to_json(self):
        ping_requests = {
            "hostId": self.hostId,
            "hostName": self.hostName,
            "hostIp": self.hostIp,
        }

        if self.autoscalingGroup:
            ping_requests["autoscalingGroup"] = self.autoscalingGroup
        if self.availabilityZone:
            ping_requests["availabilityZone"] = self.availabilityZone
        if self.agentVersion:
            ping_requests["agentVersion"] = self.agentVersion
        if self.stageType:
            ping_requests["stageType"] = self.stageType
        if self.groups:
            ping_requests["groups"] = list(self.groups)
        ping_requests["reports"] = []
        for report in self.reports:
            ping_report = {
                "deployId": report.deployId,
                "envId": report.envId,
                "deployStage": DeployStage._VALUES_TO_NAMES[report.deployStage]
                if isinstance(report.deployStage, int)
                else report.deployStage,
                "agentStatus": AgentStatus._VALUES_TO_NAMES[report.status]
                if isinstance(report.status, int)
                else report.status,
                "errorCode": report.errorCode,
                "errorMessage": report.errorMessage,
                "failCount": report.failCount,
                "deployAlias": report.deployAlias,
            }

            if report.extraInfo:
                ping_report["extraInfo"] = \
                        json.dumps(report.extraInfo, ensure_ascii=False).encode('utf8')
            ping_requests["reports"].append(ping_report)
        return ping_requests

    def __str__(self):
        return f'PingRequest(hostId={self.hostId}, hostName={self.hostName}, hostIp={self.hostIp}, agentVersion={self.agentVersion}, autoscalingGroup={self.autoscalingGroup}, availabilityZone={self.availabilityZone}, stageType={self.stageType}, groups={self.groups}, reports={",".join((str(v) for v in self.reports))})'
