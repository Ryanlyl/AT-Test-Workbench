# AT-Test-Workbench
A Python script for testing serial communication with a development board.  
It reads commands and keywords from files, communicates over a serial port, and logs results.

## Prerequisites

- **Python 3.x**  
- **pip3**  
- A development board connected via serial port  
- Files `commands.txt`, `keywords.txt`, and `results.txt` in the same directory as `Test_Set.py`

## Installation

Install the required Python library:

```bash
pip3 install pyserial
