import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
import requests
from io import BytesIO
from tqdm import tqdm
import os

def extract_text_from_local_pdf(pdf_path, output_file, batch_size=10):
    try:
        images = convert_from_path(pdf_path)
        num_pages = len(images)
        text = ""
        for batch_start in tqdm(range(0, num_pages, batch_size), desc="Procesando PDF local"):
            batch_end = min(batch_start + batch_size, num_pages)
            batch_images = images[batch_start:batch_end]
            for i, image in enumerate(batch_images, start=batch_start+1):
                text += f'Página {i}:\n{pytesseract.image_to_string(image)}\n'
                if i == num_pages:
                    break  # Detener el procesamiento si se alcanza el final del documento
            if i == num_pages:
                break  # Detener el procesamiento si se alcanza el final del documento
        
        # Guardar el texto en un archivo .txt
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(text)
        return f"Texto guardado en: {output_file}"
    
    except FileNotFoundError:
        return "Error: No se pudo encontrar el PDF local."
    except Exception as e:
        return f"Error al procesar el PDF local: {str(e)}"

def extract_text_from_online_pdf(pdf_url, output_file, batch_size=10):
    try:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            images = convert_from_bytes(response.content)
            num_pages = len(images)
            text = ""
            for batch_start in tqdm(range(0, num_pages, batch_size), desc="Procesando PDF en línea"):
                batch_end = min(batch_start + batch_size, num_pages)
                batch_images = images[batch_start:batch_end]
                for i, image in enumerate(batch_images, start=batch_start+1):
                    text += f'Página {i}:\n{pytesseract.image_to_string(image)}\n'
                    if i == num_pages:
                        break  # Detener el procesamiento si se alcanza el final del documento
                if i == num_pages:
                    break  # Detener el procesamiento si se alcanza el final del documento
            
            # Guardar el texto en un archivo .txt
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(text)
            return f"Texto guardado en: {output_file}"
        else:
            return f"Error: No se pudo acceder al PDF en línea (código de estado {response.status_code})."
    except requests.exceptions.RequestException as e:
        return f"Error al procesar el PDF en línea: {str(e)}"
    except Exception as e:
        return f"Error al procesar el PDF en línea: {str(e)}"

# Ejemplo de uso
local_pdf_path = r'FILE IN DISK'
online_pdf_url = 'FILE ONLINE'

local_output_file = 'texto_local.txt'
online_output_file = 'texto_online.txt'

local_text = extract_text_from_local_pdf(local_pdf_path, local_output_file)
print(local_text)

online_text = extract_text_from_online_pdf(online_pdf_url, online_output_file)
print(online_text)
