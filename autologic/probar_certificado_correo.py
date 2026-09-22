"""Diagnóstico local de certificados para SMTP Gmail en macOS/Python 3.14."""
import os
import ssl
import certifi

print("Python:", __import__("sys").version)
print("Certifi:", certifi.where())
print("SSL_CERT_FILE:", os.environ.get("SSL_CERT_FILE"))
print("SSL_CERT_DIR:", os.environ.get("SSL_CERT_DIR"))
ctx = ssl.create_default_context(cafile=certifi.where())
print("CAs cargadas:", len(ctx.get_ca_certs()))
print("OK: el contexto SSL de certifi se pudo crear correctamente.")
