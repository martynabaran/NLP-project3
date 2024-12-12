# Verb Association Discovery App

This project focuses on the development of a system for the automatic processing of texts to identify verbs and their associated nouns. The goal of the project is to create a tool that extracts specific parts of speech from texts, stores them in data structures (e.g., dictionaries), and allows for the analysis of relationships between various verbs. The system enables dynamic construction of a verb database and its contexts from texts, without the need for a pre-defined list of verbs. Additionally, the project supports performing set operations (e.g., union, intersection) on verb-related collections, enabling complex analysis and comparison of vocabulary.

## Features
- **Verb Extraction**: Extract verbs and their associated nouns from text.
- **Dynamic Verb Database**: Automatically build a verb dictionary based on the context in which verbs appear in the text.
- **Set Operations**: Perform set operations like union, intersection, and difference on verb-related collections.
- **User Interface**: A simple graphical user interface (GUI) built with `tkinter` to interact with the system.

## Requirements
- Python 3.x
- Installed libraries:
  - `tkinter` (for GUI)
  - `setOperationsHandler` (for handling set operations)
  - `textAsADict.textToDictionary` (for converting text to dictionary)

## Setup Instructions

1. Clone or download the repository.

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
3. Run the application:
   ```bash
   python verb_app.py
4. The application will open a graphical user interface where you can:
- Enter a verb (in its infinitive form) in the first text box.
- Enter a comma-separated list of verbs in the second text box.
- Select an operation (Sum, Intersection, Difference) to apply to the set of verbs.
- The result of the operation will be displayed in the scrollable text area.

## How It Works

- **Verb Input**: The user can enter a verb in its infinitive form in the first text box, which is then used as the reference verb.
- **Set of Verbs**: The user can provide a comma-separated list of verbs in the second input field to compare with the reference verb.
- **Set Operations**: The user can choose from three set operations:
  - **Sum**: Union of the verb sets.
  - **Intersection**: Common verbs between the sets.
  - **Difference**: Verbs in the first set but not in the second set.
- **Result**: After selecting an operation, the result is calculated and displayed in the text area below the operation buttons.

## Example
1. Enter "run" in the first text box.
2. Enter "jump, swim, run" in the second text box.
3. Click the "Intersection" button.
4. The result will display "run", as it is the only verb common to both sets.
