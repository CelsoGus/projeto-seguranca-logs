markdown
# Sistema de Monitoramento de Segurança

**Projeto Acadêmico - Coleta e Análise de Logs para Detecção de Incidentes**

##Sobre o Projeto

Sistema automatizado para coleta, análise e monitoramento de logs de segurança, implementando detecção preliminar de incidentes usando Wazuh, Graylog e scripts Python personalizados.

### Objetivos
- Coleta automatizada de logs de segurança
- Detecção de atividades suspeitas em tempo real
- Integração entre ferramentas especializadas
- Dashboard centralizado para visualização
- Pipeline CI/CD com GitHub Actions

## Arquitetura do Sistema
[Scripts Python] → Coleta logs customizados
↓
[Graylog] → Armazenamento & Análise Geral
↓
[Wazuh] → Detecção de Ameaças
↓
[Dashboards] → Visualização Unificada

##Estrutura do Projeto
projeto-seguranca-logs/
├── .github/
│ └── workflows/
│ └── security-monitoring.yml # Automação CI/CD
├── scripts/
│ ├── coleta_logs_graylog.py # Script principal
│ └── simular_eventos.py # Script de testes
├── logs/ # Logs gerados
├── config/ # Configurações
└── docs/ # Documentação

##Ferramentas Utilizadas

### Wazuh
- **Função**: SIEM e HIDS (Host-based Intrusion Detection System)
- **Uso no projeto**: Detecção de tentativas de SSH falhas, modificações em arquivos críticos
- **Acesso**: http://localhost:5601

###Graylog  
- **Função**: Gerenciamento centralizado de logs
- **Uso no projeto**: Armazenamento e análise de logs customizados
- **Acesso**: http://localhost:19000 (admin/admin)

### Scripts Python
- **coleta_logs_graylog.py**: Coleta logs do sistema e envia para Graylog
- **simular_eventos.py**: Simula eventos para testes do sistema

### GitHub Actions
- **Função**: Automação e execução agendada
- **Workflow**: Executa a cada 6 horas e em pushes

## Como Executar

### Pré-requisitos
- Kali Linux (ou outra distro Linux)
- Docker e Docker Compose
- Python 3.8+
- Git

### 1. Clone o Repositório
```bash
git clone https://github.com/CelsoGus/projeto-seguranca-logs.git
cd projeto-seguranca-logs
2. Configuração do Ambiente
Wazuh (Opcional - se quiser usar)
bash
# Instalação automática
curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
sudo bash ./wazuh-install.sh --all-in-one
Graylog (Docker)
bash
cd projeto-graylog
docker-compose up -d
# Acesse: http://localhost:19000
3. Execução dos Scripts
Script Principal
bash
cd scripts
chmod +x coleta_logs_graylog.py
python3 coleta_logs_graylog.py
Script de Testes
bash
python3 simular_eventos.py
4. Automação com Systemd
bash
# Configurar execução automática a cada 10 minutos
sudo systemctl enable coleta-seguranca.timer
sudo systemctl start coleta-seguranca.timer
 O que é Monitorado
 Segurança de Autenticação
Tentativas de SSH falhas

Logins bem-sucedidos

Tentativas de brute-force

 Integridade de Arquivos
Modificações em /etc/passwd

Alterações em /etc/shadow

Mudanças em /etc/ssh/sshd_config

⚡ Monitoramento de Sistema
Processos suspeitos em execução

Consumo de recursos

Atividades incomuns

🎯 Funcionalidades dos Scripts
coleta_logs_graylog.py
✅ Coleta logs de autenticação SSH

✅ Verifica integridade de arquivos críticos

✅ Monitora processos suspeitos

✅ Envia logs para Graylog (GELF/UDP)

✅ Gera arquivos CSV de backup

✅ Logs detalhados em /var/log/meu_monitoramento.log

simular_eventos.py
🧪 Simula tentativas de SSH falhas

🧪 Cria modificações de arquivos de teste

🧪 Gera processos para detecção

🧪 Valida funcionamento do sistema

🔧 Configuração
Variáveis do Script
python
GRAYLOG_HOST = "localhost"
GRAYLOG_PORT = 12201
LOG_DIR = "/home/user/projeto-seguranca-logs/logs"
Portas Utilizadas
Graylog Web: 19000

Graylog GELF: 12201/udp

Graylog Syslog: 1516

Wazuh: 5601

📈 Dashboards e Visualização
Graylog Dashboard
Acesse http://localhost:19000

Crie dashboard "Monitoramento de Segurança"

Adicione widgets:

Total de Eventos por Tipo

Timeline de Eventos de SSH

Gráfico de Severidade

Wazuh Dashboard
Acesse http://localhost:5601

Visualize alertas de segurança

Monitore integridade do sistema

🔄 GitHub Actions
O workflow automático executa:

✅ A cada 6 horas (agendado)

✅ Em todo push para main

✅ Manualmente via interface

✅ Gera relatórios e artefatos

🐛 Solução de Problemas
Graylog não acessível
bash
docker-compose ps
docker logs graylog-server
Scripts com erro de permissão
bash
chmod +x scripts/*.py
sudo python3 scripts/coleta_logs_graylog.py
Portas em conflito
bash
sudo netstat -tlnp | grep -E '(19000|12201|1516)'
📝 Exemplos de Uso
Execução Manual
bash
cd scripts
python3 coleta_logs_graylog.py
Ver Logs Gerados
bash
tail -f logs/monitoramento.log
cat logs/seguranca_logs_*.csv
Testar Integração Graylog
bash
python3 simular_eventos.py
# Verifique em http://localhost:19000
🤝 Contribuição
Fork o projeto

Crie uma branch para sua feature

Commit suas mudanças

Push para a branch

Abra um Pull Request

📄 Licença
Este projeto é para fins educacionais.

👨‍💻 Autor
CelsoGus - GitHub
