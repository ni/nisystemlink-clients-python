# -*- coding: utf-8 -*-

"""Implementation of HttpTagQueryResultCollection."""

from typing import Any, Dict, List, Optional, Tuple

from systemlink.clients import tag as tbase
from systemlink.clients.core._internal._http_client import HttpClient, HttpResponse
from typing_extensions import final


@final
class HttpTagQueryResultCollection(tbase.TagQueryResultCollection):
    def __init_subclass__(cls) -> None:
        raise TypeError(
            "type 'HttpTagQueryResultCollection' is not an acceptable base type"
        )

    def __init__(
        self,
        client: HttpClient,
        paths: Optional[str],
        keywords: Optional[str],
        properties: Optional[str],
        skip: int,
        take: Optional[int],
        tag_query_result: Dict[str, Any],
        http_response: HttpResponse,
    ) -> None:
        first_page, total_count = self.__handle_query_response(
            tag_query_result, http_response
        )
        super().__init__(first_page, total_count, skip)

        api = client.at_uri("/nitag/v2")
        base_params = {
            "path": paths,
            "keywords": keywords,
            "properties": properties,
            "skip": "0",
            "take": str(take) if take is not None else None,
        }
        for k, v in list(base_params.items()):
            if v is None:
                del base_params[k]

        def query(s: int) -> Tuple[Dict[str, Any], HttpResponse]:
            params = dict(base_params)
            params["skip"] = str(s)
            return api.get("/tags", params=params)

        self._query = query

    def _query_page(self, skip: int) -> List[tbase.TagData]:
        page, self._total_count = self.__handle_query_response(*self._query(skip))
        return page

    def __handle_query_response(
        self, response: Dict[str, Any], http_response: HttpResponse
    ) -> Tuple[List[tbase.TagData], int]:
        if response.get("totalCount") is None:
            raise tbase.TagManager.invalid_response(http_response)

        tags = []
        for t in response["tags"]:
            tags.append(
                tbase.TagData(
                    t["path"],
                    tbase.DataType.from_api_name(t["type"]) if t["type"] else None,
                    t.get("keywords"),
                    t.get("properties"),
                )
            )
            if t.get("collectAggregates"):
                tags[-1].collect_aggregates = True
        return tags, response["totalCount"]
