# wifiqr

Generate JPG WiFi QR codes from environment variables or command line options.

## Installation

This package uses Poetry for dependency management. To install:

1. Ensure you have Poetry installed: `curl -sSL https://install.python-poetry.org | python3 -`
2. Clone or download the project.
3. Run `poetry install` to install dependencies.

## Setup

### Option 1: Environment Variables (Recommended)

Create a `.env` file in the project root with your WiFi credentials:

```bash
WIFI_SSID=YourWiFiName
WIFI_PASSWORD=YourWiFiPassword
WIFI_ENCRYPTION=WPA
```

- `WIFI_ENCRYPTION` defaults to `WPA` if not specified
- Supported encryption types: `WPA`, `WEP`, `nopass`

### Option 2: Command Line Options

You can also pass WiFi credentials directly via command line options.

## Usage

### Basic Usage with Environment Variables

```bash
# Generate QR code using environment variables
poetry run python -m wifiqr.generator --output wifi.jpg
```

### Using Command Line Options

```bash
# Generate QR code with CLI options
poetry run python -m wifiqr.generator \
  --output wifi.jpg \
  --ssid "MyWiFiNetwork" \
  --password "MyPassword" \
  --encryption "WPA"
```

### Mixed Usage

CLI options will override environment variables:

```bash
# Use environment variables but override SSID
poetry run python -m wifiqr.generator \
  --output wifi.jpg \
  --ssid "DifferentNetwork"
```

### Open Networks (No Password)

```bash
# Generate QR code for open network
poetry run python -m wifiqr.generator \
  --output open_wifi.jpg \
  --ssid "OpenNetwork" \
  --encryption "nopass"
```

### Command Line Options

| Option | Short | Environment Variable | Required | Default | Description |
|--------|-------|----------------------|----------|---------|-------------|
| `--output` | `-o` | - | Yes | - | Output file path for the JPG |
| `--ssid` | `-s` | `WIFI_SSID` | Yes | - | WiFi network name |
| `--password` | `-p` | `WIFI_PASSWORD` | Yes (unless `nopass`) | - | WiFi password |
| `--encryption` | `-e` | `WIFI_ENCRYPTION` | No | `WPA` | Encryption type: `WPA`, `WEP`, `nopass` |

### Help

```bash
poetry run python -m wifiqr.generator --help
```

## Output

The tool generates a JPG image (827x920 pixels) containing:
- A WiFi QR code centered at the top
- Text below showing the SSID and password
- For open networks, password displays as "(no password)"

The QR code encodes the WiFi credentials in the format: `WIFI:S:<SSID>;T:<ENCRYPTION>;P:<PASSWORD>;;`

## Examples

### Home WiFi (WPA)
```bash
poetry run python -m wifiqr.generator --output home_wifi.jpg
```

### Office WiFi (WEP)
```bash
poetry run python -m wifiqr.generator \
  --output office_wifi.jpg \
  --ssid "OfficeNetwork" \
  --password "OfficePass123" \
  --encryption "WEP"
```

### Coffee Shop (Open Network)
```bash
poetry run python -m wifiqr.generator \
  --output cafe_wifi.jpg \
  --ssid "CoffeeShopWiFi" \
  --encryption "nopass"
```

## Development

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=wifiqr

# Run specific test class
poetry run pytest tests/test_cli.py::TestMainCLI
poetry run pytest tests/test_cli.py::TestGenerateWifiQR
```

## Dependencies

- `qrcode`: For generating QR codes
- `Pillow (PIL)`: For image manipulation and text rendering
- `python-dotenv`: For loading environment variables
- `click`: For CLI interface

## Error Handling

The tool provides clear error messages for:
- Missing required parameters (SSID/password)
- Invalid encryption types
- QR generation failures

## License

This project is open source. Please refer to the LICENSE file for details.
