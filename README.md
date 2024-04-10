# Event Log Extractor README

## Overview
This Python project automates the extraction of event logs from databases using a combination of SQLite databases and machine learning models. The system takes a user prompt and a CSV file to create a SQLite database. The user prompt and the database schema are then used to generate a SQL query via a large language model (OpenAI's GPT). The SQL query is executed, and the results are validated against a ground truth dataframe by calculating metrics such as precision, recall, and F1 score.

## Prerequisites
- Python 3.10
- An OpenAI API key

## Installation

1. **Clone the Repository:**
   ```
   git clone https://github.com/KiriBu10/event-log-extraction-assistant.git
   cd event-log-extraction-assistant
   ```

2. **Set up a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `.\venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **API Key Configuration:**
   - Create a file named `keys.py` in the project root directory.
   - Add your OpenAI API key to the file:
     ```python
     OPENAI_KEY = "your-openai-api-key-here"
     ```

## Usage

### Adding New Databases
- Place new CSV files in the `testDBs` directory.
- Structure your database files as follows:
  ```
  testDBs/
  ├── test1/
  │   ├── db/
  │   │   └── yourdata.csv
  │   └── ground_truth.csv
  ├── test2/
  │   ├── db/
  │   │   └── anotherdata.csv
  │   └── ground_truth.csv
  ```

### Running Test Cases
- Execute the test cases via the Jupyter notebook provided:
  ```bash
  jupyter notebook test_cases.ipynb
  ```
- Follow the instructions within the notebook to test different scenarios and database files.

## Features
- **Dynamic SQL Query Generation:** Utilizes a language model to generate SQL queries based on user inputs and database schema.
- **Automatic Database Creation:** Converts CSV files into SQLite databases.
- **Performance Metrics:** Evaluates SQL query results by comparing with ground truth data using precision, recall, and F1 score.

## Contributing

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
For support, email kiran.busch@klu.org or open an issue in the GitHub repository.

Feel free to try the system using the `test_cases.ipynb` notebook and test your own CSV files by adding them to the `testDBs` directory as described.