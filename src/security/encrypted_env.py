import os
import getpass
from cryptography.fernet import Fernet, InvalidToken


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
KEY_FILE = os.path.join(BASE_DIR, "encryption.key")
ENV_FILE = os.path.join(BASE_DIR, ".env.enc")


def generate_key():
    """Genera la llave de cifrado si no existe."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print(f"[INFO] Llave generada en: {KEY_FILE}")
    else:
        print(f"[INFO] Llave existente detectada: {KEY_FILE}")


def encrypt_secret():
    """Solicita la API key o contraseña y la guarda cifrada."""
    generate_key()
    key = open(KEY_FILE, "rb").read()
    cipher = Fernet(key)

    try:
        secret_value = getpass.getpass("🔐 Ingresa tu API key o contraseña: ").strip()
    except Exception:
        secret_value = input("⚠️ Ingresa tu API key o contraseña (visible): ").strip()

    if not secret_value:
        print("[ERROR] No se ingresó ningún valor.")
        return

    token = cipher.encrypt(secret_value.encode())
    with open(ENV_FILE, "wb") as f:
        f.write(token)

    print(f"[INFO] Clave cifrada guardada en: {ENV_FILE}")
    print("✅ Usa load_secret() para cargarla.")


def load_secret():
    """Descifra la clave guardada en .env.enc, o solicita crearla si no existe."""
    # Si no existen archivos, pedir creación
    if not os.path.exists(KEY_FILE) or not os.path.exists(ENV_FILE):
        print("[WARN] Archivos de clave o entorno no encontrados. Creando nueva clave cifrada.")
        encrypt_secret()

    # Intentar descifrar
    key = open(KEY_FILE, "rb").read()
    cipher = Fernet(key)
    token = open(ENV_FILE, "rb").read()

    try:
        decrypted = cipher.decrypt(token).decode()
        print("[INFO] Clave cargada correctamente desde .env.enc")
        return decrypted
    except InvalidToken:
        print("[ERROR] No se pudo descifrar el archivo. Probablemente la llave no coincide.")
        print("⚠️ Se generará una nueva clave cifrada.")
        encrypt_secret()
        return load_secret()


if __name__ == "__main__":
    # Si ejecutas este archivo directamente, solo generará/actualizará el secreto.
    encrypt_secret()

