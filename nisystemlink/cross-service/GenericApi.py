"""This is a module for a cross-service API class."""
import asyncio
import datetime
import http.client
import json
import os
import time
import urllib.parse
from collections import defaultdict
from enum import Enum
from io import BytesIO
from typing import Any, Dict, List, Tuple  # noqa: F401


import aiohttp
import pandas as pd
import systemlink.clients.nifile.api.files_api as files_api
import systemlink.clients.nifile.models as fis_models
import systemlink.clients.nitestmonitor.api.results_api as results_api
import systemlink.clients.nitestmonitor.models as tm_models
from nxtdms import TdmsFile


class DatatableType(str, Enum):
    """Enum to describe the type of data in a table."""

    RAW = "raw"
    CYCLE = "cycle"
    CALCULATED = "calculated"
    DATASHEET = "datasheet"


class CrossServiceApi:
    """This is a class to abstract the SystemLink and related APIs.

    This will make it more conducive to usage by broader users.

    Attributes
    ----------
    dataHandle : str
        The handle for the Data API instance
    tablesHandle : str
        The handle ofr the Tables API instance
    id : string
        the alphanumeric string representing the SystemLink id of
        the test result in question

    Methods
    -------
    findOrCreateRecord(self, identifier: str) -> str:
        Either finds a record with a name that matches the identifier or creates
        a new reord with that name, the sets the active record for the object
        to the ID of that record.
    setFileMeta(self, fileMeta: Dict[str, str]):
        Sets the File Metadata of the active result.
    setChannelMeta(self, channel: str, channelMeta: Dict[str, str]):
        Sets the metadata for the specified channel.
    setChannelMapping(self, channelMappings: Dict[str, str]):
        Sets the channel mappings of a given file. This should map the
        file-centric names to the more commonly used aliases which
        are referenced elsewhere.
    appendData(self, data: pd.DataFrame):
        Appends data to a table.
    readData(self, channels: List[str]) -> pd.DataFrame:
        Reads data from a table.
    getTestMeta(self, key: List[str] = None) -> Dict[str, str]:
        Gets some or all fo the metadata associated with a test.
    getChannelMeta(self, channel: List[str] = None, key: List[str] = None) -> Dict[str, Dict[str, str]]: # noqa: E501
        Returns some or all metadata associated with some or all of the channels in a given test.
    """

    def __init__(
        self,
        result_handle: results_api.ResultsApi = None,
        fis_handle: files_api.FilesApi = None,
        sl_api_key: str = None,
        sl_uri: str = None,
    ):
        """Creates and initializes a new object, optionally using existing handles.

        :param result_handle: An instantiated
        systemlink.clients.nitestmonitor.api.results_api instance
        :param fis_handle: An instantiated systemlink.clients.nifile.api.files_api instance
        :param sl_api_key: An api key for the server being used
        :param sl_uri: The uri of the server being used
        """
        if not sl_api_key:
            sl_api_key = os.environ.get("SYSTEMLINK_API_KEY")
        if not sl_uri:
            self._sl_uri = os.getenv("SYSTEMLINK_HTTP_URI")[8:]
        else:
            self._sl_uri = sl_uri
        self._headers = {"X-NI-API-key": sl_api_key, "Content-Type": "application/json"}
        self._http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
        if result_handle:
            self._tm_result_handle = result_handle
        else:
            self._tm_result_handle = results_api.ResultsApi(results_api.ApiClient())
        if fis_handle:
            self._fis_handle = fis_handle
        else:
            self._fis_handle = files_api.FilesApi(files_api.ApiClient())
        self._loaded_records = []
        self._data_store: Dict[str, pd.DataFrame] = {}
        self._aiohttp_session = aiohttp.ClientSession(
            f"https://{self._sl_uri}", headers=self._headers
        )

    async def find_records(
        self,
        range_start: str = "",
        range_end: str = "",
        battery_id: str = "",
        properties: Dict[str, str] = {},
    ) -> List[str]:
        """Find records in a given range of dates (or date), optionally for a specific battery.

        Returns a list of record IDs.

        :param range_start: a datetime or string representing the beginning of the range of interest
        :param range_end: a datetime or string representing the end of the range of interest
        :param battery_id: the string representing the battery_id of a DUT
        :param properties: a dictionary of custom properties to query on
        """
        query_string = ""
        if range_end == "" and range_start != "":
            range_end = datetime.datetime.fromisoformat(range_start) + datetime.timedelta(seconds=1)
        elif range_end != "":
            range_end = datetime.datetime.fromisoformat(range_end) + datetime.timedelta(seconds=1)
        if range_start:
            query_string = 'startedAt >= "{0}" and startedAt <= "{1}"'.format(
                range_start, range_end
            )
        if battery_id != "":
            query_string = query_string + ' and serialNumber = "{0}"'.format(battery_id)
        for key in properties.keys():
            temp_key = key
            if key == "host_name":
                temp_key = "hostName"
            elif key == "part_number":
                temp_key = "partNumber"
            elif key == "program_name":
                temp_key = "programName"
            elif key == "serial_number":
                temp_key = "serialNumber"
            elif key == "started_at":
                temp_key = "startedAt"
            elif key == "status_type_summary":
                temp_key = "statusTypeSummary"
            elif key == "system_id":
                temp_key = "systemId"
            elif key == "total_time_in_seconds":
                temp_key = "totalTimeInSeconds"
            elif key == "updated_at":
                temp_key = "udpatedAt"
            elif key not in ["id", "keywords", "operator", "properties", "status", "workspace"]:
                temp_key = "properties." + key
            query_string = query_string + " and " + temp_key + ' == "' + properties[key] + '"'
        if query_string[0:5] == " and ":
            query_string = query_string[5::]
        query = tm_models.ResultsAdvancedQuery(filter=query_string)
        result_ids = []
        records = await self._tm_result_handle.query_results_v2(post_body=query)
        for result in records.results:
            result_ids.append(result.id)
        while records.continuation_token:
            query.continuation_token = records.continuation_token
            records = await self._tm_result_handle.query_results_v2(post_body=query)
            for result in records.results:
                result_ids.append(result.id)
        return result_ids

    async def create_record(
        self,
        start_time: str,
        battery_id: str,
        program_name: str,
        column_schemas: list[Dict[str, Any]],
        workspace: str = None,
    ) -> str:
        """Creates a record.

        Creates a new record based on the parameters passed in.

        Returns the new record ID

        :param start_time: The time at which the test you are creating started
        :param battery_id: The id of the battery under test
        :param program_name: The value to map to 'Program Name' in the test result
        """
        running_status = tm_models.StatusObject(status_type="RUNNING", status_name="Running")
        new_result = tm_models.TestResultRequestObject(
            program_name=program_name,
            serial_number=battery_id,
            started_at=start_time,
            status=running_status,
        )
        if workspace:
            new_result.workspace = workspace
        creation_request = tm_models.CreateTestResultsRequest(results=[new_result])
        resp = tm_models.ResultsPartialSuccessResponse(
            await self._tm_result_handle.create_results_v2(creation_request)
        )
        if len(resp.results.results) > 1:
            raise InternalError()
        else:
            record_id = resp.results.results[0].id
            frames_ids = []
            for column_schema in column_schemas:
                frame_id = await self.create_datatable(column_schema, DatatableType.RAW, workspace)
                frames_ids.append(frame_id)
            await self.populate_record(record_id, data_table_ids=frames_ids)
            return record_id

    async def populate_record(
        self,
        record_id: str,
        system_id: str = None,
        hostname: str = None,
        operator: str = None,
        part_number: str = None,
        file_ids: List[str] = None,
        total_time_in_seconds: float = 0,
        metadata: Dict[str, str] = None,
        data_table_ids: List[str] = None,
    ):
        """Takes a pre-existing record and adds the specified metadata.

        :param record_id: A string representing the internal SystemLink
        id of a specific test
        :param system_id: A string representing the id of the system running the test
        :param hostname: A string representin the hostname of the tester
        :param operator: A string representing the operator
        :param part_number: A string representing the part number of the battery
        :param file_ids: A list of strings representing the SystemLink ids of the
        files to be attached to the record
        :param total_time_in_seconds: A float representing the time for which the test ran.
        :param metadata: A dictionary of strings that correspond to the test's
        metadata not otherwise described above.
        """
        #         done_status = tm_models.StatusObject(status_type="DONE", status_name="Done")
        update_request_object = {
            "id": record_id,
            "status": {"statusType": "DONE", "statusName": "Done"},
        }
        if system_id:
            update_request_object["systemID"] = system_id
        if hostname:
            update_request_object["hostName"] = hostname
        if operator:
            update_request_object["operator"] = operator
        if part_number:
            update_request_object["partNumber"] = part_number
        if file_ids:
            update_request_object["fileIds"] = file_ids
        if total_time_in_seconds > 0:
            update_request_object["totalTimeInSeconds"] = total_time_in_seconds
        if metadata:
            update_request_object["properties"] = metadata
        if data_table_ids:
            update_request_object["dataTableIds"] = data_table_ids
        update_result_request = tm_models.UpdateTestResultsRequest(results=[update_request_object])
        resp = await self._tm_result_handle.update_results_v2(update_result_request)
        if resp.failed:
            raise InternalError()

    async def set_channel_meta(self, record_id: str, channel: str, channel_meta: Dict[str, str]):
        """Sets the metadata for the specified channel.

        :param channel: The original name of the channel
        :param channelMeta: The dictionary representing the channel's metadata.
        """
        column_exist = False
        frames = await self.get_test_meta(record_id, ["data_table_ids"])
        for frame_id in frames["data_table_ids"]:
            http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
            http_conn.request("GET", "/nidataframe/v1/tables/" + frame_id, headers=self._headers)
            resp = http_conn.getresponse()
            response = json.loads(resp.read())
            for column in response["columns"]:
                if column["name"] == channel:
                    column_exist = True
                    body = json.dumps({"columns": [{"name": channel, "properties": channel_meta}]})
                    http_conn.request(
                        "PATCH",
                        "/nidataframe/v1/tables/" + frame_id,
                        body=body,
                        headers=self._headers,
                    )
        if column_exist is False:
            print("Channel " + channel + " doesn't exist")

    def set_channel_mapping(self, channel_mappings: Dict[str, str]):
        """Set mappings of original names to standardized names.

        Sets the channel mappings of a given file. This should map the
        file-centric names to the more commonly used aliases which
        are referenced elsewhere.

        :param channelMappings: A dictionary mapping aliases to channel names,
        where the key represents the alias and the value represents the native
        channel name.
        """
        # todo
        raise NotImplementedError()
        return ""

    async def get_target_frame_by_name(
        self, record_id: str, frame_names: List[str]
    ) -> Dict[str, str]:
        """Finds the frame_id of a given frame by name for a specific record id."""
        target_to_source_mapping = {}
        for source_frame in frame_names:
            test_meta = await self.get_test_meta(record_id, ["data_table_ids"])
            if test_meta["data_table_ids"][0] == "Not Found":
                raise InternalError("Record has no dataframe attached")
            for target_frame in test_meta["data_table_ids"]:
                specific_frame_name = self._get_datatable_name(target_frame)
                if source_frame == specific_frame_name:
                    target_to_source_mapping[target_frame] = source_frame
            if source_frame not in target_to_source_mapping.values():
                raise KeyError("No corresponding target frame.")
        return target_to_source_mapping

    async def append_data(
        self, record_id: str, df_dict: Dict[str, pd.DataFrame], chunk_size: int = 5000
    ):
        """Appends data to a table.

        There must be an existing and appropriately named table for each table passed.
        """
        target_to_source_mapping = await self.get_target_frame_by_name(record_id, df_dict.keys())
        for target in target_to_source_mapping.keys():
            data = df_dict[target_to_source_mapping[target]]
            columns = data.columns.values.tolist()
            print(len(data))
            num_its = len(data.index) / chunk_size
            print(num_its)
            i = 0
            print("Start upload...")
            while i < num_its:
                j = 0
                status = 0
                while j < 5 and status != 204:
                    try:
                        if status != 204:
                            body = {
                                "frame": {
                                    "columns": columns,
                                    "data": data.iloc[chunk_size * i : chunk_size * (i + 1)]
                                    .to_numpy(dtype=str, na_value="0")
                                    .tolist(),
                                },
                                "endOfData": False,
                            }
                            response = await asyncio.create_task(
                                self._aiohttp_session.post(
                                    "/nidataframe/v1/tables/{}/data".format(target), json=body
                                )
                            )
                            del body
                            await response.read()
                            status = response.status
                            print(status)
                            j += 1
                            print(f"j={j} and status={status}")
                    except Exception:
                        continue
                if j >= 5:
                    raise InternalError(await response.read())
                i += 1
                print(i)
            print("table " + target_to_source_mapping[target] + " uploads complete")
        print("Uploads complete")

    def _get_datatable_type(self, table_id: str) -> DatatableType:
        http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
        http_conn.request(
            "GET",
            "/nidataframe/v1/tables/{0}".format(table_id),
            headers=self._headers,
        )
        response = http_conn.getresponse()
        payload = str(response.read()).replace("\\", "")
        dataresponse = json.loads(payload[2:-1])
        try:
            datatable_type = dataresponse["properties"]["datatableType"]
            ret_val = DatatableType(datatable_type)
            return ret_val
        except KeyError:
            raise Exception(f"Error getting type of dataframe '{table_id}'")

    def _get_datatable_name(self, table_id: str) -> str:
        http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
        http_conn.request(
            "GET",
            "/nidataframe/v1/tables/{0}".format(table_id),
            headers=self._headers,
        )
        response = http_conn.getresponse()
        payload = str(response.read()).replace("\\", "")
        dataresponse = json.loads(payload[2:-1])
        try:
            return dataresponse["name"]
        except KeyError:
            raise Exception(f"Error getting name of dataframe '{table_id}'")

    async def _check_for_complete_table(self, table_id) -> bool:
        """Checks to see if the metadata length matches the actual."""
        http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
        http_conn.request(
            "GET",
            "/nidataframe/v1/tables/{0}".format(table_id),
            headers=self._headers,
        )
        response = http_conn.getresponse()
        payload = str(response.read()).replace("\\", "")
        dataresponse = json.loads(payload[2:-1])
        try:
            row_count = dataresponse["rowCount"]
        except KeyError:
            raise Exception(f"Error getting rowCount of dataframe '{table_id}'")
        all_there = False
        num_retries = 0
        while not all_there and num_retries < 5:
            http_conn.request(
                "GET",
                "/nidataframe/v1/tables/{0}/data?columns=DateTime&take=1".format(table_id),
                headers=self._headers,
            )
            response = http_conn.getresponse()
            payload = str(response.read()).replace("\\", "")
            dataresponse = json.loads(payload[2:-1])
            actual_row_count = dataresponse["totalRowCount"]
            if actual_row_count == row_count:
                all_there = True
            else:
                num_retries += 1
                time.sleep(30)
        return all_there

    async def read_data(
        self,
        record_id: str,
        requested_channels: List[str] = None,
        specific_table: str = None,
        num_points: int = None,
        channels_for_decimation: list[str] = None,
        verify_completeness: bool = True,
        filters: List[Dict[str, any]] = None,
    ) -> pd.DataFrame:
        """Reads data from a table.

        :param channels: a list describing the channels (columns) to return data for
        """
        if specific_table:
            target_table_dict = await self.get_target_frame_by_name(record_id, [specific_table])
            table_ids = target_table_dict.keys()
        else:
            metadata = await self.get_test_meta(record_id, ["data_table_ids"])
            table_ids = metadata["data_table_ids"]
            filtered_table_ids = []
            for id in table_ids:
                if self._get_datatable_type(id) in [DatatableType.RAW, DatatableType.CALCULATED]:
                    filtered_table_ids.append(id)
            table_ids = filtered_table_ids

        frame_ordered_lookups = defaultdict(list)
        dfs = []
        if requested_channels:
            desired_channels_dict = await self.get_channel_name_by_synonym(
                record_id, list(requested_channels), table_ids
            )
            for desired_channel in desired_channels_dict.keys():
                frame_ordered_lookups[desired_channels_dict[desired_channel]["frame"]].append(
                    desired_channels_dict[desired_channel]["actual_channel"]
                )
            required_table_ids = list(frame_ordered_lookups.keys())
        else:
            required_table_ids = table_ids
        for table_id in required_table_ids:
            if verify_completeness:
                if not await self._check_for_complete_table(table_id):
                    raise InternalError("Datatable is still being written to.")
            continuation_token = None
            body = {}
            if frame_ordered_lookups:
                try:
                    desired_channels = list(frame_ordered_lookups[table_id])
                    if "DateTime" not in desired_channels:
                        desired_channels.append("DateTime")
                    body["columns"] = desired_channels
                except KeyError:
                    pass
            if filters:
                body["filters"] = filters
            http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
            if num_points:
                body["decimation"] = {}
                body["decimation"]["xColumn"] = "DateTime"
                body["decimation"]["intervals"] = num_points
                if channels_for_decimation:
                    body["decimation"]["method"] = "MAX_MIN"
                    body["decimation"]["yColumns"] = channels_for_decimation
                http_conn.request(
                    "POST",
                    "/nidataframe/v1/tables/{0}/query-decimated-data".format(table_id),
                    body=json.dumps(body),
                    headers=self._headers,
                )
            else:
                body["orderBy"] = [{"column": "DateTime", "descending": False}]
                http_conn.request(
                    "POST",
                    "/nidataframe/v1/tables/{0}/query-data".format(table_id),
                    body=json.dumps(body),
                    headers=self._headers,
                )
            response = http_conn.getresponse()
            payload = str(response.read()).replace("\\", "")
            dataresponse = json.loads(payload[2:-1])
            try:
                df = pd.DataFrame(
                    dataresponse["frame"]["data"], columns=dataresponse["frame"]["columns"]
                )
            except KeyError:
                raise KeyError(payload)
            if not num_points:
                continuation_token = dataresponse["continuationToken"]
            while continuation_token:
                body["continuationToken"] = continuation_token
                http_conn.request(
                    "POST",
                    "/nidataframe/v1/tables/{0}/query-data".format(table_id),
                    body=json.dumps(body),
                    headers=self._headers,
                )
                response = http_conn.getresponse()
                payload = str(response.read()).replace("\\", "")
                dataresponse = json.loads(payload[2:-1])
                try:
                    df = pd.concat(
                        [
                            df,
                            pd.DataFrame(
                                dataresponse["frame"]["data"],
                                columns=dataresponse["frame"]["columns"],
                            ),
                        ],
                        copy=False,
                        ignore_index=True,
                    )
                    continuation_token = dataresponse["continuationToken"]
                except KeyError:
                    raise KeyError(payload)
            df.set_index("DateTime")
            for column in df.columns:
                data_type = await self._get_channel_datatype(column, table_id)
                if data_type == "TIMESTAMP":
                    data_type = "datetime64"
                elif data_type == "STRING":
                    data_type = "object"
                else:
                    data_type = data_type.lower()
                df = df.astype({column: data_type})
            dfs.append(df)
        return_df = dfs[0]
        for df in dfs[1:]:
            return_df = pd.concat(
                [return_df, df],
                axis=1,
            )
        if "DateTime" in return_df.columns:
            df_date = df["DateTime"]
            df_values = return_df.drop(["DateTime"], axis=1)
            return_df = pd.concat([df_date, df_values], axis=1)
        new_channel_names = {}
        if requested_channels:
            for channel in requested_channels:
                new_channel_names[desired_channels_dict[channel]["actual_channel"]] = channel
            final_column_names = []
            for column in return_df.columns.values.tolist():
                try:
                    final_column_names.append(new_channel_names[column])
                except KeyError as e:
                    if column == "DateTime":
                        return_df = return_df.drop(["DateTime"], axis=1)
                    else:
                        raise e
            return_df.columns = final_column_names
        if requested_channels:
            return return_df[requested_channels]
        else:
            return return_df

    async def _get_channel_datatype(self, desired_channel: str, frame_id: str) -> str:
        """Get the datatype of a given cahnnel."""
        http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
        http_conn.request(
            "GET",
            "/nidataframe/v1/tables/{0}".format(frame_id),
            headers=self._headers,
        )
        response = http_conn.getresponse()
        payload = str(response.read()).replace("\\", "")
        try:
            dataresponse = json.loads(payload[2:-1])
            for column in dataresponse["columns"]:
                if column["name"] == desired_channel:
                    return column["dataType"]
        except Exception:
            raise InternalError(dataresponse)

    async def get_all_columns(self, record_id: str) -> List[str]:
        """Reads data from a table.

        :param channels: a list describing the channels (columns) to return data for
        """
        search_results = await self.get_test_meta(record_id, ["data_table_ids"])
        data_table_ids = search_results["data_table_ids"]
        column_names = []
        for frame_id in data_table_ids:

            http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
            http_conn.request(
                "GET",
                "/nidataframe/v1/tables/{0}".format(frame_id),
                headers=self._headers,
            )
            response = http_conn.getresponse()
            payload = str(response.read()).replace("\\", "")
            dataresponse = json.loads(payload[2:-1])
            for column in dataresponse["columns"]:
                column_names.append(column["name"])
        return column_names

    async def get_specific_columns(self, table_id: str) -> List[str]:
        """Reads data from a table.

        :param channels: a list describing the channels (columns) to return data for
        """
        column_names = []
        http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
        http_conn.request(
            "GET",
            "/nidataframe/v1/tables/{0}".format(table_id),
            headers=self._headers,
        )
        response = http_conn.getresponse()
        payload = str(response.read()).replace("\\", "")
        dataresponse = json.loads(payload[2:-1])
        for column in dataresponse["columns"]:
            column_names.append(column["name"])
        return column_names

    async def get_test_meta(self, record_id: str, keys: List[str] = None) -> Dict[str, str]:
        """Gets some or all fo the metadata associated with a test.

        :param record_id: A string representing the internal SystemLink id of a specific test
        :param keys: a list describing the keys to return values for
        """
        resp = await self._tm_result_handle.get_result_v2(
            result_id=record_id, _preload_content=False
        )
        response = await resp.read()
        resp = json.loads(response)
        name_map = {
            "fileIds": "file_ids",
            "hostName": "host_name",
            "id": "id",
            "keywords": "keywords",
            "operator": "operator",
            "partNumber": "part_number",
            "programName": "program_name",
            "properties": "properties",
            "serialNumber": "serial_number",
            "startedAt": "started_at",
            "status": "status",
            "statusTypeSummary": "status_type_summary",
            "systemId": "system_id",
            "totalTimeInSeconds": "total_time_in_seconds",
            "updatedAt": "updated_at",
            "workspace": "workspace",
            "dataTableIds": "data_table_ids",
        }
        resp = {name_map[name]: val for name, val in resp.items()}
        status_map = {"statusType": "status_type", "statusName": "status_name"}
        resp["status"] = {status_map[name]: val for name, val in resp["status"].items()}
        return_dict = {}
        if keys:
            for key in keys:
                if key == "status":
                    return_dict["status"] = resp["status"]["status_name"]
                else:
                    try:
                        return_dict[key] = resp[key]
                    except Exception:
                        try:
                            return_dict[key] = resp["properties"][key]
                        except Exception:
                            return_dict[key] = "Not Found"
        else:
            for key in resp:
                #                 if key in ["started_at", "updated_at"]:
                #                     temp = resp[key].isoformat()
                #                     return_dict[key] = str(temp)
                if key == "properties":
                    for property in resp["properties"]:
                        return_dict[property] = resp["properties"][property]
                elif key == "status":
                    return_dict["status"] = resp["status"]["status_name"]
                elif key in ["status_type_summary", "id", "file_ids", "workspace"]:
                    continue
                else:
                    return_dict[key] = resp[key]
        return return_dict

    async def get_channel_name_by_synonym(
        self, record_id: str, channels: List[str], table_ids: List[str] = None
    ) -> Dict[str, Dict[str, str]]:
        """Looks up a channel name based on a synonym. Returns a list of Dictionaries."""
        if not table_ids:
            search_results = await self.get_test_meta(record_id, ["data_table_ids"])
            data_table_ids = search_results["data_table_ids"]
        else:
            data_table_ids = table_ids
        return_dict = {}
        for frame_id in data_table_ids:
            found_dict = {}
            http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
            http_conn.request(
                "GET",
                "/nidataframe/v1/tables/{0}".format(frame_id),
                headers=self._headers,
            )
            response = http_conn.getresponse()
            payload = str(response.read())[2:-1]
            dataresponse = json.loads(payload.replace("\\", "\\\\"))
            try:
                dataframe_type = dataresponse["properties"]["datatable_type"]
            except KeyError:
                dataframe_type = DatatableType.RAW
            if dataframe_type in [DatatableType.RAW, DatatableType.CALCULATED]:
                for channel in channels:
                    mapped_channel_name = ""
                    for column in dataresponse["columns"]:
                        if not mapped_channel_name:
                            if column["name"] == channel:
                                mapped_channel_name = channel
                                found_dict[channel] = {
                                    "frame": frame_id,
                                    "actual_channel": column["name"],
                                }
                            elif "synonym" in column["properties"].keys():
                                if column["properties"]["synonym"] == channel:
                                    mapped_channel_name = channel
                                    found_dict[channel] = {
                                        "frame": frame_id,
                                        "actual_channel": column["name"],
                                    }

                for found_channel in found_dict.keys():
                    channels.remove(found_channel)
                return_dict.update(found_dict)
        if len(channels) > 0:
            error_message = "Missing the following channels: "
            for channel in channels:
                error_message.join(f"{channel}, ")
            error_message = error_message[:-2]
            raise KeyError(error_message)
        return return_dict

    def get_channel_meta(
        self, channel: List[str] = None, key: List[str] = None
    ) -> Dict[str, Dict[str, str]]:
        """Return some or all of the channel metadata.

        Channel data may include things like units or other identifying characterstics

        :param channel: a list describing the channels (columns) to return data for
        :param key: a list describing the keys to return values for
        """
        raise NotImplementedError()
        if key:

            # return specified key-value pairs as a dictionary, with in a dictionary
            # where the key represents the channel name
            return ""
        else:
            # return all key-value pairs as a dictionary, with in a dictionary
            # where the key represents the channel name
            return ""

    async def get_synonym_table(self, file_name: str = "synonyms.csv") -> Dict[str, str]:
        """Get the synonym lookup table as a dictionary."""
        property_query = fis_models.PropertyQuery("Name", "EQUAL", file_name)
        fis_query = fis_models.QueryAvailableFilesRequest(properties_query=[property_query])
        file_list = await self._fis_handle.query_available_files(query=fis_query)
        properties = file_list.available_files[0].properties
        return properties  # todo: Need a test for this

    async def close_connections(self):
        """Close all open session handles."""
        await self._tm_result_handle.api_client.close()
        await self._fis_handle.api_client.close()

    async def _post_data_to_dfs(self, body, frame_id, max_tries=5):
        num_trys = 0
        upload_success = False
        local_http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
        while not upload_success and num_trys < max_tries:
            local_http_conn.request(
                "POST",
                "/nidataframe/v1/tables/{}/data".format(frame_id),
                body=json.dumps(body),
                headers=self._headers,
            )
            r = local_http_conn.getresponse()
            if r.status == 204:
                upload_success = True
            else:
                num_trys += 1
                print(r.status)
                print("Upload attempt {} failed".format(num_trys))
        local_http_conn.close()
        return upload_success

    async def get_test_id_from_file_id(self, file_id: str):
        """Get the test id that corresponds to a given file."""
        response = fis_models.QueryResponse(
            await self._fis_handle.list_available_files_get(id=file_id)
        )
        files = response.links.available_files
        return files[0].properties["test_id"]

    async def create_datatable(
        self,
        column_schema: Dict[str, Any],
        datatable_type: DatatableType = DatatableType.RAW,
        workspace: str = None,
    ) -> str:
        """Create a datatable."""
        datatable = ""
        if workspace:
            column_schema["workspace"] = workspace
        body = json.dumps(column_schema)
        self._http_conn.request("POST", "/nidataframe/v1/tables", body=body, headers=self._headers)
        response = self._http_conn.getresponse()
        if response.status >= 400:
            raise InternalError(response.read())
        else:
            payload = ""
            while chunk := response.read(200):
                payload += repr(chunk)
            frames = json.loads(payload.replace("'", '"')[2:-1])
            datatable = frames["id"]
        body = json.dumps({"properties": {"datatableType": datatable_type}})
        self._http_conn.request(
            "PATCH", f"/nidataframe/v1/tables/{datatable}", body=body, headers=self._headers
        )
        response = self._http_conn.getresponse()
        if response.status >= 400:
            raise InternalError(response.read())
        else:
            response.read()
        return datatable

    async def get_workspace_id(self, desired_workspace: str) -> str:
        """Get the id of the specified workspace."""
        desired_workspace = urllib.parse.quote(desired_workspace)
        self._http_conn.request(
            "GET", f"/niuser/v1/workspaces?name={desired_workspace}", headers=self._headers
        )
        response = self._http_conn.getresponse()
        if response.status >= 400:
            raise InternalError(response.read())
        payload = ""
        while chunk := response.read(200):
            payload += repr(chunk)
        query_response = json.loads(payload.replace("'", '"')[2:-1])
        workspace_id = query_response["workspaces"][0]["id"]
        return workspace_id

    async def get_specific_cycle_table_id(
        self, battery_id: str, cycle_counter_version: str = None
    ) -> str:
        """Get the id of the specified cycle table."""
        local_http_conn = http.client.HTTPSConnection(self._sl_uri + ":443")
        body = {}
        desired_type = DatatableType.CYCLE
        if cycle_counter_version:
            body[
                "filter"
            ] = f'properties["SerialNumber"] == "{battery_id}" and properties["cycle_counter_version"] == "{cycle_counter_version}" and properties["datatableType"] == "{desired_type}"'  # noqa: E501
        else:
            body[
                "filter"
            ] = f'properties["SerialNumber"] == "{battery_id}" and properties["datatableType"] == "{desired_type}"'  # noqa: E501
        body["orderBy"] = "CREATED_AT"
        body["orderByDescending"] = True

        local_http_conn.request(
            "POST", "/nidataframe/v1/query-tables", body=json.dumps(body), headers=self._headers
        )
        response = local_http_conn.getresponse()
        if response.status >= 400:
            raise InternalError(response.read())
        else:
            payload = ""
            while chunk := response.read(200):
                payload += repr(chunk).replace("'", '"')[2:-1]
            try:
                frames = json.loads(payload)
            except Exception as e:
                print(payload)
                raise e(payload)
            return frames["tables"][0]["id"]

    async def get_limit_meta_data(
        self, test_result_id: str, properties_desired: list[str], revision: str = None
    ):
        """This returns metadata stored as part of a limit sheet dataframe."""
        dataframes = await self.get_test_meta(test_result_id, ["data_table_ids"])
        newest_frame = {}
        for frame in dataframes["data_table_ids"]:
            if frame != "":
                # check if revision has a value, compare to "SheetRevision"
                try:
                    datatable_type = self._get_datatable_type(frame)
                    if datatable_type == DatatableType.DATASHEET:
                        http_conn = http.client.HTTPSConnection(self.sl_uri + ":443")
                        http_conn.request(
                            "GET",
                            f"/nidataframe/v1/tables/{frame}",
                            headers=self.headers,
                        )
                        response = http_conn.getresponse()
                        payload = json.loads(response.read().decode())
                        if revision is not None:
                            if payload["properties"]["SheetRevision"] == revision:
                                newest_frame["frame"] = payload
                        else:
                            timestamp = datetime.datetime.fromisoformat(payload["createdAt"][:-1])
                            try:
                                if timestamp > newest_frame["timestamp"]:
                                    newest_frame["timestamp"] = timestamp
                                    newest_frame["frame"] = payload
                            except KeyError:
                                newest_frame["timestamp"] = timestamp
                                newest_frame["frame"] = payload
                except KeyError:
                    continue
        try:
            selected_sheet = newest_frame["frame"]
        except KeyError:
            raise KeyError(f"Revision '{revision}' not found")
        selected_properties = {}
        for prop in properties_desired:
            try:
                selected_properties[prop] = selected_sheet["properties"][prop]
            except KeyError:
                raise KeyError(
                    f"Error getting meta_data '{prop}' of dataframe '{selected_sheet['id']}'"
                )
        return selected_properties

    async def get_limit_columns(
        self, test_result_id: str, columns_desired: list[str], revision: str = None
    ):
        """Returns a specific column or columns from a limit sheet."""
        dataframes = await self.get_test_meta(test_result_id, ["data_table_ids"])
        newest_frame = {}
        for frame in dataframes["data_table_ids"]:
            if frame != "":
                try:
                    datatable_type = self._get_datatable_type(frame)
                    if datatable_type == DatatableType.DATASHEET:
                        http_conn = http.client.HTTPSConnection(self.sl_uri + ":443")
                        http_conn.request(
                            "GET",
                            f"/nidataframe/v1/tables/{frame}",
                            headers=self.headers,
                        )
                        response = http_conn.getresponse()
                        payload = json.loads(response.read().decode())
                        if revision is not None:
                            if payload["properties"]["SheetRevision"] == revision:
                                newest_frame["frame"] = payload
                        else:
                            timestamp = datetime.datetime.fromisoformat(payload["createdAt"][:-1])
                            try:
                                if timestamp > newest_frame["timestamp"]:
                                    newest_frame["timestamp"] = timestamp
                                    newest_frame["frame"] = payload
                            except KeyError:
                                newest_frame["timestamp"] = timestamp
                                newest_frame["frame"] = payload
                except KeyError:
                    continue
        try:
            selected_sheet = newest_frame["frame"]
        except KeyError:
            raise KeyError(f"Revision '{revision}' not found")
        limit_df = pd.DataFrame()
        if "Temperature" not in columns_desired:
            columns_desired.insert(0, "Temperature")
        else:
            index = columns_desired("Temperature")
            columns_desired.insert(0, columns_desired.pop(index))
        for column in columns_desired:
            try:
                body = {}
                body["columns"] = [column]
                body["orderBy"] = [{"column": "Temperature", "descending": False}]
                http_conn = http.client.HTTPSConnection(self.sl_uri + ":443")
                http_conn.request(
                    "POST",
                    f"/nidataframe/v1/tables/{selected_sheet['id']}/query-data",
                    body=json.dumps(body),
                    headers=self.headers,
                )
                response = http_conn.getresponse()
                payload = json.loads(response.read().decode())
                new_df = pd.DataFrame(
                    payload["frame"]["data"],
                    columns=payload["frame"]["columns"],
                )
                limit_df = pd.concat([limit_df, new_df], axis=1)

            except KeyError:
                raise KeyError(
                    f"Error getting column '{column}' of dataframe '{selected_sheet['id']}'"
                )
        return limit_df


class InternalError(Exception):
    """Covers a variety of internal situations that should never occur. Contact NI for support."""

    pass