# API Documentation

## Base URL
All endpoints are located at `/`.

## Authentication
Some routes require authentication, which is handled using Auth0. The permission required for each route is specified in the endpoint documentation.

## Articles Endpoints

### `GET /articles`
Fetch all articles.

- **URL**: `/articles`
- **Method**: `GET`
- **URL Params**: Optional, `page` (default is 1)
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "articles": [
                {
                    "id": 1,
                    "title": "Article Title",
                    "content": "Article content...",
                    "author": "Author Name"
                },
                ...
            ]
        }
        ```

### `GET /articles/<int:article_id>`
Fetch a single article by its ID.

- **URL**: `/articles/<article_id>`
- **Method**: `GET`
- **URL Params**: `article_id`
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "article": {
                "id": 1,
                "title": "Article Title",
                "content": "Article content...",
                "author": "Author Name"
            }
        }
        ```
- **Error Response**:
    - **Code**: 404
    - **Message**: `ID <article_id> not found`

### `POST /articles`
Create a new article (requires `post:articles` permission).

- **URL**: `/articles`
- **Method**: `POST`
- **Body**:
    ```json
    {
        "title": "Article Title",
        "content": "Article content...",
        "author": "Author Name"
    }
    ```
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "id": 1
        }
        ```

### `PATCH /articles/<int:article_id>`
Update an existing article by its ID (requires `patch:articles` permission).

- **URL**: `/articles/<article_id>`
- **Method**: `PATCH`
- **URL Params**: `article_id`
- **Body**:
    ```json
    {
        "title": "New Title",
        "content": "Updated content...",
        "author": "New Author"
    }
    ```
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "id": 1
        }
        ```
- **Error Response**:
    - **Code**: 404
    - **Message**: `ID <article_id> not found`

### `DELETE /articles/<int:article_id>`
Delete an article by its ID (requires `delete:articles` permission).

- **URL**: `/articles/<article_id>`
- **Method**: `DELETE`
- **URL Params**: `article_id`
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "delete": 1
        }
        ```
- **Error Response**:
    - **Code**: 404
    - **Message**: `ID <article_id> not found`

---

## Collections Endpoints

### `GET /collections`
Fetch all collections.

- **URL**: `/collections`
- **Method**: `GET`
- **URL Params**: Optional, `page` (default is 1)
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "collections": [
                {
                    "id": 1,
                    "title": "Collection Title",
                    "description": "Collection description...",
                    "articles": [
                        {"id": 1, "title": "Article 1"},
                        {"id": 2, "title": "Article 2"}
                    ]
                },
                ...
            ]
        }
        ```

### `GET /collections/<int:collection_id>`
Fetch a single collection by its ID.

- **URL**: `/collections/<collection_id>`
- **Method**: `GET`
- **URL Params**: `collection_id`
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "collection": {
                "id": 1,
                "title": "Collection Title",
                "description": "Collection description...",
                "articles": [
                    {"id": 1, "title": "Article 1"},
                    {"id": 2, "title": "Article 2"}
                ]
            }
        }
        ```
- **Error Response**:
    - **Code**: 404
    - **Message**: `ID <collection_id> not found`

### `POST /collections`
Create a new collection (requires `post:collections` permission).

- **URL**: `/collections`
- **Method**: `POST`
- **Body**:
    ```json
    {
        "title": "Collection Title",
        "description": "Collection description...",
        "article_ids": [1, 2]
    }
    ```
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "collection": "<repr_of_collection>"
        }
        ```

### `PATCH /collections/<int:collection_id>`
Update an existing collection by its ID (requires `patch:collections` permission).

- **URL**: `/collections/<collection_id>`
- **Method**: `PATCH`
- **URL Params**: `collection_id`
- **Body**:
    ```json
    {
        "title": "Updated Title",
        "description": "Updated description...",
        "article_ids": [1, 2]
    }
    ```
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "id": 1
        }
        ```
- **Error Response**:
    - **Code**: 404
    - **Message**: `ID <collection_id> not found`

### `DELETE /collections/<int:collection_id>`
Delete a collection by its ID (requires `delete:collections` permission).

- **URL**: `/collections/<collection_id>`
- **Method**: `DELETE`
- **URL Params**: `collection_id`
- **Success Response**:
    - **Code**: 200
    - **Content**:
        ```json
        {
            "success": true,
            "delete": 1
        }
        ```
- **Error Response**:
    - **Code**: 404
    - **Message**: `ID <collection_id> not found`

---

## Error Handling

Common error responses include:

- **401 Unauthorized**:
    ```json
    {
        "success": false,
        "error": 401,
        "message": "Request lacks authorization parameter"
    }
    ```
- **403 Forbidden**:
    ```json
    {
        "success": false,
        "error": 403,
        "message": "Unauthorized"
    }
    ```
- **404 Not Found**:
    ```json
    {
        "success": false,
        "error": 404,
        "message": "ID <resource_id> not found"
    }
    ```
- **422 Unprocessable Entity**:
    ```json
    {
        "success": false,
        "error": 422,
        "message": "unprocessable"
    }
    ```
- **500 Internal Server Error**:
    ```json
    {
        "success": false,
        "error": 500,
        "message": "Error processing the request"
    }
    ```
