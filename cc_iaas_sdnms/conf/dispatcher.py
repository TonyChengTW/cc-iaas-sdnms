# Copyright 2014 IBM Corp
# (C) Copyright 2015,2016 Hewlett Packard Enterprise Development LP
# Copyright 2017 Fujitsu LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg

dispatcher_opts = [
    cfg.StrOpt('scores',
               default='cc_iaas_sdnms.scores:ScoresResource',
               help='ScoresResource controller'),
]

dispatcher_group = cfg.OptGroup(name='dispatcher', title='dispatcher')


def register_opts(conf):
    conf.register_group(dispatcher_group)
    conf.register_opts(dispatcher_opts, dispatcher_group)


def list_opts():
    return dispatcher_group, dispatcher_opts