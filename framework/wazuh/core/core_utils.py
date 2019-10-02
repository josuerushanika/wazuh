# Copyright (C) 2015-2019, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2

from wazuh.agent import WazuhDBQueryAgents, WazuhDBQueryMultigroups


def get_agents_info():
    agents = WazuhDBQueryAgents(select=['id']).run()['items']
    agents_list = set()
    for agent_info in agents:
        agents_list.add(str(agent_info['id']).zfill(3))

    return agents_list


def expand_group(group_name):
    if group_name == '*':
        data = WazuhDBQueryAgents(select=['group']).run()['items']
        groups = set()
        for agent_group in data:
            groups.update(set(agent_group.get('group', list())))
    else:
        groups = {group_name}
    agents_ids = set()
    for group in groups:
        agents_group = WazuhDBQueryMultigroups(group, select=['id']).run()['items']
        for agent in agents_group:
            agents_ids.add(str(agent['id']).zfill(3))

    return agents_ids
