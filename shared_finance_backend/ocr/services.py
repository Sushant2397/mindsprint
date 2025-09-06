import pytesseract
from PIL import Image
import re
from datetime import datetime
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class OCRService:
    """Service for processing receipt images and extracting data"""
    
    @staticmethod
    def extract_text_from_image(image_path):
        """Extract text from image using pytesseract"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return ""
    
    @staticmethod
    def parse_receipt_data(text):
        """Parse extracted text to extract structured data"""
        data = {
            'vendor': '',
            'invoice_no': '',
            'date': None,
            'amount': None,
            'gstin': '',
            'raw_text': text
        }
        
        if not text:
            return data
        
        # Extract vendor name (usually at the top)
        lines = text.split('\n')
        if lines:
            data['vendor'] = lines[0].strip()
        
        # Extract amount (look for currency symbols and numbers)
        amount_patterns = [
            r'₹\s*(\d+(?:\.\d{2})?)',
            r'INR\s*(\d+(?:\.\d{2})?)',
            r'Total\s*:?\s*₹?\s*(\d+(?:\.\d{2})?)',
            r'Amount\s*:?\s*₹?\s*(\d+(?:\.\d{2})?)',
            r'(\d+(?:\.\d{2})?)\s*₹',
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    data['amount'] = Decimal(match.group(1))
                    break
                except (ValueError, IndexError):
                    continue
        
        # Extract invoice number
        invoice_patterns = [
            r'Invoice\s*#?\s*:?\s*([A-Z0-9\-]+)',
            r'Bill\s*#?\s*:?\s*([A-Z0-9\-]+)',
            r'Receipt\s*#?\s*:?\s*([A-Z0-9\-]+)',
            r'#\s*([A-Z0-9\-]+)',
        ]
        
        for pattern in invoice_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['invoice_no'] = match.group(1)
                break
        
        # Extract date
        date_patterns = [
            r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    date_str = match.group(1)
                    # Try different date formats
                    for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d %b %Y']:
                        try:
                            data['date'] = datetime.strptime(date_str, fmt).date()
                            break
                        except ValueError:
                            continue
                    if data['date']:
                        break
                except (ValueError, IndexError):
                    continue
        
        # Extract GSTIN
        gstin_pattern = r'[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}'
        gstin_match = re.search(gstin_pattern, text)
        if gstin_match:
            data['gstin'] = gstin_match.group(0)
        
        return data
    
    @staticmethod
    def process_receipt(image_path):
        """Complete receipt processing pipeline"""
        # Extract text
        text = OCRService.extract_text_from_image(image_path)
        
        # Parse data
        parsed_data = OCRService.parse_receipt_data(text)
        
        return parsed_data