# urban_vibes

An AI-powered assistant designed to monitor and analyze social media concerns in your city, enabling government officials and stakeholders to understand emerging issues and craft informed, effective responses.

## Table of Contents

- [Introduction](#introduction)  
- [Features](#features)  
- [Project Structure](#project-structure)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Setting Up the Python Environment](#setting-up-the-python-environment)  
  - [Installing Dependencies](#installing-dependencies)  
  - [Setting Up Secret Keys](#setting-up-secret-keys)  
    - [OpenAI API Key](#openai-api-key)  
    - [Grok (X) API Key](#grok-x-api-key)  
    - [Streamlit Secrets](#streamlit-secrets)
- [Running the Application](#running-the-application)  
- [Usage Guide](#usage-guide)  
  - [Selecting a City](#selecting-a-city)  
  - [Choosing Sectors of Interest](#choosing-sectors-of-interest)  
  - [Viewing Concerns and Solutions](#viewing-concerns-and-solutions)  
- [Deployment](#deployment)  
  - [Deploying on Streamlit Cloud](#deploying-on-streamlit-cloud)  
  - [Using Docker](#using-docker)  
  - [Other Hosting Options](#other-hosting-options)  
- [Contributing](#contributing)  
- [License](#license)  
- [Additional Resources](#additional-resources)

---

## Introduction

**urban_vibes** is an interactive application that uses OpenAI's GPT models to analyze social media content and highlight the most pressing public concerns within a chosen U.S. city and its government sectors. Beyond merely identifying issues, **urban_vibes** suggests potential solutions as if delivered by the chief executive of the relevant department, making it a valuable tool for policymakers, city planners, and community leaders.

---

## Features

- **City Selection**: Pick from an extensive database of U.S. cities.  
- **Sector Selection**: Choose one or more sectors from a curated list representing various government departments (Education, Healthcare, Public Safety, etc.).  
- **Concern Analysis**: Obtain AI-generated summaries of trending public concerns drawn from social media inputs.  
- **Suggested Solutions**: Review AI-generated action plans and recommended steps to address identified issues, contextualized as if suggested by the department’s leader.  
- **Responsive Interface**: An interactive and user-friendly Streamlit-based UI with expandable sections and optional dark theme support.
- **Secure Secrets Management**: Integrate your API keys securely using Streamlit’s built-in secrets management.

---

## Project Structure

```bash
urban_vibes/
├── app.py               # Main Streamlit application script
├── sector_list.py       # Defines sectors and associated departments
├── concern.py           # Data class for storing concern information
├── twitter_fetcher.py              # Functions for fetching and analyzing social media trends (mock & actual)
├── gov_ceo.py           # Functions calling OpenAI API to generate department-level solutions
├── assets/
│   └── cities.csv       # CSV file containing a list of U.S. cities
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## Getting Started

### Prerequisites

- **Python 3.7 or Higher**: Tested primarily on Python 3.10, but 3.7+ should work.
- **OpenAI API Key**: Required to generate AI-based summaries and solutions.
- **Grok (X) API Key**: Required to analyze real-time social media trends (if available).
- **Streamlit**: A Python library for rapid web app development.

Before starting, ensure you have all the necessary keys and have installed Python on your system.

### Setting Up the Python Environment

1. **Check Python Installation**:
   
   Confirm that Python 3.7+ is installed:
   ```bash
   python --version
   ```
   If you do not have the appropriate version, download Python from the [official website](https://www.python.org/downloads/).

2. **Create a Virtual Environment** (Optional but Recommended):

   It’s a best practice to create a virtual environment to avoid conflicts with system-wide packages:
   ```bash
   python -m venv urban_vibes_env
   ```

3. **Activate the Virtual Environment**:

   On macOS/Linux:
   ```bash
   source urban_vibes_env/bin/activate
   ```

   On Windows (PowerShell):
   ```bash
   .\urban_vibes_env\Scripts\activate
   ```

### Installing Dependencies

Once the virtual environment is active, install the required Python packages:
```bash
pip install -r requirements.txt
```

This command installs:
- **streamlit** (for the web interface)  
- **openai** (for AI-generated content)  
- **pandas** (for data handling)  
- **datetime** (for time-based operations)

### Setting Up Secret Keys

**Important**: Do not hard-code your API keys directly into the source files. Instead, use Streamlit’s secure secrets management.

#### OpenAI API Key

1. Obtain your OpenAI API key from the [OpenAI Dashboard](https://platform.openai.com/account/api-keys).
2. Copy the key and store it securely.

#### Grok (X) API Key

1. If you have a Grok (or an X API) key, keep it handy as well.
2. If not, you may need to mock data or skip features dependent on this API.

#### Streamlit Secrets

Streamlit supports a secure secrets management system via `secrets.toml` files.

1. In your project root, create a directory named `.streamlit` if it doesn’t exist:
   ```bash
   mkdir .streamlit
   ```

2. Inside `.streamlit`, create a file named `secrets.toml`:
   ```bash
   nano .streamlit/secrets.toml
   ```

3. Add your API keys to `secrets.toml`:
   ```toml
   OPENAI_API_KEY = "sk-your-key"
   X_API_KEY = "xai-your-key"
   ```

4. Ensure `secrets.toml` is listed in your `.gitignore` (it should never be committed to version control).

In your Python code, you can access these secrets via:
```python
import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]
# For Grok usage:
grok_api_key = st.secrets.get("X_API_KEY", None)
```

---

## Running the Application

With your virtual environment active and dependencies installed, run:
```bash
streamlit run app.py
```

If successful, Streamlit will launch a local server and display a URL (like `http://localhost:8501`). Open this URL in your web browser to interact with **urban_vibes**.

---

## Usage Guide

### Selecting a City

1. On the app’s homepage, locate the **"Select a US city"** dropdown.
2. Choose a city from the provided list. The app uses `cities.csv` to populate this menu.

### Choosing Sectors of Interest

1. Below the city selection, find the **"Select Sectors of Interest"** multiselect widget.
2. Pick one or more sectors to focus the analysis (e.g., Education, Healthcare, Public Safety).

### Viewing Concerns and Solutions

1. **Get Concerns**: Click the **"Get Concerns"** button.
   - The app queries social media trends (via Grok or mock data) and displays a list of concerns related to the chosen city and sectors.

2. **View Suggested Solutions**:
   - For each listed concern, click the **"View Suggested Solution"** button.
   - An AI-generated action plan or solution, framed as if from the department’s chief executive, will appear after a brief loading period.

Use these steps to quickly understand pressing local issues and potential interventions.

---

## Deployment

You can run **urban_vibes** locally or deploy it online for wider access.

### Deploying on Streamlit Cloud

1. Push your project to a GitHub repository.
2. Create an account (if you haven’t already) on [Streamlit Cloud](https://streamlit.io/cloud).
3. Connect your GitHub repository.
4. Configure your API keys under the "Secrets" setting in Streamlit Cloud’s dashboard.
5. Launch the app from your Streamlit Cloud workspace.

For more details, consult [Streamlit’s Secrets Management documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

### Using Docker

1. **Create a Dockerfile**:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build the Docker Image**:
   ```bash
   docker build -t urban_vibes:latest .
   ```

3. **Run the Container**:
   ```bash
   docker run -p 8501:8501 -e OPENAI_API_KEY='sk-your-key' -e X_API_KEY='xai-your-key' urban_vibes:latest
   ```
   Access the app at `http://localhost:8501`.

You can also deploy this Docker image to platforms like AWS ECS, Azure Container Instances, or Google Cloud Run.

### Other Hosting Options

- **Heroku**: Use the [Streamlit on Heroku guide](https://towardsdatascience.com/deploying-streamlit-apps-on-heroku-is-dead-long-live-streamlit-cloud-8589553c31dd) for configuration tips.
- **Cloud Platforms**: AWS, Azure, and GCP all support containerized or direct Python app deployments.

---

## Contributing

Contributions are welcome! Please open issues and submit pull requests to help improve **urban_vibes**. Whether you find a bug, suggest a feature, or improve documentation, we appreciate your input.

---

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as permitted by the license.

---

## Additional Resources

- [OpenAI Documentation](https://platform.openai.com/docs/introduction)  
- [Streamlit Documentation](https://docs.streamlit.io/)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)  
- [Datetime Documentation](https://docs.python.org/3/library/datetime.html)

---

**urban_vibes** empowers local decision-makers by providing clear insights and actionable solutions derived from real-time public discourse. Get started now and help shape the future of your city!