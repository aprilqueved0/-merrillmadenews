import feedparser
import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load Slack token from environment variable
slack_token = os.environ.get('SLACK_API_TOKEN')
client = WebClient(token=slack_token)

# Define your Slack channel name or ID (ensure your bot has access)
SLACK_CHANNEL = "news-alerts"

# Author feed URLs
FEEDS = {
    "Paul Kiefer": "https://www.washingtonpost.com/arcio/rss/author/Paul-Kiefer/?itid=ap_paul-kiefer",
    "Daranee Balachandar": "https://www.washingtonpost.com/arcio/rss/author/Daranee-Balachandar/?itid=ap_daranee-balachandar",
    "Robert Stewart": "https://veritenews.org/author/robert-stewart/feed/",
    "Aidan Hughes": "https://insideclimatenews.org/profile/aidan-hughes/feed/",
    "Antonia Navarro": "https://azcir.org/news/author/anavarro/feed/",
    "Shaela Foster": "https://www.baltimoresun.com/author/shaela-foster/feed/"
}

CACHE_FILE = "seen_articles.json"

FEEDS = {
    "Paul Kiefer": "https://www.washingtonpost.com/arcio/rss/author/Paul-Kiefer/?itid=ap_paul-kiefer",
    "Daranee Balachandar": "https://www.washingtonpost.com/arcio/rss/author/Daranee-Balachandar/?itid=ap_daranee-balachandar",
    "Robert Stewart": "https://veritenews.org/author/robert-stewart/feed/",
    "Aidan Hughes": "https://insideclimatenews.org/profile/aidan-hughes/feed/",
    "Adriana Navarro": "https://azcir.org/news/author/anavarro/feed/",
    "Shaela Foster": "https://www.baltimoresun.com/author/shaela-foster/feed/"
}

CACHE_FILE = "seen_articles.json"

# Load previously seen article IDs from file
def load_seen_articles():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

# Save updated seen article IDs to file
def save_seen_articles(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Post message to Slack
def post_to_slack(author, title, link):
    message = f"*{author}* just published:\n<{link}|{title}>"
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message,
            unfurl_links=True,
            unfurl_media=True
        )
        print(f"Posted to Slack: {title}")
    except SlackApiError as e:
        print(f"Slack error: {e.response['error']}")

# Main logic to check feeds and notify on new articles
def check_feeds():
    seen = load_seen_articles()

    for author, url in FEEDS.items():
        print(f"Checking feed for {author}")
        feed = feedparser.parse(url)

        if author not in seen:
            seen[author] = []

        for entry in feed.entries:
            article_id = entry.get("id") or entry.get("link")
            if article_id and article_id not in seen[author]:
                post_to_slack(author, entry.title, entry.link)
                seen[author].append(article_id)

    save_seen_articles(seen)

# Run the script
if __name__ == "__main__":
    check_feeds()