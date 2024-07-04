import os
import weaviate

def cargador_documentos(client, class_name, directory_path, batch_size=100):
    """
    Carga todos los documentos de texto .txt en una carpeta en Weaviate usando importación por lotes.

    Args:
        client (weaviate.WeaviateClient): Instancia del cliente de Weaviate.
        class_name (str): Nombre de la clase donde se cargarán los documentos.
        directory_path (str): Ruta de la carpeta que contiene los archivos .txt.
        batch_size (int): Tamaño de los lotes de importación (predeterminado: 100).
    """
    # Preparar el proceso de importación por lotes
    with client.batch as batch:
        dynamic=True
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, "r") as file:
                    text = file.read()
                new_object = {
                    "class": class_name,
                    "properties": {
                        "text": text
                    }
                }
                batch.add_data_object(new_object, class_name=class_name)

    print(f"Documentos cargados en la clase '{class_name}'.")
    