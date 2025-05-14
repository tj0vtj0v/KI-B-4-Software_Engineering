# Software Engineering Project

![](https://img.shields.io/badge/status-active-brightgreen)
![](https://img.shields.io/badge/python-3.12-blue.svg)
![](https://img.shields.io/github/v/release/tj0vtj0v/KI-B-4-Software_Engineering)
![](https://img.shields.io/codecov/c/github/tj0vtj0v/KI-B-4-Software_Engineering)
![](https://img.shields.io/badge/code%20style-flake8-brightgreen.svg)
![](https://img.shields.io/github/license/tj0vtj0v/KI-B-4-Software_Engineering)

This repository contains a submission project developed for the Software Engineering course in the 4th semester of the Artificial Intelligence bachelor's program at the Deggendorf Institute of Technology.
The project implements a microwave defrosting program and includes the complete Agile development process, source code, technical documentation, sprint management, and a detailed Wiki.

## Repository Structure
```
├── src/                 # Source code
├── tests/               # Unit and integration tests
├── docs/                # Task-related documents and required declarations
├── README.md            # Project overview and setup guide
├── LICENSE              # MIT License file
├── requirements.txt     # Production dependencies
└── requirements-dev.txt # Development and testing dependencies
```

## Installation

To get started with the project, follow these steps:

Clone the repository
```bash
git clone https://github.com/tj0vtj0v/KI-B-4-Software_Engineering.git Defrosting_Program
cd Defrosting_Program
```

Install dependencies

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you're contributing to the project, install the development dependencies instead:

```bash
pip install -r requirements-dev.txt
```

### Running Tests

To run the test suite with coverage:
```bash
coverage run -m pytest tests
coverage report
```

A coverage below 90% is considered a failure and will fail the CI build. You can enforce this locally with:
```bash
coverage report --fail-under=90
```

## Project Wiki

All process documentation, coding conventions, and detailed development plans are maintained in the project Wiki.

Access it here: [Project Wiki](https://github.com/tj0vtj0v/KI-B-4-Software_Engineering/wiki)

## Usage

To run the application or demo the system, use the following command:
```bash
python src/main.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Maintained by [Tjorven Burdorf](http://www.burdorf.dev). For inquiries or feedback, please reach out via email: [burdorftjorven@gmail.com](mailto:burdorftjorven@gmail.com).
