# Email Cleaner AI

Email Cleaner AI is a tool designed to help users manage their email inbox by identifying and deleting unnecessary emails, thereby freeing up space. This project leverages AI techniques to enhance the email cleaning process.

## Features

- Automatically identifies unnecessary emails based on predefined criteria.
- Deletes unwanted emails to help manage inbox space.
- Easy integration with existing email services.

## Installation

To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage

To start the email cleaning process, run the main application:

```
python src/main.py
```

## Project Structure

```
email-cleaner-ai
├── src
│   ├── main.py          # Entry point of the application
│   ├── agent
│   │   └── email_agent.py  # Contains the EmailAgent class
│   ├── utils
│   │   └── email_utils.py   # Utility functions for email handling
│   └── types
│       └── __init__.py      # Custom types and data structures
├── requirements.txt      # List of dependencies
├── setup.py              # Packaging configuration
└── README.md             # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.