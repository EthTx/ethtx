# Copyright 2021 DAI FOUNDATION (the original version https://github.com/daifoundation/ethtx_ce)
# Copyright 2021-2022 Token Flow Insights SA (modifications to the original software as recorded
# in the changelog https://github.com/EthTx/ethtx/blob/master/CHANGELOG.md)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
# The product contains trademarks and other branding elements of Token Flow Insights SA which are
# not licensed under the Apache 2.0 license. When using or reproducing the code, please remove
# the trademark and/or other branding elements.

from ethtx.models.semantics_model import (
    EventSemantics,
    ParameterSemantics,
    TransformationSemantics,
)

lognote_event_v1 = EventSemantics(
    signature="0xd3ff30f94bb4ebb4f3d773ea26b6efc7328b9766f99f19dff6f01392138be46d",
    anonymous=False,
    name="LogNote",
    parameters=[
        ParameterSemantics(
            parameter_name="sig", parameter_type="bytes4", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="arg1", parameter_type="bytes32", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="arg2", parameter_type="bytes32", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="arg3", parameter_type="bytes32", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="data",
            parameter_type="bytes",
            components=[],
            indexed=False,
            dynamic=True,
        ),
    ],
)

lognote_transformation_v1 = {
    "sig": TransformationSemantics(transformed_type="ignore"),
    "arg1": TransformationSemantics(transformed_type="ignore"),
    "arg2": TransformationSemantics(transformed_type="ignore"),
    "arg3": TransformationSemantics(transformed_type="ignore"),
    "data": TransformationSemantics(
        transformed_type="call", transformation="decode_call(__contract__, data)"
    ),
}

lognote_event_v2 = EventSemantics(
    signature="0xd3d8bec38a91a5f4411247483bc030a174e77cda9c0351924c759f41453aa5e8",
    anonymous=False,
    name="LogNote",
    parameters=[
        ParameterSemantics(
            parameter_name="sig", parameter_type="bytes4", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="user", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="arg1", parameter_type="bytes32", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="arg2", parameter_type="bytes32", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="data",
            parameter_type="bytes",
            components=[],
            indexed=False,
            dynamic=True,
        ),
    ],
)

lognote_transformation_v2 = {
    "sig": TransformationSemantics(transformed_type="ignore"),
    "arg1": TransformationSemantics(transformed_type="ignore"),
    "arg2": TransformationSemantics(transformed_type="ignore"),
    "data": TransformationSemantics(
        transformed_type="call", transformation="decode_call(__contract__, data)"
    ),
}

lognote_event_v3 = EventSemantics(
    signature="0x644843f351d3fba4abcd60109eaff9f54bac8fb8ccf0bab941009c21df21cf31",
    anonymous=False,
    name="LogNote",
    parameters=[
        ParameterSemantics(
            parameter_name="sig", parameter_type="bytes4", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="guy", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="foo", parameter_type="bytes32", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="bar", parameter_type="bytes32", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="wad", parameter_type="uint256", components=[], indexed=False
        ),
        ParameterSemantics(
            parameter_name="fax",
            parameter_type="bytes",
            components=[],
            indexed=False,
            dynamic=True,
        ),
    ],
)

lognote_transformation_v3 = {
    "sig": TransformationSemantics(transformed_type="ignore"),
    "foo": TransformationSemantics(transformed_type="ignore"),
    "bar": TransformationSemantics(transformed_type="ignore"),
    "wad": TransformationSemantics(transformation="wad / 10**18"),
    "fax": TransformationSemantics(
        transformed_type="call", transformation="decode_call(__contract__, fax)"
    ),
}

logcall_event = EventSemantics(
    signature="0x25fce1fe01d9b241fda40b2152ddd6f4ba063fcfb3c2c81dddf84ee20d3f341f",
    anonymous=False,
    name="LOG_CALL",
    parameters=[
        ParameterSemantics(
            parameter_name="sig", parameter_type="bytes4", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="caller",
            parameter_type="address",
            components=[],
            indexed=True,
        ),
        ParameterSemantics(
            parameter_name="data",
            parameter_type="bytes",
            components=[],
            indexed=False,
            dynamic=True,
        ),
    ],
)

logcall_transformation = {
    "sig": TransformationSemantics(transformed_type="ignore"),
    "data": TransformationSemantics(
        transformed_type="call", transformation="decode_call(__contract__, data)"
    ),
}

anonymous_events = {
    lognote_event_v1.signature: lognote_transformation_v1,
    lognote_event_v2.signature: lognote_transformation_v2,
    lognote_event_v3.signature: lognote_transformation_v3,
    logcall_event.signature: logcall_transformation,
}
