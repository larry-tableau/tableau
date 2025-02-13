# Data Dictionary and Semantic Layer for Tableau VizQL Data Service (VDS)

## **Purpose**
This document serves as a **Data Dictionary and Semantic Layer** to guide Large Language Models (LLMs) in constructing **valid JSON payloads** for querying Tableau's **VizQL Data Service (VDS)** via the REST API. It provides structured definitions of API components, schema requirements, and query rules to ensure **accurate and compliant request generation**.

## **1. API Endpoints**
### **1.1 Read Metadata**
- **Endpoint**: `POST /read-metadata`
- **Purpose**: Retrieves metadata about a published datasource.
- **Request Structure**:
  ```json
  {
    "connection": {
      "tableauServerName": "string",
      "siteId": "string",
      "datasource": "string",
      "databaseUsername": "string",
      "databasePassword": "string"
    },
    "options": {
      "returnFormat": "OBJECTS",
      "debug": false
    }
  }
  ```
- **Response Structure**:
  ```json
  {
    "data": [{}]
  }
  ```

### **1.2 Query Datasource**
- **Endpoint**: `POST /query-datasource`
- **Purpose**: Executes a structured query against a published datasource.
- **Request Structure**:
  ```json
  {
    "connection": {
      "tableauServerName": "string",
      "siteId": "string",
      "datasource": "string",
      "databaseUsername": "string",
      "databasePassword": "string"
    },
    "query": {
      "columns": [],
      "filters": []
    },
    "options": {
      "disaggregate": false,
      "returnFormat": "OBJECTS",
      "debug": false
    }
  }
  ```
- **Response Structure**:
  ```json
  {
    "data": [null]
  }
  ```

### **1.3 Simple Request**
- **Endpoint**: `GET /simple-request`
- **Purpose**: Health check or basic request validation.
- **Response Structure**:
  ```json
  "string"
  ```

---
## **2. Data Model and Query Components**

### **2.1 Connection Object**
Defines authentication and datasource parameters.
| Parameter            | Type   | Required | Description |
|----------------------|--------|----------|-------------|
| tableauServerName   | String | Yes      | Tableau Cloud server name |
| siteId              | String | Yes      | Tableau site identifier |
| datasource         | String | Yes      | Name of the published datasource |
| databaseUsername    | String | No       | Database username (if applicable) |
| databasePassword    | String | No       | Database password (if applicable) |

### **2.2 Query Object**
Defines the request payload structure for querying data.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| columns   | Array | Yes | Defines the output fields in the query. Must reference fields from the **DATA_MODEL**. |
| filters   | Array | No | Specifies conditions to filter query results. |

### **2.3 Column Object**
Each column object within the `columns` array represents a field in the dataset.
| Parameter        | Type   | Required | Description |
|------------------|--------|----------|-------------|
| columnName       | String | Yes      | Name of the field to query. |
| function        | String | No       | Aggregation function (e.g., `SUM`, `AVG`). Required for measures. |
| calculation     | String | No       | Custom calculation formula (e.g., `SUM([Profit])/SUM([Sales])`). |
| sortPriority    | Number | No       | Sorting priority (lower number = higher precedence). |
| sortDirection   | String | No       | Sort order (`ASC`, `DESC`). |
| maxDecimalPlaces | Number | No       | Number of decimal places for numeric outputs. |

### **2.4 Filter Object**
Filters refine query results by applying conditions.
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| columnName | String | Yes | Field being filtered. |
| filterType | String | Yes | Type of filter (`QUANTITATIVE`, `SET`, `DATE`, `TOP`). |
| howMany | Number | No | Used for `TOP` filters. Specifies number of results. |
| fieldToMeasure | Object | No | Required for `TOP` filters. Specifies column and function used to rank results. |
| min | Number | No | Used in `QUANTITATIVE` filters. Defines the lower limit. |
| max | Number | No | Used in `QUANTITATIVE` filters. Defines the upper limit. |
| units | String | No | Used in `DATE` filters. Time units (`DAYS`, `WEEKS`, etc.). |
| pastCount | Number | No | Used in `DATE` filters. Defines lookback window. |
| futureCount | Number | No | Used in `DATE` filters. Defines lookahead window. |

---
## **3. Query Examples**

### **3.1 Basic Query: Sum of Sales by Segment**
```json
{
  "columns": [
    { "columnName": "Segment" },
    { "columnName": "Sales", "function": "SUM" }
  ]
}
```

### **3.2 Filtered Query: Top 10 States by Sales**
```json
{
  "columns": [
    { "columnName": "State/Province" },
    { "columnName": "Sales", "function": "SUM" }
  ],
  "filters": [
    {
      "columnName": "State/Province",
      "filterType": "TOP",
      "howMany": 10,
      "fieldToMeasure": { "columnName": "Sales", "function": "SUM" },
      "direction": "TOP"
    }
  ]
}
```

### **3.3 Date-Based Query: Sales from the Last 30 Days**
```json
{
  "columns": [
    { "columnName": "Sales", "function": "SUM" }
  ],
  "filters": [
    {
      "filterType": "DATE",
      "columnName": "Order Date",
      "units": "DAYS",
      "pastCount": 30,
      "futureCount": 0
    }
  ]
}
```

---
## **4. Error Handling and Compliance**
- If a **malformed query** is detected, return an error message.
  ```json
  { "error": "Invalid query structure. Please refer to the VizQL documentation." }
  ```
- If the **query fails**, reference the **Vector Database** (`Tableau VizQL Reference Docs`).

---
## **5. Final Considerations**
This **Data Dictionary and Semantic Layer** ensures that LLMs generate **accurate, compliant, and structured queries** for Tableau's **VizQL Data Service**. It defines schema rules, API requirements, and structured examples to **minimize query failures** and **enhance API interaction efficiency**.

