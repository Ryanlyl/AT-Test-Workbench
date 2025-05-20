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
```
## Usage
### Windows
1. Ensure `commands.txt`, `keywords.txt`, and `results.txt` are in the same directory as `Test_Set.py`.
2. Connect the development board to your PC.
3. Open PowerShell and navigate to the script directory:
```powershell
cd c:\\path\\to\\script
```
4. Run the script:
```powershell
python .\Test_Set.py
```
5. When prompted, enter the port name (e.g., `COM3`) and press `Enter`.
6. Press the `Enter` again to accept the default baud rate e.g. 115200.
7. Results will be displayed in the terminal and appended to `results.txt`.

### Ubuntu
1. Ensure `commands.txt`, `keywords.txt`, and `results.txt` are in the same directory as `Test_Set.py`.
2. Connect the development board to your machine.
3. Open a terminal and navigate to the script directory:
```bash
cd /path/to/script
```
4. Run the script:
```bash
python ./Test_Set.py
```
5. Press Enter to accept the default port name and baud rate when prompted.
6. Results will be displayed in the terminal and appended to `results.txt`.

## Files
- `Test_Set.py`-- Main script for AT command testing.
- `commands.txt` -- List of commands to send to the board.
- `keywords.txt` -- Keywords to search for in responses.
- `results.txt` -- Log file where results are documented.
