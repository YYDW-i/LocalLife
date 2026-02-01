# 构建前端产物到 frontend/dist
# 运行：.\scripts\build_frontend.ps1

$ErrorActionPreference = "Stop"
cd frontend
npm install
npm run build
