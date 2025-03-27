import json
import os
import requests
from dotenv import load_dotenv
from PIL import Image  # For image validation

# Load environment variables from .env file
load_dotenv()

# Securely retrieve API credentials from environment variables
LicenseCode = os.getenv('OCR_LICENSE_CODE')
UserName = os.getenv('OCR_USERNAME')

if not LicenseCode or not UserName:
    print("Error: OCR_LICENSE_CODE or OCR_USERNAME environment variables not set.")
    exit()

def extract_text_from_image(image_path, language="english", tobw=False):
    """
    Extracts text from a single image using OCRWebService.com API.

    Args:
        image_path (str): Path to the image file.
        language (str): Language for OCR (e.g., "english", "german").
        tobw (bool): Convert image to black and white.

    Returns:
        str: Extracted text or None if an error occurs.
    """
    try:
        RequestUrl = f"http://www.ocrwebservice.com/restservices/processDocument?gettext=true&language={language}&tobw={str(tobw).lower()}"
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        r = requests.post(RequestUrl, data=image_data, auth=(UserName, LicenseCode))
        r.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        jobj = json.loads(r.content)
        ocrError = str(jobj.get("ErrorMessage", "")) #Use .get to prevent key errors

        if ocrError:
            print(f"Recognition Error for {os.path.basename(image_path)}: {ocrError}")
            return None

        return str(jobj["OCRText"][0][0]) # Extract text.

    except requests.exceptions.RequestException as e:
        print(f"API Request Error for {os.path.basename(image_path)}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error for {os.path.basename(image_path)}: {e}")
        return None
    except KeyError as e:
        print(f"Key Error for {os.path.basename(image_path)}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for {os.path.basename(image_path)}: {e}")
        return None


def process_images_in_folder(folder_path, language="english", tobw=False):
    """
    Processes all image files in a folder and saves extracted text to a JSON file.

    Args:
        folder_path (str): Path to the folder containing image files.
        language (str): Language for OCR.
        tobw (bool): Convert image to black and white.
    """
    extracted_text_data = {}
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif'))]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)

        # Validate image file
        try:
            Image.open(image_path)  # Attempt to open the image.
        except Exception as e:
            print(f"Skipping invalid image file: {image_file}. Error: {e}")
            continue #skip to next image

        extracted_text = extract_text_from_image(image_path, language, tobw)
        if extracted_text:
            extracted_text_data[image_file] = extracted_text

    with open('extracted_text_from_images.json', 'w', encoding="utf-8") as json_file:
        json.dump(extracted_text_data, json_file, indent=4, ensure_ascii=False) #ensure_ascii fixes encoding issues.

    print("Extracted text saved to extracted_text_from_images.json")

# Example usage:
folder_path = "c:\\Users\Mr Dashi\Downloads\email_scanner\images"
process_images_in_folder(folder_path, language="german", tobw=True) #example usage of language and tobw parameters.