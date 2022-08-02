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

from deploy_board.webapp.helpers.rodimus_client import RodimusClient

rodimus_client = RodimusClient()


TerminationPolicy = ["Default", "OldestInstance", "NewestInstance", "OldestLaunchConfiguration",
                     "ClosestToNextInstanceHour"]

Comparator = ["GreaterThanOrEqualToThreshold", "GreaterThanThreshold", "LessThanOrEqualToThreshold",
              "LessThanThreshold"]


#
# Groups resource
#
def get_env_group_names(request, start, size):
    params = {"start": start, "size": size}
    return rodimus_client.get("/groups/names", request.teletraan_user_id.token, params=params)


def create_launch_config(request, group_name, asg_info):
    return rodimus_client.post(
        f"/groups/{group_name}", request.teletraan_user_id.token, data=asg_info
    )


def update_launch_config(request, group_name, asg_info):
    return rodimus_client.put(
        f"/groups/{group_name}", request.teletraan_user_id.token, data=asg_info
    )


def update_group_info(request, group_name, group_info):
    return rodimus_client.put(
        f"/groups/{group_name}/config",
        request.teletraan_user_id.token,
        data=group_info,
    )


def get_group_info(request, group_name):
    return rodimus_client.get(
        f"/groups/{group_name}", request.teletraan_user_id.token
    )


def launch_hosts(request, group_name, host_count, subnet):
    params = {"hostCount": host_count, "subnet": subnet}
    return rodimus_client.put(
        f"/groups/{group_name}/hosts",
        request.teletraan_user_id.token,
        params=params,
    )


def launch_hosts_with_placement_group(request, group_name, host_count, subnet, placement_group):
    data = {"hostCount": host_count,
            "cloudLaunchConfig": {"subnet": subnet, "placementGroup": placement_group}}

    # Note: this sends a post request while above sends a put
    return rodimus_client.post(
        f"/groups/{group_name}/hosts",
        request.teletraan_user_id.token,
        data=data,
    )


def terminate_all_hosts(request, group_name):
    return rodimus_client.delete(
        f"/groups/{group_name}/terminate/all", request.teletraan_user_id.token
    )


# Health Checks
def create_health_check(request, group_name, health_check_info):
    return rodimus_client.post(
        f"/groups/{group_name}/healthcheck",
        request.teletraan_user_id.token,
        data=health_check_info,
    )


def enable_health_check(request, group_name):
    params = [('actionType', 'ENABLE')]
    return rodimus_client.post(
        f"/groups/{group_name}/healthcheck/action",
        request.teletraan_user_id.token,
        params=params,
    )


def disable_health_check(request, group_name):
    params = [('actionType', 'DISABLE')]
    return rodimus_client.post(
        f"/groups/{group_name}/healthcheck/action",
        request.teletraan_user_id.token,
        params=params,
    )


def get_health_check_activities(request, group_name, index, size):
    params = [('pageIndex', index), ('pageSize', size)]
    return rodimus_client.get(
        f"/groups/{group_name}/healthchecks/",
        request.teletraan_user_id.token,
        params=params,
    )


def get_health_check(request, id):
    return rodimus_client.get(
        f"/groups/healthchecks/{id}", request.teletraan_user_id.token
    )


def get_health_check_error(request, id):
    return rodimus_client.get(
        f"/groups/healthchecks/errors/{id}", request.teletraan_user_id.token
    )


# Config history
def get_config_history(request, group_name, index, size):
    params = [('pageIndex', index), ('pageSize', size)]
    return rodimus_client.get(
        f"/groups/{group_name}/configs/history/",
        request.teletraan_user_id.token,
        params=params,
    )


#
# AutoScalingGroups resource
#
def create_autoscaling(request, cluster_name, asg_info):
    return rodimus_client.post(
        f"/clusters/{cluster_name}/autoscaling",
        request.teletraan_user_id.token,
        data=asg_info,
    )


def update_autoscaling(request, cluster_name, asg_info):
    return rodimus_client.put(
        f"/clusters/{cluster_name}/autoscaling",
        request.teletraan_user_id.token,
        data=asg_info,
    )


def delete_autoscaling(request, cluster_name, detach_host):
    params = [('detachHosts', detach_host)]
    return rodimus_client.delete(
        f"/clusters/{cluster_name}/autoscaling",
        request.teletraan_user_id.token,
        params=params,
    )


def get_autoscaling(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling",
        request.teletraan_user_id.token,
    )


def get_autoscaling_summary(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/summary",
        request.teletraan_user_id.token,
    )


# Asg Actions
def get_autoscaling_status(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/status",
        request.teletraan_user_id.token,
    )


def enable_autoscaling(request, cluster_name):
    params = [('actionType', 'ENABLE')]
    return rodimus_client.post(
        f"/clusters/{cluster_name}/autoscaling/action",
        request.teletraan_user_id.token,
        params=params,
    )


def disable_autoscaling(request, cluster_name):
    params = [('actionType', 'DISABLE')]
    return rodimus_client.post(
        f"/clusters/{cluster_name}/autoscaling/action",
        request.teletraan_user_id.token,
        params=params,
    )


def disable_scaling_down_event(request, cluster_name):
    params = [('actionType', 'DISABLE_TERMINATE')]
    return rodimus_client.post(
        f"/clusters/{cluster_name}/autoscaling/action",
        request.teletraan_user_id.token,
        params=params,
    )


def get_disabled_asg_actions(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/action",
        request.teletraan_user_id.token,
    )


# Asg Alarms
def put_scaling_policies(request, cluster_name, policies_info):
    return rodimus_client.post(
        f"/clusters/{cluster_name}/autoscaling/policies",
        request.teletraan_user_id.token,
        data=policies_info,
    )


def get_policies(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/policies",
        request.teletraan_user_id.token,
    )


def add_alarm(request, cluster_name, alarm_infos):
    return rodimus_client.post(
        f"/clusters/{cluster_name}/autoscaling/alarms",
        request.teletraan_user_id.token,
        data=alarm_infos,
    )


def update_alarms(request, cluster_name, alarm_infos):
    return rodimus_client.put(
        f"/clusters/{cluster_name}/autoscaling/alarms",
        request.teletraan_user_id.token,
        data=alarm_infos,
    )


def get_alarms(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/alarms",
        request.teletraan_user_id.token,
    )


def delete_alarm(request, cluster_name, alarm_id):
    return rodimus_client.delete(
        f"/clusters/{cluster_name}/autoscaling/alarms/{alarm_id}",
        request.teletraan_user_id.token,
    )


def get_alarm_state(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/alarmstate",
        request.teletraan_user_id.token,
    )


def get_system_metrics(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/metrics/system",
        request.teletraan_user_id.token,
    )


# Asg Schedules
def add_scheduled_actions(request, cluster_name, schedule_actions):
    return rodimus_client.post(
        f"/clusters/{cluster_name}/autoscaling/schedules",
        request.teletraan_user_id.token,
        data=schedule_actions,
    )


def delete_scheduled_action(request, cluster_name, action_id):
    return rodimus_client.delete(
        f"/clusters/{cluster_name}/autoscaling/schedules/{action_id}",
        request.teletraan_user_id.token,
    )


def get_scheduled_actions(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/schedules",
        request.teletraan_user_id.token,
    )


# Scaling activities
def get_scaling_activities(request, cluster_name, page_size, token):
    params = {"size": page_size, "token": token}
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/activities",
        request.teletraan_user_id.token,
        params=params,
    )


# pas
def update_pas_config(request, cluster_name, pas_config):
    return rodimus_client.put(
        f"/clusters/{cluster_name}/autoscaling/pas",
        request.teletraan_user_id.token,
        data=pas_config,
    )


def get_pas_config(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/pas",
        request.teletraan_user_id.token,
    )


# hosts
# TODO no usage
def get_autoscaling_group_hosts(request, cluster_name):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/hosts",
        request.teletraan_user_id.token,
    )


def hosts_action_in_group(request, cluster_name, host_ids, action):
    params = {"actionType": action}
    return rodimus_client.post(
        f"/clusters/{cluster_name}/autoscaling/hosts/action",
        request.teletraan_user_id.token,
        params=params,
        data=host_ids,
    )


def is_hosts_protected(request, cluster_name, host_ids):
    return rodimus_client.get(
        f"/clusters/{cluster_name}/autoscaling/host/protection",
        request.teletraan_user_id.token,
        data=host_ids,
    )
