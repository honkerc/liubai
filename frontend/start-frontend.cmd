@echo off
cd /d "%~dp0"
node "node_modules\@vue\cli-service\bin\vue-cli-service.js" serve --port 8080
