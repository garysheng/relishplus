# RelishPlus 🍔

An automated meal ordering system for Relish/ezCater that helps Gauntlet AI students easily order their weekly subsidized meals.

## Features

- Automated weekly meal ordering through Relish/ezCater
- Support for $20 daily meal subsidy (both lunch and dinner)
- Dietary restriction support (vegetarian, vegan, gluten-free, etc.)
- Smart meal selection prioritizing healthy options
- Maximizes your subsidy by ordering at least $15 worth of food per meal
- Secure handling of credentials

## Prerequisites

- Python 3.11 or higher
- Poetry for dependency management
- A Relish/ezCater account with Gauntlet AI student access
- OpenAI API key

## Step-by-Step Setup for Gauntlet Students

1. First, ensure you have Python 3.11+ installed:
   ```bash
   python --version
   ```
   If not, download it from [python.org](https://www.python.org/downloads/)

2. Install Poetry (package manager):
   ```bash
   # On macOS/Linux:
   curl -sSL https://install.python-poetry.org | python3 -

   # On Windows:
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```

3. Clone the repository:
   ```bash
   git clone https://github.com/garysheng/relishplus.git
   cd relishplus
   ```

4. Install dependencies:
   ```bash
   poetry install
   ```

5. Create your configuration file:
   ```bash
   cp config.json.example config.json
   ```
   Edit `config.json` to set your dietary preferences and restrictions.

6. Set up your credentials by creating a `.env` file:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   RELISH_EMAIL=your_gauntlet_email@gauntletai.com
   RELISH_PASSWORD=your_relish_password
   ```

## Usage

Run the ordering system:

```bash
poetry run python -m relishplus
```

The system will:
1. Log into your Relish account
2. Navigate through the next 6 days
3. For each day:
   - Order lunch if not already ordered
   - Order dinner if not already ordered
   - Ensure at least $15 worth of food per meal
   - Follow your dietary restrictions
   - Prioritize healthy options

### Important Notes

- The Relish login flow can be buggy - sometimes it shows an incorrect password error even with correct credentials. If this happens, try running the automation again.
- The system will skip days that are grayed out or unavailable
- Each meal order will try to use at least $15 of your $20 subsidy
- Orders are placed one at a time to ensure proper tracking
- The automation runs locally on your machine - no credentials are sent anywhere else

## Troubleshooting

1. **Login Issues**: The Relish login system can be temperamental. If you get a "wrong password" error:
   - Double-check your credentials in `.env`
   - Try running the automation again
   - If issues persist, try logging in manually on the website first

2. **Order Not Completing**: If an order gets stuck:
   - Check if the restaurant is still accepting orders
   - Verify your subsidy is still available
   - Try running the automation again

3. **Dietary Restrictions**: If orders don't match your preferences:
   - Verify your settings in `config.json`
   - Some restaurants may not properly tag their dietary options
   - Consider being less restrictive if too few options are available

## Security

- Your credentials are stored locally in the `.env` file
- Never commit your `.env` file to version control
- The automation runs entirely on your local machine
- Your OpenAI API key is only used for navigation logic

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details # relishplus
