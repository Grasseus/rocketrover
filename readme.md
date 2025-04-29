# Rocketrover

Rocketrover is a web controlled rover.

## Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)

---

## Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

Clone the repository using Git:

```bash
git clone https://github.com/Grasseus/rocketrover.git
```

Or download the ZIP file and extract it manually.

Then, navigate into the project directory:

```bash
cd rocketrover
```

### 2. Create a Virtual Environment

Create a virtual environment to isolate your project dependencies:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**On Windows:**

```bash
.venv\Scripts\activate
```

**On macOS/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install Project Dependencies

Install all the required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This ensures your environment has the correct versions of all dependencies.

---

## Usage

After installing the dependencies, you can run the main application script. It initializes the rover object and starts a WebSocket server on port 8080. To run the main application script, execute the following command:

```bash
python main.py
```

To deactivate the virtual environment after you're done:

```bash
deactivate
```

---
