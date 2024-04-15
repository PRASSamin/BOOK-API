# PRAS BOOK API Documentation

Welcome to the PRAS BOOK API documentation. This guide provides information on how to use the API to access book data.

## Base URL

The base URL for the PRAS BOOK API is `https://prasbook.onrender.com/api`.

## Endpoints

### Retrieve All Books

- **URL**: `/books`
- **Method**: `GET`
- **Description**: Retrieves a list of all available books.
- **Query Parameters** (optional):
  - `q`: Filter books by title, author, or genre.
- **Example Requests**:
### HTTP
  ```http
  GET https://prasbook.onrender.com/api/books
  ```
### Python
  ```python
  import requests
  
  response = requests.get('https://prasbook.onrender.com/api/books')
  print(response.json())
  ```
### JavaScript
  ```javascript
  fetch('https://prasbook.onrender.com/api/books')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
  ```
### Ruby
  ```ruby
  require 'net/http'
  require 'json'
  
  uri = URI('https://prasbook.onrender.com/api/books')
  response = Net::HTTP.get(uri)
  puts JSON.parse(response)
  ```
### Java
  ```java
  import java.net.HttpURLConnection;
  import java.net.URL;
  import java.io.BufferedReader;
  import java.io.InputStreamReader;
  
  public class Main {
      public static void main(String[] args) throws Exception {
          URL url = new URL("https://prasbook.onrender.com/api/books");
          HttpURLConnection connection = (HttpURLConnection) url.openConnection();
          connection.setRequestMethod("GET");
  
          BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
          String inputLine;
          StringBuffer response = new StringBuffer();
  
          while ((inputLine = in.readLine()) != null) {
              response.append(inputLine);
          }
          in.close();
  
          System.out.println(response.toString());
      }
  }
  ```
### Flutter(dart)
  ```dart
  import 'package:http/http.dart' as http;
  
  void main() async {
    var response = await http.get('https://prasbook.onrender.com/api/books');
    print(response.body);
  }
  ```
### C++
  ```cpp
  #include <iostream>
  #include <curl/curl.h>
  
  int main() {
      CURL *curl;
      CURLcode res;
  
      curl = curl_easy_init();
      if (curl) {
          curl_easy_setopt(curl, CURLOPT_URL, "https://prasbook.onrender.com/api/books");
          res = curl_easy_perform(curl);
  
          if (res != CURLE_OK)
              std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
  
          curl_easy_cleanup(curl);
      }
  
      return 0;
  }
  ```
- **Example Response**:
### JSON
  ```json
  [
    {
      "Title": "Book Title 1",
      "Authors": ["Author 1", "Author 2"],
      "Publisher": "Publisher 1",
      "Published Date": "2022-01-01",
      "ISBN": "1234567890",
      "Thumbnail URL": "https://example.com/thumbnail1.jpg"
    },
    {
      "Title": "Book Title 2",
      "Authors": ["Author 3"],
      "Publisher": "Publisher 2",
      "Published Date": "2022-02-01",
      "ISBN": "0987654321",
      "Thumbnail URL": "https://example.com/thumbnail2.jpg"
    },
    ...
  ]
  ```

### Search Books

- **URL**: `/books?q=<query>`
- **Method**: `GET`
- **Description**: Search for books based on specific criteria such as title, author, or genre.
- **Query Parameters**:
  - `q`: Search query. Can be a book title, author name, or genre.
- **Example Requests**:
### HTTP
  ```http
  GET https://prasbook.onrender.com/api/books?q=Harry%20Potter
  ```
### Python
  ```python
  import requests
  
  response = requests.get('https://prasbook.onrender.com/api/books?q=Harry%20Potter')
  print(response.json())
  ```
### JavaScript 
  ```javascript
  fetch('https://prasbook.onrender.com/api/books?q=Harry%20Potter')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
  ```
### Ruby 
  ```ruby
  require 'net/http'
  require 'json'
  
  uri = URI('https://prasbook.onrender.com/api/books?q=Harry%20Potter')
  response = Net::HTTP.get(uri)
  puts JSON.parse(response)
  ```
### Java
  ```java
  import java.net.HttpURLConnection;
  import java.net.URL;
  import java.io.BufferedReader;
  import java.io.InputStreamReader;
  
  public class Main {
      public static void main(String[] args) throws Exception {
          URL url = new URL("https://prasbook.onrender.com/api/books?q=Harry%20Potter");
          HttpURLConnection connection = (HttpURLConnection) url.openConnection();
          connection.setRequestMethod("GET");
  
          BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
          String inputLine;
          StringBuffer response = new StringBuffer();
  
          while ((inputLine = in.readLine()) != null) {
              response.append(inputLine);
          }
          in.close();
  
          System.out.println(response.toString());
      }
  }
  ```
### Flutter(dart)
  ```dart
  import 'package:http/http.dart' as http;
  
  void main() async {
    var response = await http.get('https://prasbook.onrender.com/api/books?q=Harry%20Potter');
    print(response.body);
  }
  ```
### C++
  ```cpp
  #include <iostream>
  #include <curl/curl.h>
  
  int main() {
      CURL *curl;
      CURLcode res;
  
      curl = curl_easy_init();
      if (curl) {
          curl_easy_setopt(curl, CURLOPT_URL, "https://prasbook.onrender.com/api/books?q=Harry%20Potter");
          res = curl_easy_perform(curl);
  
          if (res != CURLE_OK)
              std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
  
          curl_easy_cleanup(curl);
      }
  
      return 0;
  }
  ```
- **Example Response**:
### JSON
  ```json
  [
    {
      "Title": "Harry Potter and the Philosopher's Stone",
      "Authors": ["J.K. Rowling"],
      "Publisher": "Bloomsbury Publishing",
      "Published Date": "1997-06-26",
      "ISBN": "0747532699",
      "Thumbnail URL": "https://example.com/harry_potter_thumbnail.jpg"
    },
    {
      "Title": "Harry Potter and the Chamber of Secrets",
      "Authors": ["J.K. Rowling"],
      "Publisher": "Bloomsbury Publishing",
      "Published Date": "1998-07-02",
      "ISBN": "0747538492",
      "Thumbnail URL": "https://example.com/chamber_of_secrets_thumbnail.jpg"
    },
    ...
  ]
  ```

## Error Handling

The PRAS BOOK API follows standard HTTP status codes to indicate the success or failure of a request. In case of an error, additional information may be provided in the response body.

## Rate Limiting

To ensure fair usage and prevent abuse, the API may enforce rate limits on certain endpoints. Please refer to the response headers for information on rate limiting.
