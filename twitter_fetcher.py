# twitter_fetcher.py
import streamlit as st
import openai
import requests
import datetime as dt
import json
import concern

openai.api_key = st.secrets["OPENAI_API_KEY"]
twitter_bearer_token = st.secrets.get("TWITTER_BEARER_TOKEN", None)

def fetch_tweets(city, sectors, max_results=20):
    if not twitter_bearer_token:
        st.error("No Twitter Bearer Token provided.")
        return []

    # Construct a query: we include the city name and the sectors as keywords
    query_terms = " OR ".join(sectors)
    query = f"({query_terms}) ({city}) lang:en -is:retweet"

    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {twitter_bearer_token}"}
    params = {
        "query": query,
        "max_results": str(max_results),
        "tweet.fields": "created_at,lang,text"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        st.error(f"Twitter API Error: {response.status_code} - {response.text}")
        return []

    data = response.json()
    tweets = data.get("data", [])
    # Return only English tweets
    return [t["text"] for t in tweets if t.get("lang") == "en"]

def analyze_concerns(sectors, departments, city, tweets):
    if not tweets:
        return []

    tweets_text = "\n\n".join(tweets)
    today = dt.datetime.now().strftime("%Y-%m-%d")

    system_prompt = "You are an AI assistant analyzing social media (tweets) for public concerns."
    user_prompt = f"""
    Today is {today}.
    Tweets from {city}:
    {tweets_text}

    Instructions:
    1. Identify key public concerns related to these sectors: {sectors}
    2. Assign each concern to a corresponding department from this list: {departments}
    3. Determine the degree: 'Trending' (3), 'Emerging' (2), or 'Sporadic' (1).
    4. Return JSON in the format:
    [
      {{
        "sector": "Sector Name",
        "department": "Department Name",
        "concern": "Brief description",
        "degree": "Trending/Emerging/Sporadic",
        "degree_level": 3/2/1
      }}
    ]

    If no concerns, return an empty list.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()
    try:
        data = json.loads(content)
        return [concern.Concern.from_dict(item) for item in data]
    except json.JSONDecodeError:
        st.warning("Failed to parse JSON from the AI response. The response was:")
        st.write(content)
        return []

def get_concerns(sectors, departments, city):
    sector_names = [s.sector if hasattr(s, 'sector') else s for s in sectors]
    tweets = fetch_tweets(city, sector_names)
    return analyze_concerns(sector_names, departments, city, tweets)
