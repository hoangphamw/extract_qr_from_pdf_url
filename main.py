import fitz  # PyMuPDF
import requests
from io import BytesIO
from PIL import Image
from pyzbar.pyzbar import decode as pyzbarDecode

def extract_qrcode_from_pdf(url):

    extracted_str_list = []

    # Download the PDF file
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to download the PDF file.")
        return

    # Load PDF file from memory
    pdf_data = BytesIO(response.content)
    try:
        doc = fitz.open(stream=pdf_data, filetype="pdf")
    except Exception as e:
        print("Error:", e)
        return

    for page_num in range(len(doc)):
        print(f"Processing page {page_num + 1}")
        page = doc[page_num]
        images_in_page = page.get_images(full=True)
        for img_index, img_info in enumerate(images_in_page, start=1):
            print(f"Processing image {img_index + 1} on page {page_num + 1}")
            try:

                # get the XREF of the image
                xref = img_info[0]

                # extract the image bytes
                base_image = doc.extract_image(xref)

                image_bytes = base_image["image"]

                qrcode_decoded = pyzbarDecode(Image.open(BytesIO(image_bytes)))

                if qrcode_decoded:
                    print('qrcode_decoded={}'.format(qrcode_decoded))
                    if qrcode_decoded[0].type == 'QRCODE':
                        qrcode_decoded_str = qrcode_decoded[0].data.decode("utf-8")
                        print('qrcode_decoded_str={}'.format(qrcode_decoded_str))
                        extracted_str_list.append(qrcode_decoded_str)

            except Exception as e:
                print(f"Error processing image {img_index + 1} on page {page_num + 1}: {e}")

    print('extracted_str_list={}'.format(extracted_str_list))
    doc.close()
    return extracted_str_list

# Example usage:
pdf_url = "https://abc.def/xxx.pdf"
extracted_qrcode_str = extract_qrcode_from_pdf(pdf_url)
print(f"Total QR string extracted: {len(extracted_qrcode_str)}")
