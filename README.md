# Google Careers France - Deploy Railway

Sistema completo de vagas de emprego do Google Careers France com backend Flask e frontend React.

## 🚀 Deploy no Railway

### Pré-requisitos
- Conta no Railway (https://railway.app)
- Git instalado

### Passos para Deploy

1. **Criar novo projeto no Railway**
   ```bash
   railway login
   railway new
   ```

2. **Fazer deploy**
   ```bash
   railway up
   ```

3. **Configurar variáveis de ambiente (opcional)**
   - `SECRET_KEY`: Chave secreta para Flask
   - `PORT`: Porta do servidor (Railway define automaticamente)

### Estrutura do Projeto

```
google-careers-railway/
├── src/                    # Backend Flask
│   ├── models/            # Modelos SQLAlchemy
│   ├── routes/            # Rotas da API
│   ├── static/            # Frontend React buildado
│   └── main.py           # Aplicação principal
├── requirements.txt       # Dependências Python
├── Procfile              # Configuração de processo
├── railway.json          # Configuração Railway
└── populate_db.py        # Script para popular banco
```

## 🌟 Funcionalidades

### Frontend
- ✅ Interface responsiva em francês
- ✅ Geolocalização automática
- ✅ Formulário completo de candidatura
- ✅ Upload de documentos
- ✅ Carrossel de vagas
- ✅ Favicon do Google

### Backend
- ✅ API REST completa
- ✅ Sistema de upload de arquivos
- ✅ Painel administrativo
- ✅ Banco de dados SQLite
- ✅ CORS configurado

### Admin
- ✅ Visualização de candidaturas
- ✅ Gerenciamento de documentos
- ✅ Dashboard com estatísticas
- ✅ Sistema de status

## 🔧 Configuração Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Popular banco de dados
python populate_db.py

# Executar aplicação
python src/main.py
```

## 📱 URLs

- **Frontend:** `/` (página principal)
- **Admin:** `/admin` (painel administrativo)
- **API:** `/api/*` (endpoints da API)

## 🎯 Tecnologias

- **Backend:** Flask, SQLAlchemy, Flask-CORS
- **Frontend:** React, Vite, TailwindCSS
- **Banco:** SQLite
- **Deploy:** Railway, Gunicorn

---

**Desenvolvido para Google Careers France** 🇫🇷

