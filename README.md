# Retrodrop Telegram Bot

Retrodrop is a Telegram bot that interacts with users, tracks engagement, and rewards users based on their participation in a Telegram chat. The bot is designed to integrate with a MySQL database for tracking user statistics.

## Features

- Tracks user messages and activity
- Rewards users based on specific actions
- Penalizes spammy or short messages
- Displays leaderboards for top participants
- User login and score management

## Project Structure

- **handlers/**: Contains all the command and message handlers for the bot.
- **database/**: Manages database connections and interactions with MySQL.
- **Dockerfile**: Builds the bot into a Docker container.
- **docker-compose.yml**: Sets up the bot and MySQL service with Docker Compose.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11 or later
- Poetry (for dependency management)

### Local Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/shukranjs/retrodrop-bot.git
   cd retrodrop-bot


2. Install dependencies using Poetry:


3. Copy the `.env.example` file to `.env` and set up your environment variables:


4. Run the bot locally:


### Running with Docker

1. run: 
    - chmod +x run.sh
    - ./run.sh

