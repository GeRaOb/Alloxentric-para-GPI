import os
from weaviate.auth import AuthApiKey
import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout
from Cargador import cargador_documentos

# Configurar la conexión a Weaviate
WCD_URL = "https://weavitext-6wfr035z.weaviate.network"
WCD_API_KEY = "F2ax19PAU8E7yOpw8jCr8tbOZczkfpB7zMjY"

try:
    # Conectar a Weaviate
    client = weaviate.connect_to_wcs(
        cluster_url=WCD_URL,
        auth_credentials=AuthApiKey(WCD_API_KEY),
        additional_config=AdditionalConfig(timeout=Timeout(init=10)),
        skip_init_checks=True
    )

    # Verificar la conexión
    if client.is_ready():
        print("Conexión a Weaviate establecida correctamente.")

        # Cargar los documentos de texto
        class_name = "MyDocuments"
        directory_path = os.path.join(os.path.dirname(__file__), ".")
        cargador_documentos(client, class_name, directory_path)
    else:
        print("Error al establecer la conexión a Weaviate.")
finally:
    # Cerrar la conexión a Weaviate
    client.close()
