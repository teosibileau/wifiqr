import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from wifiqr.generator import main, generate_wifi_qr, WiFiQRGenerator
import os


class TestMainCLI:
    """Test class for the main CLI function."""
    
    @pytest.fixture
    def runner(self):
        """Click test runner fixture."""
        return CliRunner()
    
    @pytest.fixture
    def mock_qr_image(self):
        """Mock QR image fixture."""
        mock_img = MagicMock()
        mock_img.save = MagicMock()
        return mock_img
    
    @pytest.fixture
    def env_vars(self):
        """Environment variables fixture."""
        return {
            'WIFI_SSID': 'test_network',
            'WIFI_PASSWORD': 'test_password',
            'WIFI_ENCRYPTION': 'WPA'
        }
    
    @patch('wifiqr.generator.WiFiQRGenerator')
    @patch('wifiqr.generator.load_dotenv')
    def test_main_with_env_vars_success(self, mock_load_dotenv, mock_wifi_qr_generator, runner, mock_qr_image, env_vars):
        """Test successful execution with environment variables."""
        mock_generator_instance = MagicMock()
        mock_generator_instance.create_image.return_value = mock_qr_image
        mock_wifi_qr_generator.return_value = mock_generator_instance
        
        with patch.dict(os.environ, env_vars):
            result = runner.invoke(main, ['--output', 'test.jpg'])
        
        assert result.exit_code == 0
        assert "JPG saved to test.jpg" in result.output
        mock_wifi_qr_generator.assert_called_once_with('test_network', 'test_password', 'WPA')
        mock_generator_instance.create_image.assert_called_once()
        mock_generator_instance.save_image.assert_called_once_with(mock_qr_image, 'test.jpg')
    
    @patch('wifiqr.generator.WiFiQRGenerator')
    @patch('wifiqr.generator.load_dotenv')
    def test_main_with_cli_options_success(self, mock_load_dotenv, mock_wifi_qr_generator, runner, mock_qr_image):
        """Test successful execution with CLI options."""
        mock_generator_instance = MagicMock()
        mock_generator_instance.create_image.return_value = mock_qr_image
        mock_wifi_qr_generator.return_value = mock_generator_instance
        
        result = runner.invoke(main, [
            '--output', 'test.jpg',
            '--ssid', 'cli_network',
            '--password', 'cli_password',
            '--encryption', 'WEP'
        ])
        
        assert result.exit_code == 0
        assert "JPG saved to test.jpg" in result.output
        mock_wifi_qr_generator.assert_called_once_with('cli_network', 'cli_password', 'WEP')
        mock_generator_instance.create_image.assert_called_once()
        mock_generator_instance.save_image.assert_called_once_with(mock_qr_image, 'test.jpg')
    
    @patch('wifiqr.generator.load_dotenv')
    def test_main_missing_ssid_error(self, mock_load_dotenv, runner):
        """Test error when SSID is missing."""
        env_vars = {'WIFI_PASSWORD': 'test_password'}
        
        with patch.dict(os.environ, env_vars, clear=True):
            result = runner.invoke(main, ['--output', 'test.jpg'])
        
        assert result.exit_code == 1
        assert "SSID is required" in result.output
    
    @patch('wifiqr.generator.load_dotenv')
    def test_main_missing_password_error(self, mock_load_dotenv, runner):
        """Test error when password is missing."""
        env_vars = {'WIFI_SSID': 'test_network'}
        
        with patch.dict(os.environ, env_vars, clear=True):
            result = runner.invoke(main, ['--output', 'test.jpg'])
        
        assert result.exit_code == 1
        assert "Password is required" in result.output
    
    @patch('wifiqr.generator.load_dotenv')
    def test_main_invalid_encryption_error(self, mock_load_dotenv, runner):
        """Test error when encryption type is invalid."""
        env_vars = {
            'WIFI_SSID': 'test_network',
            'WIFI_PASSWORD': 'test_password'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            result = runner.invoke(main, [
                '--output', 'test.jpg',
                '--encryption', 'INVALID'
            ])
        
        assert result.exit_code == 1
        assert "Invalid encryption type 'INVALID'" in result.output
        assert "WPA, WEP, nopass" in result.output
    
    @patch('wifiqr.generator.WiFiQRGenerator')
    @patch('wifiqr.generator.load_dotenv')
    def test_main_generate_wifi_qr_error(self, mock_load_dotenv, mock_wifi_qr_generator, runner):
        """Test error handling when WiFiQRGenerator raises ValueError."""
        mock_wifi_qr_generator.side_effect = ValueError("QR generation failed")
        
        env_vars = {
            'WIFI_SSID': 'test_network',
            'WIFI_PASSWORD': 'test_password'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            result = runner.invoke(main, ['--output', 'test.jpg'])
        
        assert result.exit_code == 1
        assert "QR generation failed" in result.output
    
    @patch('wifiqr.generator.WiFiQRGenerator')
    @patch('wifiqr.generator.load_dotenv')
    def test_main_default_encryption_wpa(self, mock_load_dotenv, mock_wifi_qr_generator, runner, mock_qr_image):
        """Test default encryption is WPA when not specified."""
        mock_generator_instance = MagicMock()
        mock_generator_instance.create_image.return_value = mock_qr_image
        mock_wifi_qr_generator.return_value = mock_generator_instance
        
        env_vars = {
            'WIFI_SSID': 'test_network',
            'WIFI_PASSWORD': 'test_password'
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            result = runner.invoke(main, ['--output', 'test.jpg'])
        
        assert result.exit_code == 0
        mock_wifi_qr_generator.assert_called_once_with('test_network', 'test_password', 'WPA')
    
    @patch('wifiqr.generator.WiFiQRGenerator')
    @patch('wifiqr.generator.load_dotenv')
    def test_main_cli_overrides_env_vars(self, mock_load_dotenv, mock_wifi_qr_generator, runner, mock_qr_image):
        """Test that CLI options override environment variables."""
        mock_generator_instance = MagicMock()
        mock_generator_instance.create_image.return_value = mock_qr_image
        mock_wifi_qr_generator.return_value = mock_generator_instance
        
        env_vars = {
            'WIFI_SSID': 'env_network',
            'WIFI_PASSWORD': 'env_password',
            'WIFI_ENCRYPTION': 'WEP'
        }
        
        with patch.dict(os.environ, env_vars):
            result = runner.invoke(main, [
                '--output', 'test.jpg',
                '--ssid', 'cli_network',
                '--password', 'cli_password',
                '--encryption', 'nopass'
            ])
        
        assert result.exit_code == 0
        mock_wifi_qr_generator.assert_called_once_with('cli_network', 'cli_password', 'nopass')
    
    @patch('wifiqr.generator.WiFiQRGenerator')
    @patch('wifiqr.generator.load_dotenv')
    def test_main_partial_cli_options(self, mock_load_dotenv, mock_wifi_qr_generator, runner, mock_qr_image):
        """Test partial CLI options with environment variables."""
        mock_generator_instance = MagicMock()
        mock_generator_instance.create_image.return_value = mock_qr_image
        mock_wifi_qr_generator.return_value = mock_generator_instance
        
        env_vars = {
            'WIFI_SSID': 'env_network',
            'WIFI_PASSWORD': 'env_password'
        }
        
        with patch.dict(os.environ, env_vars):
            result = runner.invoke(main, [
                '--output', 'test.jpg',
                '--encryption', 'WEP'
            ])
        
        assert result.exit_code == 0
        mock_wifi_qr_generator.assert_called_once_with('env_network', 'env_password', 'WEP')
    
    @patch('wifiqr.generator.WiFiQRGenerator')
    @patch('wifiqr.generator.load_dotenv')
    def test_main_nopass_encryption(self, mock_load_dotenv, mock_wifi_qr_generator, runner, mock_qr_image):
        """Test nopass encryption type."""
        mock_generator_instance = MagicMock()
        mock_generator_instance.create_image.return_value = mock_qr_image
        mock_wifi_qr_generator.return_value = mock_generator_instance
        
        result = runner.invoke(main, [
            '--output', 'test.jpg',
            '--ssid', 'open_network',
            '--password', '',
            '--encryption', 'nopass'
        ])
        
        assert result.exit_code == 0
        mock_wifi_qr_generator.assert_called_once_with('open_network', None, 'nopass')


class TestWiFiQRGenerator:
    """Test class for the WiFiQRGenerator class."""
    
    @pytest.fixture
    def mock_qr_code(self):
        """Mock QR code fixture."""
        mock_qr = MagicMock()
        mock_img = MagicMock()
        mock_img.size = (400, 400)
        mock_qr.make_image.return_value = mock_img
        return mock_qr
    
    @pytest.fixture
    def mock_pil_image(self):
        """Mock PIL Image fixture."""
        mock_img = MagicMock()
        mock_img.size = (400, 400)
        return mock_img
    
    def test_init_success(self):
        """Test successful initialization."""
        generator = WiFiQRGenerator('test_ssid', 'test_password', 'WPA')
        assert generator.ssid == 'test_ssid'
        assert generator.password == 'test_password'
        assert generator.encryption == 'WPA'
    
    def test_init_default_encryption(self):
        """Test initialization with default encryption."""
        generator = WiFiQRGenerator('test_ssid', 'test_password')
        assert generator.encryption == 'WPA'
    
    def test_init_missing_ssid_error(self):
        """Test error when SSID is missing during initialization."""
        with pytest.raises(ValueError, match="SSID must be provided"):
            WiFiQRGenerator('', 'test_password', 'WPA')
        
        with pytest.raises(ValueError, match="SSID must be provided"):
            WiFiQRGenerator(None, 'test_password', 'WPA')
    
    def test_init_missing_password_error(self):
        """Test error when password is missing for encrypted networks."""
        with pytest.raises(ValueError, match="Password must be provided for encrypted networks"):
            WiFiQRGenerator('test_ssid', '', 'WPA')
        
        with pytest.raises(ValueError, match="Password must be provided for encrypted networks"):
            WiFiQRGenerator('test_ssid', None, 'WEP')
    
    def test_init_nopass_no_password(self):
        """Test successful initialization with nopass encryption and no password."""
        generator = WiFiQRGenerator('open_ssid', None, 'nopass')
        assert generator.ssid == 'open_ssid'
        assert generator.password is None
        assert generator.encryption == 'nopass'
    
    def test_encode_wifi_string_wpa(self):
        """Test WiFi string encoding for WPA."""
        generator = WiFiQRGenerator('test_ssid', 'test_password', 'WPA')
        result = generator.encode_wifi_string()
        assert result == 'WIFI:S:test_ssid;T:WPA;P:test_password;;'
    
    def test_encode_wifi_string_wep(self):
        """Test WiFi string encoding for WEP."""
        generator = WiFiQRGenerator('test_ssid', 'test_password', 'WEP')
        result = generator.encode_wifi_string()
        assert result == 'WIFI:S:test_ssid;T:WEP;P:test_password;;'
    
    def test_encode_wifi_string_nopass(self):
        """Test WiFi string encoding for nopass."""
        generator = WiFiQRGenerator('open_ssid', None, 'nopass')
        result = generator.encode_wifi_string()
        assert result == 'WIFI:S:open_ssid;T:nopass;P:;;'
    
    def test_generate_text_overlay_with_password(self):
        """Test text overlay generation for networks with password."""
        generator = WiFiQRGenerator('test_ssid', 'test_password', 'WPA')
        result = generator.generate_text_overlay(20, 400)
        
        expected = [
            ((90, 380), 'ssid: test_ssid'),
            ((90, 430), 'password: test_password')
        ]
        assert result == expected
    
    def test_generate_text_overlay_nopass(self):
        """Test text overlay generation for open networks."""
        generator = WiFiQRGenerator('open_ssid', None, 'nopass')
        result = generator.generate_text_overlay(20, 400)
        
        expected = [
            ((90, 380), 'ssid: open_ssid'),
            ((90, 430), 'password: (no password)')
        ]
        assert result == expected
    
    @patch('wifiqr.generator.Image.new')
    @patch('wifiqr.generator.ImageDraw.Draw')
    @patch('wifiqr.generator.ImageFont.truetype')
    @patch('wifiqr.generator.qrcode.QRCode')
    def test_create_image_success(self, mock_qr_code_class, mock_truetype, mock_draw, mock_image_new, mock_qr_code, mock_pil_image):
        """Test successful image creation."""
        mock_qr_code_class.return_value = mock_qr_code
        mock_image_new.return_value = mock_pil_image
        mock_truetype.return_value = MagicMock()
        mock_draw.return_value = MagicMock()
        
        generator = WiFiQRGenerator('test_ssid', 'test_password', 'WPA')
        result = generator.create_image()
        
        # Verify QR code creation
        mock_qr_code_class.assert_called_once_with(box_size=22, border=4)
        mock_qr_code.add_data.assert_called_once_with('WIFI:S:test_ssid;T:WPA;P:test_password;;')
        mock_qr_code.make.assert_called_once_with(fit=True)
        mock_qr_code.make_image.assert_called_once()
        
        # Verify canvas creation
        mock_image_new.assert_called_once_with('RGB', (827, 920), 'white')
        
        assert result == mock_pil_image
    
    @patch('wifiqr.generator.ImageFont.truetype')
    def test_get_font_success(self, mock_truetype):
        """Test successful font loading."""
        mock_truetype.return_value = MagicMock()
        
        generator = WiFiQRGenerator('test_ssid', 'test_password', 'WPA')
        font = generator._get_font()
        
        mock_truetype.assert_called_once_with("/System/Library/Fonts/Arial.ttf", 40)
        assert font == mock_truetype.return_value
    
    @patch('wifiqr.generator.ImageFont.truetype')
    @patch('wifiqr.generator.ImageFont.load_default')
    def test_get_font_fallback(self, mock_load_default, mock_truetype):
        """Test font fallback when Arial is not available."""
        mock_truetype.side_effect = OSError("Font not found")
        mock_load_default.return_value = MagicMock()
        
        generator = WiFiQRGenerator('test_ssid', 'test_password', 'WPA')
        font = generator._get_font()
        
        mock_truetype.assert_called_once_with("/System/Library/Fonts/Arial.ttf", 40)
        mock_load_default.assert_called_once()
        assert font == mock_load_default.return_value
    
    def test_save_image(self):
        """Test image saving."""
        mock_image = MagicMock()
        
        generator = WiFiQRGenerator('test_ssid', 'test_password', 'WPA')
        generator.save_image(mock_image, 'test_output.jpg')
        
        mock_image.save.assert_called_once_with('test_output.jpg', 'JPEG')


class TestGenerateWifiQR:
    """Test class for the legacy generate_wifi_qr function."""
    
    @patch('wifiqr.generator.Image.new')
    @patch('wifiqr.generator.ImageDraw.Draw')
    @patch('wifiqr.generator.ImageFont.truetype')
    @patch('wifiqr.generator.qrcode.QRCode')
    def test_legacy_function_backward_compatibility(self, mock_qr_code_class, mock_truetype, mock_draw, mock_image_new):
        """Test that legacy function still works for backward compatibility."""
        mock_qr_code = MagicMock()
        mock_qr_img = MagicMock()
        mock_qr_img.size = (400, 400)
        mock_qr_code.make_image.return_value = mock_qr_img
        mock_pil_image = MagicMock()
        mock_qr_code_class.return_value = mock_qr_code
        mock_image_new.return_value = mock_pil_image
        mock_truetype.return_value = MagicMock()
        mock_draw.return_value = MagicMock()
        
        result = generate_wifi_qr('test_ssid', 'test_password', 'WPA')
        
        mock_qr_code.add_data.assert_called_once_with('WIFI:S:test_ssid;T:WPA;P:test_password;;')
        assert result == mock_pil_image