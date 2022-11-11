from nisystemlink.clients.core._uplink._json_model import JsonModel


class Operation(JsonModel):
    available: bool
    version: int


class OperationsV1(JsonModel):
    create_tables: Operation
    delete_tables: Operation
    modify_metadata: Operation
    list_tables: Operation
    read_data: Operation
    write_data: Operation


class ApiInfo(JsonModel):
    operations: OperationsV1
