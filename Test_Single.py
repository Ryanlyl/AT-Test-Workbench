import serial
import time

def send_at_command(port, baudrate, command, timeout=2):
    """
    Sends an AT command to the specified serial port and returns the response lines.

    :param port: Serial port device (e.g., '/dev/ttyUSB0' or 'COM3')
    :param baudrate: Baud rate for the serial connection (e.g., 115200)
    :param command: AT command string (without CRLF)
    :param timeout: Read timeout in seconds
    :return: List of response lines
    """
    # Open serial connection
    with serial.Serial(port, baudrate, timeout=timeout) as ser:
        # Clear buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        # Send command with CRLF
        full_command = command + '\r\n'
        ser.write(full_command.encode('utf-8'))

        response = []
        start_time = time.time()
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                response.append(line)
                # Stop if we detect standard terminators
                if line.upper() in ("OK", "ERROR"):
                    break
            # Timeout condition
            if (time.time() - start_time) > timeout:
                break

        return response

if __name__ == "__main__":
    # Configuration
    port = 'COM3'                           # Update this to your actual serial port
    baudrate = 115200                       # Match your Ameba Z2 baud rate
    at_command = 'ATW0=MatterOnly'          # The ATC command you want to test

    print(f"Sending command: {at_command} on {port} at {baudrate} baud")
    resp_lines = send_at_command(port, baudrate, at_command)

    print("Response received:")
    for line in resp_lines:
        print(f"  {line}")

    # Basic check for success
    if "[ATW0]: _AT_WLAN_SET_SSID_ [MatterOnly]" in [l for l in resp_lines]:
        print("AT command executed successfully.")
    else:
        print("AT command failed or did not return OK.")

