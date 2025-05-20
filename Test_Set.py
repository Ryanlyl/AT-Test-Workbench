import serial
import time

def send_at_command(port, baudrate, command, timeout=10):
    """
    Sends an AT command to the specified serial port and returns the response lines.
    """
    with serial.Serial(port, baudrate, timeout=timeout) as ser:
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        ser.write((command + '\r\n').encode('utf-8'))

        response = []
        start_time = time.time()
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                response.append(line)
                if line.upper() in ("OK", "ERROR"):
                    break
            if time.time() - start_time > timeout:
                break
        return response

def test_multiple_commands(port, baudrate, commands, success_keywords=None, timeout=2):
    """
    Test multiple AT commands and return the response and result for each command.

    :param commands: list of AT command strings
    :param success_keywords: dict mapping command -> success
    :return: dict mapping command -> {'response': [...], 'ok': True/False}
    """
    results = {}
    for cmd in commands:
        resp = send_at_command(port, baudrate, cmd, timeout=timeout)
        # check if the response contains "OK" or "ERROR"
        ok = any(line.upper() == "OK" for line in resp)

        # if success_keywords:
        if success_keywords and cmd in success_keywords:
            key = success_keywords[cmd]
            if isinstance(key, (list, tuple)):
                ok = any(any(k in line for k in key) for line in resp)
            else:
                ok = any(key in line for line in resp)

        results[cmd] = {
            'response': resp,
            'ok': ok
        }
    return results

def read_commands_from_file(filename):
    with open(filename, 'r') as file:
        commands = [line.strip() for line in file if line.strip()]
    return commands

def read_dict_from_file(filename):
    result = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # drop the space, { and commends
            if not line or line.startswith('{') or line.startswith('}') or line.startswith('#'):
                continue
            # drop the comma
            if line.endswith(','):
                line = line[:-1].strip()
            # find the : to separate
            sep = line.find(':')
            if sep < 0:
                continue
            key_part = line[:sep].strip()
            val_part = line[sep+1:].strip()
            # drop '"
            if (key_part[0] in ('"', "'") and key_part[-1] == key_part[0]):
                key = key_part[1:-1]
            else:
                continue
            if (val_part[0] in ('"', "'") and val_part[-1] == val_part[0]):
                val = val_part[1:-1]
            else:
                continue
            result[key] = val
    return result 

if __name__ == "__main__":
    port = input("Please input the port name(default: /dev/ttyUSB0): ") or "/dev/ttyUSB0"
    baudrate = input("Please input the baudrate(default: 115200): ") or "115200"
    baudrate = int(baudrate)

    # Test commands
    commands = read_commands_from_file('commands.txt')

    # Optional, can specify success keywords for each command
    success_keywords = read_dict_from_file('keywords.txt')

    results = test_multiple_commands(port, baudrate, commands, success_keywords)

    # Print results
    for cmd, info in results.items():
        print(f"\n>>> Command: {cmd}")
        print("Response:")
        for line in info['response']:
            print("  " + line)
        if info['ok']:
            print("=>Success")
        else:
            print("=>Failed")

    with open('results.txt', 'w', encoding='utf-8') as f:
        for cmd, info in results.items():
            print(f"\n>>> Command: {cmd}", file=f)
            print("Response:", file=f)
            for line in info['response']:
                print("  " + line, file=f)
            if info['ok']:
                print("=>Success", file=f)
            else:
                print("=>Failed", file=f)