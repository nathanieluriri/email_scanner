
```markdown
## Getting Started

Before you start anything, make sure to set up a virtual environment:

```bash
python -m venv venv
```

### Install Requirements

After activating your virtual environment, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Run the Application

Once everything is set up, run the main script:

```bash
python main.py
```

You should see the output in the command line.
```

```markdown
## Project Workflow

This project processes emails using a custom-built NER (Named Entity Recognition) system and saves the extracted data into Excel files. Here's how it works:

### 1. Read and Save Emails
The system reads and extracts emails, then stores them in a JSON file for processing.

```python
from emailll.read_email import read_this_email

read_this_email()
# ➤ Extracts emails and saves them to `emailll/email.json`
```

### 2. Extract Entities from Emails
It loads the saved emails and processes them using a custom NER system based on a fine-tuned T5 model combined with rule-based tokenization.

```python
from utils import extract_email_data_into_object

extracted_data = extract_email_data_into_object()
```

### 3. Save Extracted Data to Excel
The extracted data is flattened and written to a new Excel workbook. Each file is timestamped to avoid overwriting and to help identify the latest file.

```python
from utils import save_sheet

save_sheet(extracted_data)
# ➤ Output saved as a timestamped Excel file
```

### 📌 Bonus: Handling Failures
In cases where the NER system fails to make predictions, those email groups are saved for review:

- Failed predictions are stored inside the `emailll/Failures/` directory.
- Each failure file is also timestamped with the current date.

---

This setup allows for easy tracking, debugging, and improvement of the system's performance over time.
```

