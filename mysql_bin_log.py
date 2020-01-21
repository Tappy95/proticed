import json
import sys

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)

MYSQL_SETTINGS = {
    "host": "47.102.220.1",
    "port": 3306,
    "user": "wind",
    "passwd": "!Syy950507"
}

def main():
    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=3,
        blocking=True,
        only_schemas=['bigdata'],
        only_tables=['ebay_product'],
        only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
        # resume_stream=True,
        # log_file='mysql-bin.000001'
        )

    for binlogevent in stream:
        for row in binlogevent.rows:
            event = {"schema": binlogevent.schema, "table": binlogevent.table}
            if isinstance(binlogevent, DeleteRowsEvent):
                event["action"] = "delete"
                event["values"] = dict(row["values"].items())
                event = dict(event.items())
            elif isinstance(binlogevent, UpdateRowsEvent):
                event["action"] = "update"
                event["before_values"] = dict(row["before_values"].items())
                event["after_values"] = dict(row["after_values"].items())
                event = dict(event.items())
            elif isinstance(binlogevent, WriteRowsEvent):
                event["action"] = "insert"
                event["values"] = dict(row["values"].items())
                event = dict(event.items())
            print(event)
            sys.stdout.flush()
    stream.close()


if __name__ == "__main__":
    main()
