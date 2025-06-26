# GitHub Star Tagger

A tool to pull your GitHub starred repositories and organize them with custom tags, making it easier to manage and find projects among hundreds or thousands of stars.

**Why?**
GitHub’s default star list offers little organization, making it hard to remember why you starred something or to find projects you want to revisit. This tool lets you tag stars by categories like "Want to Try," "For Learning," "Tried & Disliked," or any custom tag you need[1][2].

---

## Features

- Fetches all your starred repositories from GitHub.
- Lets you assign multiple custom tags to each repository.
- Filter and search your stars by tag or keyword.
- Keeps your tagging data private and local (unless you choose to sync).
- Simple interface focused on speed for large star lists (1000+ repos).

---

## Example Tags

- todo
- python
- homelab
- work

---

## Getting Started

Easiest way is with docker

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/pypeaday/gh-star-sorter.git
    cd gh-star-sorter
    ```
2.  **Create a GitHub Personal Access Token (PAT):**
    - Easiest way is with the github cli `gh auth token`
    - Add the token to you .env file - see [.env.example](.env.example)

3.  **Configure Kanboard Integration (Optional):**
    If you don't use kanboard go to step 4.
    To create Kanboard tickets directly from the application, you need to provide your Kanboard instance details. Add the following variables to your `.env` file:
    ```
    KANBOARD_URL="https://your-kanboard-instance.com/jsonrpc.php"
    KANBOARD_API_TOKEN="your_kanboard_api_token"
    KANBOARD_PROJECT_ID="your_project_id"
    ```
    -   `KANBOARD_URL`: The full URL to your Kanboard `jsonrpc.php` endpoint.
    -   `KANBOARD_API_TOKEN`: Your personal API token from Kanboard's settings.
    -   `KANBOARD_PROJECT_ID`: The ID of the project where you want to create tickets.

4.  **Run docker compose:**
    ```bash
    docker compose up -d
    ```

5.  **Access the application:**
    Open your browser and navigate to `http://localhost:8000`.

---

## Usage

-   **Sync Stars**: Click the **Sync Stars** button to fetch all your starred repositories from GitHub and save them to the local `gh_stars.db` database. This only needs to be done periodically to pull in new stars.
-   **Tagging**: In the "Tags" column for each repository, type your tags (comma-separated) and click **Save**. The tags will be saved instantly.
-   **Filtering**: Click on any tag button at the top of the page to filter the list and show only repositories with that tag. Click **All** to clear the filter.
-   **Sorting**: Click on the **Name** or **Stars** table headers to sort the repositories. Clicking again will reverse the sort order.

---

## Privacy

- Your tag data is stored locally by default.
- No analytics or data collection.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

MIT License

---
