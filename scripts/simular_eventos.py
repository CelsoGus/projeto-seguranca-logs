#!/usr/bin/env python3
"""
Script para simular eventos de segurança para teste
"""

import subprocess
import time
import os

def simular_ssh_falho():
    print("🚨 Simulando evento de SSH falho...")
    try:
        # Tenta executar comando que pode gerar logs
        result = subprocess.run(['who'], capture_output=True, text=True)
        print(f"Usuários logados: {result.stdout}")
    except Exception as e:
        print(f"Erro ao simular SSH: {e}")

def simular_alteracao_arquivo():
    print("📁 Simulando verificação de arquivos...")
    try:
        result = subprocess.run(['ls', '-la', '/etc/hosts'], capture_output=True, text=True)
        print(f"Arquivo hosts: {result.stdout}")
    except Exception as e:
        print(f"Erro ao verificar arquivo: {e}")

def criar_arquivo_teste():
    print("📝 Criando arquivo de teste para monitoramento...")
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_file = os.path.join(project_root, "logs", "arquivo_teste.txt")
        
        with open(test_file, 'w') as f:
            f.write(f"Arquivo de teste criado em: {time.ctime()}\n")
            f.write("Este arquivo pode ser monitorado pelo script de segurança.\n")
        
        print(f"✅ Arquivo de teste criado: {test_file}")
    except Exception as e:
        print(f"❌ Erro ao criar arquivo de teste: {e}")

def main():
    print("🎭 INICIANDO SIMULAÇÃO DE EVENTOS DE SEGURANÇA")
    print(f"📂 Diretório do projeto: {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
    
    eventos = [simular_ssh_falho, simular_alteracao_arquivo, criar_arquivo_teste]
    
    for i, evento in enumerate(eventos, 1):
        print(f"\n--- Evento {i}/3 ---")
        evento()
        time.sleep(1)
    
    print("\n" + "="*50)
    print("✅ Simulação concluída!")
    print("📊 Execute o script de coleta para ver os logs:")
    print("   python3 coleta_logs.py")
    print("="*50)

if __name__ == "__main__":
    main()
