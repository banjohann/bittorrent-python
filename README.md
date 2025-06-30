# Emulação de protocolo BitTorrent em Python
Autores: Érick de Souza Nunes e Johann Alexander Bandelow

## Descrição:
Esse trabalho foi desenvolvido para a matéria de Redes de Computadores do curso de TADS da UDESC

## Requisitos:
- Python3

## Para rodar:

### 1. Para gerar os pedaços de forma automática antes da execução, você pode executar o arquivo setup.py:
```bash
python setup.py
```

Você terá opções para escolher quandos pedaços seram gerados e de que forma (Aleatório ou Sequencial)

### 2. Para executar o servidor:
```bash
python server/main.py
```

### 3. Para executar o cliente:
Primeiro você deve alterar o arquivo main.py, preenchendo o IP do servidor com o IP da máquina:

```python
TRACKER_IP = 'IP DO SEU SERVIDOR'
```

Em seguida você pode executar o cliente da seguinte forma:
```bash
python client/main.py
```