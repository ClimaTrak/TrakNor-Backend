#!/usr/bin/env bash
# -----------------------------------------------------------------------------
#  Codex environment bootstrapper for the ClimaTrak stack
# -----------------------------------------------------------------------------
set -euo pipefail

# ----- CONFIGURÁVEIS ---------------------------------------------------------
PYTHON_VERSION="${PYTHON_VERSION:-3.12}"
NODE_VERSION="${NODE_VERSION:-20}"
POSTGRES_VERSION="${POSTGRES_VERSION:-16}"
BACKEND_REPO="https://github.com/ClimaTrak/TrakNor-Backend.git"
FRONTEND_REPO="https://github.com/ClimaTrak/traknor-frontend.git"
PROJECT_DIR="$HOME/climatrak"
# -----------------------------------------------------------------------------

echo "🚀  Iniciando setup Codex…"

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# ---------------------------------------------------------------------------
# 1. Clone dos repositórios
# ---------------------------------------------------------------------------
echo "🔄  Clonando repositórios…"
git clone "$BACKEND_REPO" backend || echo "Backend já clonado."
git clone "$FRONTEND_REPO" frontend || echo "Frontend já clonado."

# ---------------------------------------------------------------------------
# 2. Backend (Python/Django)
# ---------------------------------------------------------------------------
echo "🐍  Configurando backend…"
cd backend
python$PYTHON_VERSION -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt                # dependências Django/DRF
pip install pre-commit commitizen              # ferramenta Codex → hooks
pre-commit install                             # ruff / isort / black / pytest
cz init --name cz_conventional --yes >/dev/null || true

# .env
cp .env.example .env
sed -i '' 's/DEBUG=.*/DEBUG=true/' .env 2>/dev/null || sed -i 's/DEBUG=.*/DEBUG=true/' .env

# Migrations + super-usuário dummy
python manage.py migrate
echo "from django.contrib.auth import get_user_model; \
      get_user_model().objects.create_superuser('admin@local', 'admin')" \
      | python manage.py shell || true

deactivate
cd ..

# ---------------------------------------------------------------------------
# 3. Frontend (React + pnpm)
# ---------------------------------------------------------------------------
echo "🖼️  Configurando frontend…"
curl -fsSL https://get.pnpm.io/install.sh | sh -  # instala pnpm
export PNPM_HOME="$HOME/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
corepack enable
corepack prepare pnpm@latest --activate

cd frontend
pnpm install
pnpm dlx husky-init --yarn2 && pnpm install
# commitlint
pnpm add -D @commitlint/{config-conventional,cli}
echo "module.exports = {extends: ['@commitlint/config-conventional']};" > commitlint.config.cjs
npx husky add .husky/commit-msg 'pnpm commitlint --edit $1'

cd ..

# ---------------------------------------------------------------------------
# 4. Banco PostgreSQL (local via Docker)
# ---------------------------------------------------------------------------
echo "🐘  Subindo PostgreSQL…"
docker run -d --name climatrak-pg \
  -e POSTGRES_DB=traknor -e POSTGRES_USER=traknor -e POSTGRES_PASSWORD=traknor \
  -p 5432:5432 postgres:$POSTGRES_VERSION

# ---------------------------------------------------------------------------
# 5. Geração Swagger / OpenAPI
# ---------------------------------------------------------------------------
echo "📑  Gerando documentação Swagger…"
cd backend
source .venv/bin/activate
make swagger:generate || python manage.py spectacular --file docs/openapi.yaml
deactivate
cd ..

# ---------------------------------------------------------------------------
# 6. Finalização
# ---------------------------------------------------------------------------
echo -e "\n✅  Ambiente Codex pronto!\n"
echo "• Ative o backend:  cd backend && source .venv/bin/activate && python manage.py runserver"
echo "• Inicie o frontend: cd frontend && pnpm dev"
echo "• Acesse o Swagger: http://127.0.0.1:8000/docs/"
echo "• Use 'cz c' para commits seguindo Conventional Commits."
