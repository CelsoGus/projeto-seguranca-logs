#!/usr/bin/env python3
"""
Script de Coleta com Integração Graylog
"""

import logging
import csv
import datetime
import subprocess
import os
import json
import socket
import time

# Configurações
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
GRAYLOG_HOST = "localhost"
GRAYLOG_PORT = 12201

def setup_logging():
    """Configura o sistema de logging"""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(LOG_DIR, "monitoramento.log")),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def enviar_graylog(mensagem, nivel="INFO", campos_extras=None):
    """Envia log para Graylog via GELF"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        log_data = {
            "version": "1.1",
            "host": socket.gethostname(),
            "short_message": mensagem,
            "timestamp": datetime.datetime.now().timestamp(),
            "level": 6 if nivel == "INFO" else 4 if nivel == "WARNING" else 3,
            "_script": "coletor_seguranca",
            "_tipo": campos_extras.get('tipo', 'unknown') if campos_extras else 'unknown'
        }
        
        # Adicionar campos extras
        if campos_extras:
            for key, value in campos_extras.items():
                log_data[f"_{key}"] = str(value)
        
        message = json.dumps(log_data)
        sock.sendto(message.encode('utf-8'), (GRAYLOG_HOST, GRAYLOG_PORT))
        sock.close()
        
        logger = setup_logging()
        logger.info(f"📤 Enviado para Graylog: {mensagem}")
        return True
    except Exception as e:
        logger = setup_logging()
        logger.error(f"❌ Erro ao enviar para Graylog: {e}")
        return False

def coletar_logs_ssh():
    """Coleta tentativas de login SSH falhas"""
    logger = setup_logging()
    try:
        if not os.path.exists('/var/log/auth.log'):
            logger.warning("Arquivo /var/log/auth.log não encontrado")
            return []
        
        result = subprocess.run(
            ['sudo', 'grep', 'Failed password', '/var/log/auth.log'],
            capture_output=True, text=True
        )
        
        logs_ssh = []
        for line in result.stdout.split('\n'):
            if line.strip():
                log_entry = {
                    'timestamp': datetime.datetime.now().isoformat(),
                    'tipo': 'SSH_FAILED_LOGIN',
                    'mensagem': line.strip(),
                    'severidade': 'ALTA'
                }
                logs_ssh.append(log_entry)
                
                # 🆕 ENVIAR PARA GRAYLOG
                enviar_graylog(
                    f"Tentativa SSH falha: {line.strip()}",
                    "WARNING",
                    {'tipo': 'ssh_failed', 'severidade': 'alta', 'fonte': 'auth.log'}
                )
        
        logger.info(f"Coletados {len(logs_ssh)} logs SSH falhos")
        return logs_ssh
        
    except Exception as e:
        logger.error(f"Erro ao coletar logs SSH: {e}")
        return []

def verificar_arquivos_sistema():
    """Verifica arquivos importantes do sistema"""
    logger = setup_logging()
    arquivos_verificar = ['/etc/passwd', '/etc/hosts', '/etc/ssh/sshd_config']
    
    logs_arquivos = []
    for arquivo in arquivos_verificar:
        if os.path.exists(arquivo):
            try:
                stat = os.stat(arquivo)
                mod_time = datetime.datetime.fromtimestamp(stat.st_mtime)
                size = stat.st_size
                
                log_entry = {
                    'timestamp': datetime.datetime.now().isoformat(),
                    'tipo': 'INFO_ARQUIVO',
                    'mensagem': f'Arquivo {arquivo} verificado',
                    'severidade': 'BAIXA',
                    'arquivo': arquivo
                }
                logs_arquivos.append(log_entry)
                
                # 🆕 ENVIAR PARA GRAYLOG
                enviar_graylog(
                    f"Arquivo verificado: {arquivo}",
                    "INFO",
                    {'tipo': 'arquivo_verificado', 'arquivo': arquivo, 'tamanho': size}
                )
                
            except PermissionError:
                logger.warning(f"Sem permissão para acessar: {arquivo}")
                continue
    
    return logs_arquivos

def monitorar_processos_suspeitos():
    """Monitora processos potencialmente suspeitos"""
    logger = setup_logging()
    processos_suspeitos = ['nmap', 'metasploit', 'john', 'hashcat']
    
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        logs_processos = []
        
        for processo in processos_suspeitos:
            if processo in result.stdout.lower():
                log_entry = {
                    'timestamp': datetime.datetime.now().isoformat(),
                    'tipo': 'PROCESSO_SUSPEITO',
                    'mensagem': f'Processo suspeito: {processo}',
                    'severidade': 'ALTA',
                    'processo': processo
                }
                logs_processos.append(log_entry)
                
                # 🆕 ENVIAR PARA GRAYLOG
                enviar_graylog(
                    f"Processo suspeito detectado: {processo}",
                    "ALERT",
                    {'tipo': 'processo_suspeito', 'processo': processo, 'severidade': 'alta'}
                )
        
        return logs_processos
    except Exception as e:
        logger.error(f"Erro ao monitorar processos: {e}")
        return []

def salvar_logs_csv(logs):
    """Salva logs em arquivo CSV (backup local)"""
    if not logs:
        return None
    
    nome_arquivo = os.path.join(LOG_DIR, f"logs_seguranca_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    campos = ['timestamp', 'tipo', 'mensagem', 'severidade', 'arquivo', 'processo']
    
    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writeheader()
            
            for log in logs:
                linha = {campo: log.get(campo, '') for campo in campos}
                writer.writerow(linha)
        
        logger = setup_logging()
        logger.info(f"💾 Backup CSV salvo: {nome_arquivo}")
        return nome_arquivo
    except Exception as e:
        logger.error(f"Erro ao salvar CSV: {e}")
        return None

def main():
    """Função principal"""
    logger = setup_logging()
    logger.info("🚀 INICIANDO COLETA COM GRAYLOG")
    
    # 🆕 Enviar início para Graylog
    enviar_graylog("Script de monitoramento iniciado", "INFO", {'tipo': 'script_inicio'})
    
    todos_logs = []
    
    # Coletar logs
    todos_logs.extend(coletar_logs_ssh())
    todos_logs.extend(verificar_arquivos_sistema())
    todos_logs.extend(monitorar_processos_suspeitos())
    
    # Salvar backup CSV
    if todos_logs:
        arquivo_saida = salvar_logs_csv(todos_logs)
        
        # 🆕 Enviar resumo para Graylog
        enviar_graylog(
            f"Coleta concluída: {len(todos_logs)} eventos",
            "INFO",
            {'tipo': 'resumo_coleta', 'total_eventos': len(todos_logs)}
        )
        
        logger.info(f"✅ COLETA CONCLUÍDA: {len(todos_logs)} eventos")
    else:
        enviar_graylog("Nenhum evento de segurança detectado", "INFO")
        logger.info("ℹ️  Nenhum evento detectado")
    
    return len(todos_logs)

if __name__ == "__main__":
    main()
