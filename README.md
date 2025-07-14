# Discord MLX Bot

This project is a simple Discord bot that utilizes an MLX model to generate responses based on user messages in a channel. The bot listens for messages and replies using the model's output.

## Project Structure

```
discord-mlx-bot
├── src
│   ├── bot.py          # Main logic for the Discord bot
│   └── ml_model.py     # Handles loading the MLX model and generating responses
├── .env                # Environment variables for the bot
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd discord-mlx-bot
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   ```

## Usage

1. **Run the bot:**
   ```bash
   python src/bot.py
   ```

2. **Interact with the bot in your Discord server.** The bot will respond to messages in channels where it has permission to read and send messages.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.