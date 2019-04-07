# BigCoBackend
BigCo Studio backend system for Citi Innovation for BigCo Studio course.

### Deployment

***

- Python 2.7
- MongoDB 3.4
- Django 1.11.5
- xlsxwriter (Python library)
- Mongoengine (Python library)

Setting parameters in `backend/backend/settings.py`.

### Features to add

***

1. Pagination for `/api/digests`

### Interface Document

***

#### ① /api/detections

Supported HTTP types: **POST, PUT**

This api is used for NLP service to submit new detection results to backend systems or updated results of existed entries.

POST to create new entries. PUT to update existing entries.

**Request JSON format**

| Parameter    | Type            | Meaning                           |
| ------------ | --------------- | --------------------------------- |
| app_name     | string          | name of the app                   |
| manager_name | string          | name of the manager               |
| business     | string          | business department it belongs to |
| corp_sector  | string          | corporation sector it belongs to  |
| detected     | boolean         | whether this app contains PII     |
| result       | dict of records | detection results                 |

where a typical `result` looks like this:

```
{
    "col47":    ["Ssn", "Race"],
    "nameCol":  ["Name", "Gender"]
}
```

**Return**

A JSON which contains execution information.

If it succeeds, following JSON will return:

```
{
		"status": "ok"
}
```

Or an error JSON will return:

```
{
    "status": "error",
    "reason": "reason of failure"
}
```

#### ② /api/categories

Supported HTTP types: **GET**

This api is used for querying business and corp_sector information.

**Request JSON format**

No parameters.

**Return**

A JSON which maps business to its corp_sector list.

A typical result looks like this:

```
{
  	"Security": [
      	"Management",
        "Innovation",
        "Hr"
    ],
    "Finance": [
        "Management",
        "Recruitment",
        "Risk Analysis",
        "Innovation"
    ]
}
```

#### ③ /api/digests

Supported HTTP types: **GET**

This api is used for querying related DetectResult items given a query request. Function uses `business` and `corp_sector`  to do **AND** filtering and uses `app_name` and `manager_name` to do text searching.

**Request JSON format**

| Parameter    | Type   | Meaning                                      |
| ------------ | ------ | -------------------------------------------- |
| app_name     | string | name of the app (optional)                   |
| manager_name | string | name of the manager (optional)               |
| business     | string | business department it belongs to (optional) |
| corp_sector  | string | corporation sector it belongs to (optional)  |

**Return**

A JSON which is in following format:

```
{
  	"digest":  list(records)
}
```

where a single record is in following format:

```
{
    "app_name":     string,
    "manager_name": string,
    "business":     string,
    "corp_sector":  string,
    "detected":     boolean,
    "last_updated": string,
    "result":       dict(detected_results)
}
```

An example of `record["result"]` can be:

```
{
    "col47":    ["Ssn", "Race"],
    "nameCol":  ["Name", "Gender"]
}
```

#### ④ /api/reports

Supported HTTP types: **GET**

This api is used for getting a report file given a query request. Function uses  `business` and `corp_sector` to do **AND** filtering and uses `app_name` and `manager_name` to do text searching.

**Request JSON format**

| Parameter    | Type   | Meaning                                      |
| ------------ | ------ | -------------------------------------------- |
| app_name     | string | name of the app (optional)                   |
| manager_name | string | name of the manager (optional)               |
| business     | string | business department it belongs to (optional) |
| corp_sector  | string | corporation sector it belongs to (optional)  |

**Return**

An xlsx file.