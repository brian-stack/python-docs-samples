# Copyright 2020 Google LLC
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

from __future__ import absolute_import

import datetime
import os
import pytest

import dialogflow_v2 as dialogflow

import entity_type_management

PROJECT_ID = os.getenv("GCLOUD_PROJECT")
DISPLAY_NAME = "entity_type_" + datetime.datetime.now().strftime(
    "%Y%m%d%H%M%S"
)


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    # Create an entity type to list
    entity_types_client = dialogflow.EntityTypesClient()
    parent = entity_types_client.project_agent_path(PROJECT_ID)
    entity_type = dialogflow.types.EntityType(
        display_name=DISPLAY_NAME,
        kind=dialogflow.enums.EntityType.Kind.KIND_MAP,
    )
    response = entity_types_client.create_entity_type(parent, entity_type)
    entity_type_id = response.name.split("agent/entityTypes/")[1]

    yield

    # Delete the created entity type
    entity_type_path = entity_types_client.entity_type_path(
        PROJECT_ID, entity_type_id
    )
    entity_types_client.delete_entity_type(entity_type_path)


def test_list_entity_types(capsys):
    entity_type_management.list_entity_types(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert DISPLAY_NAME in out
