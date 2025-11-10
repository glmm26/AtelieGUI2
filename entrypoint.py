import os
import sys
import time
import subprocess

def ensure_dependencies():
    """Verifica e instala dependências ausentes automaticamente."""
    required_packages = ['flask_login', 'sqlalchemy', 'flask', 'psycopg2']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} já está instalado")
        except ImportError:
            print(f"⚠ {package} não encontrado, instalando...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', '-r', 'requirements.txt'])
                print(f"✓ Dependências instaladas com sucesso!")
                return
            except subprocess.CalledProcessError as e:
                print(f"✗ Erro ao instalar dependências: {e}")
                sys.exit(1)

# Imports após garantir que as dependências estão instaladas
import psycopg2  # type: ignore
from app import create_app
from atelie_online.models import db

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/atelie_db')

def wait_for_db():
    print("Aguardando banco de dados...")
    while True:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            print("Banco disponível!")
            break
        except Exception:
            print("Banco não pronto, tentando de novo em 2s...")
            time.sleep(2)

if __name__ == '__main__':
    ensure_dependencies()
    wait_for_db()
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Tabelas criadas (se não existiam).")
    app.run(host='0.0.0.0', port=5000, debug=True)
