# RAWG API Technical Notes - Siege System

## 1. Base Configuration
* **Base URL:** `https://api.rawg.io/api`
* **Authentication:** API key passed as query parameter `?key=YOUR_API_KEY`.
* **Security:** API key must reside in a `.env` file (never committed to version control).

## 2. Search Endpoint & Efficiency
* **Endpoint:** `GET /games`
* **Search Parameter:** `search` (fuzzy matching).
* **Efficiency:** Use `page_size=5` in the request query to limit the payload to only the results intended for user selection.

## 3. Response Structure & Data Mapping
The API returns a paginated JSON object. Key field paths for extraction:
* **Title:** `game['name']`
* **Genres:** `genre['name']` (extracted from the `genres` array).
* **Platforms:** `item['platform']['name']` (extracted from the `platforms` array, accessing the inner `platform` dictionary).

## 4. Search Strategy
* **Selection Logic:** To ensure data integrity, the system will not auto-select the first result.
* **Workflow:** The system will fetch the top 5 matches and present them to the user for manual confirmation before proceeding to storage.

## 5. Reliability & Rate Limiting
* **Rate Limiting:** Free tier is limited to 20,000 requests per month.
* **Error Handling:**
    * `200 OK (with results)`: Proceed with parsing.
    * `200 OK (empty results)`: Handle gracefully by informing the user that no matches were found.
    * `403 Forbidden`: Validate API key.
    * `429 Too Many Requests`: Implement wait/retry logic or notify the user to avoid service suspension.

## 6. Architectural Implementation
1. **Request Module:** Use `requests` library.
2. **Client Class:** Encapsulate logic in a `RawgClient` class.
3. **Data Mapper:** Standardize API output into clean dictionaries for database ingestion.
