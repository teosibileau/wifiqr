import os

import click
import qrcode
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont


class WiFiQRGenerator:
    """Class for generating WiFi QR codes with text overlay."""

    def __init__(self, ssid: str, password: str, encryption: str = "WPA"):
        """Initialize the WiFi QR generator.

        Args:
            ssid: WiFi network name
            password: WiFi password (None for open networks)
            encryption: Encryption type (WPA, WEP, nopass)
        """
        if not ssid:
            msg = "SSID must be provided"
            raise ValueError(msg)
        if not password and encryption != "nopass":
            msg = "Password must be provided for encrypted networks"
            raise ValueError(msg)

        self.ssid = ssid
        self.password = password
        self.encryption = encryption

    def encode_wifi_string(self) -> str:
        """Encode WiFi credentials into QR code string format.

        Returns:
            WiFi string in format: WIFI:S:<SSID>;T:<ENCRYPTION>;P:<PASSWORD>;;
        """
        password_str = self.password if self.password is not None else ""
        return f"WIFI:S:{self.ssid};T:{self.encryption};P:{password_str};;"

    def generate_text_overlay(self, qr_y_position: int, qr_height: int) -> list:
        """Generate text overlay data for the QR code image.

        Args:
            qr_y_position: Y position of the QR code on canvas
            qr_height: Height of the QR code

        Returns:
            List of tuples containing (position, text) for drawing
        """
        text_y = qr_y_position + qr_height - 40
        password_display = (
            self.password if self.password is not None else "(no password)"
        )

        return [
            ((90, text_y), f"ssid: {self.ssid}"),
            ((90, text_y + 50), f"password: {password_display}"),
        ]

    def create_image(self) -> Image.Image:
        """Create the complete QR code image with text overlay.

        Returns:
            PIL Image object containing QR code and text
        """
        # Generate QR code
        wifi_string = self.encode_wifi_string()
        qr = qrcode.QRCode(box_size=22, border=4)
        qr.add_data(wifi_string)
        qr.make(fit=True)
        qr_img = qr.make_image()

        # Create canvas
        canvas_width = 827
        canvas_height = 920
        canvas = Image.new("RGB", (canvas_width, canvas_height), "white")

        # Paste QR code centered at top
        qr_width, qr_height = qr_img.size
        x = (canvas_width - qr_width) // 2
        y = 20  # small margin from top
        canvas.paste(qr_img, (x, y))

        # Add text overlay
        self._add_text_to_canvas(canvas, y, qr_height)

        return canvas

    def _add_text_to_canvas(self, canvas: Image.Image, qr_y: int, qr_height: int):
        """Add text overlay to the canvas.

        Args:
            canvas: PIL Image object to draw on
            qr_y: Y position of QR code
            qr_height: Height of QR code
        """
        draw = ImageDraw.Draw(canvas)
        font = self._get_font()

        text_data = self.generate_text_overlay(qr_y, qr_height)
        for position, text in text_data:
            draw.text(position, text, fill="black", font=font)

    def _get_font(self):
        """Get font for text rendering, with fallback to default.

        Returns:
            PIL ImageFont object
        """
        try:
            return ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 40)
        except OSError:
            return ImageFont.load_default()

    def save_image(self, image: Image.Image, output_path: str) -> None:
        """Save the image to a file.

        Args:
            image: PIL Image object to save
            output_path: Path where to save the JPG file
        """
        image.save(output_path, "JPEG")


def generate_wifi_qr(ssid: str, password: str, encryption: str = "WPA") -> Image.Image:
    """Legacy function for backward compatibility.

    Args:
        ssid: WiFi network name
        password: WiFi password (None for open networks)
        encryption: Encryption type (WPA, WEP, nopass)

    Returns:
        PIL Image object containing QR code and text
    """
    generator = WiFiQRGenerator(ssid, password, encryption)
    return generator.create_image()


@click.command()
@click.option(
    "--output", "-o", type=click.Path(), required=True, help="Output file for the JPG."
)
@click.option("--ssid", "-s", envvar="WIFI_SSID", help="WiFi network name.")
@click.option("--password", "-p", envvar="WIFI_PASSWORD", help="WiFi password.")
@click.option(
    "--encryption",
    "-e",
    envvar="WIFI_ENCRYPTION",
    default="WPA",
    help="WiFi encryption type (WPA, WEP, nopass).",
)
def main(output, ssid, password, encryption):
    """Generate WiFi QR code JPG from environment variables or command line options."""
    load_dotenv()

    # Use environment variables if CLI options not provided
    if not ssid:
        ssid = os.getenv("WIFI_SSID")
    if not password:
        password = os.getenv("WIFI_PASSWORD")
    if not encryption or encryption == "WPA":
        encryption = os.getenv("WIFI_ENCRYPTION", "WPA")

    # Validate required parameters
    if not ssid:
        click.echo(
            "Error: SSID is required. Set WIFI_SSID environment variable or use --ssid option.",
            err=True,
        )
        raise click.Exit(1)

    if not password and encryption != "nopass":
        click.echo(
            "Error: Password is required. Set WIFI_PASSWORD environment variable or use --password option.",
            err=True,
        )
        raise click.Exit(1)

    # Validate encryption type
    valid_encryptions = ["WPA", "WEP", "nopass"]
    if encryption not in valid_encryptions:
        click.echo(
            f"Error: Invalid encryption type '{encryption}'. Must be one of: {', '.join(valid_encryptions)}",
            err=True,
        )
        raise click.Exit(1)

    try:
        generator = WiFiQRGenerator(ssid, password, encryption)
        img = generator.create_image()
        generator.save_image(img, output)
        click.echo(f"JPG saved to {output}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1) from None


if __name__ == "__main__":
    main()
