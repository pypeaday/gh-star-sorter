## Project: GitHub Star Tagger

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

- Want to Try
- For Learning
- Tried & Disliked (but don't want to unstar)
- Favorites
- Reference

---

## Getting Started

Follow these steps to set up and run the application locally.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/gh-star-sorter.git
    cd gh-star-sorter
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a GitHub Personal Access Token (PAT):**
    -   Go to your [GitHub Developer settings](https://github.com/settings/tokens).
    -   Click **Generate new token** and select **Generate new token (classic)**.
    -   Give your token a descriptive name (e.g., `gh-star-sorter`).
    -   Select the following scopes: `read:user` and `public_repo`.
    -   Click **Generate token** and copy the token immediately. You won't be able to see it again.

5.  **Set the environment variable:**
    Create a file named `.env` in the root of the project directory and add your token to it like this:
    ```
    GITHUB_TOKEN="your_personal_access_token_here"
    ```
    The application uses `python-dotenv` to load this variable automatically. Alternatively, you can use a tool like `direnv`.

6.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

7.  **Open in your browser:**
    Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

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

## Alternatives

- [Star Order](https://starorder.akring.com): Native app for Apple devices with tagging and favorites[1][3].
- [Star Manager](https://star-manager.vercel.app): AI-powered star organization and insights[4].
- [Astral](https://astralapp.com): Web-based GitHub star organizer with tags[2].

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

MIT License

---

> “If you starred thousands of repos just like me, this app might be helpful too.”[1]

Citations:
[1] A new way to manage GitHub stars with my app - Star Order - Reddit https://www.reddit.com/r/github/comments/15w54ep/a_new_way_to_manage_github_stars_with_my_app_star/
[2] How to categorize Github stars? - DEV Community https://dev.to/defman/how-to-categorize-github-stars-5akc
[3] StarOrder-GitHub star manager 4+ - App Store - Apple https://apps.apple.com/ru/app/starorder-github-star-manager/id1182745159?l=en-GB&mt=12
[4] Star Manager https://star-manager.vercel.app
[5] How to group git repositories by keyword/tag - Stack Overflow https://stackoverflow.com/questions/14247455/how-to-group-git-repositories-by-keyword-tag
[6] Astral: Organize Your GitHub Stars With Ease https://astralapp.com
[7] Organize your GitHub stars with Astral - Alexandre Nédélec https://techwatching.dev/posts/astral
[8] Astral - Organize Your GitHub Stars With Ease - Cloudron Forum https://forum.cloudron.io/topic/4261/astral-organize-your-github-stars-with-ease
[9] Best practices for managing GitHub organizations - Graphite https://graphite.dev/guides/managing-github-organizations
[10] GitHub Organizations Best Practices - Blog - GitProtect.io https://gitprotect.io/blog/github-organizations-best-practices/