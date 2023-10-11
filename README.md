# brite
`pip install -r requirements.txt` - install the requirements <br>
`uvicorn main:app --reload` - run the application <br>
`pytest` - run the tests

## Requests:
1. Get a list of movies:
    ```
    curl --location --request GET 'http://127.0.0.1:8000/movies?skip=2&title=with&limit=1'
    ```
2. Add a movie:
    ```
   curl --location --request POST 'http://127.0.0.1:8000/movies/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "title": "Shrek 2"
    }'
   ```
3. Delete a movie:
    ```
   curl --location --request DELETE 'http://127.0.0.1:8000/movies/97' \
    --header 'Authorization: Basic c3RhbmxleWpvYnNvbjpzd29yZGZpc2g='
   ```
