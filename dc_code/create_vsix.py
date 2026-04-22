import os
import shutil
import zipfile
import json
from pathlib import Path

# .vsix 파일 생성 스크립트
extension_dir = Path("d:/data3/Roo-Code/dc_code/extension")
sample_db_path = Path("d:/data3/Roo-Code/dc_code/sample.db")
output_vsix = Path("d:/data3/Roo-Code/dc_code/sqlite-query-tool-0.0.1.vsix")

# 임시 디렉토리
temp_dir = Path("d:/data3/Roo-Code/dc_code/extension/.vsix-temp")
if temp_dir.exists():
    shutil.rmtree(temp_dir)
temp_dir.mkdir(parents=True)

print("📦 .vsix 파일 생성 중...")

# 1. 필요한 파일들 복사
files_to_include = [
    ("package.json", "package.json"),
    ("README.md", "README.md"),
    (".vscodeignore", ".vscodeignore"),
]

for src, dst in files_to_include:
    src_path = extension_dir / src
    if src_path.exists():
        shutil.copy(src_path, temp_dir / dst)
        print(f"  ✓ {dst}")

# 2. src 폴더 복사
src_folder = extension_dir / "src"
if src_folder.exists():
    shutil.copytree(src_folder, temp_dir / "src")
    print(f"  ✓ src/")

# 3. out 폴더 생성 (JavaScript 버전)
out_dir = temp_dir / "out"
out_dir.mkdir(exist_ok=True)

# 4. extension.ts를 간단한 JavaScript로 변환
js_code = '''
const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

let currentPanel = undefined;
let dbBuffer = undefined;

function activate(context) {
  console.log('SQLite Query Tool 활성화됨');

  const dbPath = path.join(context.extensionPath, '../../sample.db');

  try {
    dbBuffer = fs.readFileSync(dbPath);
    console.log(`데이터베이스 로드됨: ${dbPath} (${dbBuffer.length} bytes)`);
  } catch (error) {
    vscode.window.showErrorMessage(`데이터베이스 파일을 찾을 수 없습니다: ${dbPath}`);
    return;
  }

  let disposable = vscode.commands.registerCommand(
    'sqliteQuery.openQuery',
    () => openQueryPanel(context)
  );

  context.subscriptions.push(disposable);

  const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
  );
  statusBarItem.command = 'sqliteQuery.openQuery';
  statusBarItem.text = '$(database) SQLite Query';
  statusBarItem.show();
  context.subscriptions.push(statusBarItem);
}

function openQueryPanel(context) {
  const column = vscode.ViewColumn.One;

  if (currentPanel) {
    currentPanel.reveal(column);
    return;
  }

  currentPanel = vscode.window.createWebviewPanel(
    'sqliteQuery',
    'SQLite Query Tool',
    column,
    {
      enableScripts: true,
      enableForms: true,
      retainContextWhenHidden: true
    }
  );

  currentPanel.webview.html = getWebviewContent(dbBuffer);

  currentPanel.onDidDispose(
    () => {
      currentPanel = undefined;
    },
    undefined,
    []
  );

  currentPanel.webview.onDidReceiveMessage(
    (message) => {
      switch (message.command) {
        case 'showMessage':
          vscode.window.showInformationMessage(message.text);
          break;
      }
    },
    undefined,
    []
  );
}

function getWebviewContent(dbBuffer) {
  const dbBase64 = dbBuffer.toString('base64');

  return `
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>SQLite Query Tool</title>
      <script src="https://sql.js.org/dist/sql-wasm.js"><\/script>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
          background: var(--vscode-editor-background);
          color: var(--vscode-editor-foreground);
          padding: 20px; line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { margin-bottom: 20px; font-size: 24px; border-bottom: 2px solid var(--vscode-focusBorder); padding-bottom: 10px; }
        .section { margin-bottom: 30px; }
        .section-title { font-size: 16px; font-weight: 600; margin-bottom: 12px; color: var(--vscode-terminal-ansiBlue); }
        .tables-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; margin-bottom: 20px; }
        .table-btn { padding: 8px 12px; background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; border-radius: 4px; cursor: pointer; font-size: 13px; transition: background 0.2s; }
        .table-btn:hover { background: var(--vscode-button-hoverBackground); }
        textarea { width: 100%; height: 120px; padding: 10px; background: var(--vscode-input-background); color: var(--vscode-input-foreground); border: 1px solid var(--vscode-input-border); border-radius: 4px; font-family: monospace; font-size: 13px; }
        .query-controls { display: flex; gap: 8px; margin-top: 10px; }
        button { padding: 8px 16px; background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; border-radius: 4px; cursor: pointer; font-size: 13px; }
        button:hover { background: var(--vscode-button-hoverBackground); }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .results { margin-top: 20px; max-height: 400px; overflow: auto; border: 1px solid var(--vscode-input-border); border-radius: 4px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid var(--vscode-input-border); }
        th { background: var(--vscode-tab-activeBackground); font-weight: 600; color: var(--vscode-terminal-ansiCyan); }
        tr:hover { background: rgba(255,255,255,0.05); }
        .error { color: var(--vscode-terminal-ansiRed); padding: 10px; background: rgba(255,0,0,0.1); border-radius: 4px; margin-top: 10px; border-left: 3px solid red; }
        .success { color: var(--vscode-terminal-ansiGreen); padding: 10px; background: rgba(0,255,0,0.1); border-radius: 4px; margin-top: 10px; border-left: 3px solid green; }
        .loading { text-align: center; padding: 20px; opacity: 0.6; }
        .spinner { border: 3px solid var(--vscode-input-border); border-top: 3px solid var(--vscode-terminal-ansiCyan); border-radius: 50%; width: 24px; height: 24px; animation: spin 1s infinite; margin: 0 auto 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>📊 SQLite Query Tool</h1>
        <div id="loading" class="loading">
          <div class="spinner"><\/div>
          <p>데이터베이스 로드 중...</p>
        </div>
        <div id="content" style="display: none;">
          <div class="section">
            <div class="section-title">📋 테이블 목록</div>
            <div class="tables-list" id="tablesList">
              <p style="opacity: 0.6;">테이블을 로드할 수 없습니다</p>
            </div>
          </div>
          <div class="section">
            <div class="section-title">✏️ SQL 쿼리</div>
            <textarea id="queryInput" placeholder="SELECT * FROM users LIMIT 10"><\/textarea>
            <div class="query-controls">
              <button onclick="executeQuery()" id="executeBtn">🚀 실행</button>
              <button onclick="clearQuery()">🗑️ 초기화</button>
            </div>
          </div>
          <div class="section">
            <div class="section-title">📈 결과</div>
            <div id="resultsContainer" style="display: none;">
              <div id="results"><\/div>
            </div>
            <div id="messageContainer" style="display: none;"><\/div>
          </div>
        </div>
      </div>
      <script>
        let db = null;
        let SQL = null;
        async function initDatabase() {
          try {
            SQL = await initSqlJs();
            const dbData = '${dbBase64}';
            const binaryString = atob(dbData);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
              bytes[i] = binaryString.charCodeAt(i);
            }
            db = new SQL.Database(bytes);
            document.getElementById('loading').style.display = 'none';
            document.getElementById('content').style.display = 'block';
            loadTablesList();
          } catch (error) {
            document.getElementById('loading').innerHTML = '<div class="error">❌ 데이터베이스 로드 실패: ' + error.message + '<\/div>';
          }
        }
        function loadTablesList() {
          try {
            const result = db.exec("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name");
            const tables = result.length > 0 ? result[0].values.map(row => row[0]) : [];
            const container = document.getElementById('tablesList');
            if (tables.length === 0) {
              container.innerHTML = '<p style="opacity: 0.6;">테이블이 없습니다<\/p>';
              return;
            }
            container.innerHTML = tables.map(table => \`<button class="table-btn" onclick="loadTable('\\${table}')">\${table}<\/button>\`).join('');
          } catch (error) { console.error(error); }
        }
        function loadTable(tableName) {
          document.getElementById('queryInput').value = \`SELECT * FROM \\${tableName} LIMIT 100\`;
        }
        function executeQuery() {
          if (!db) { alert('데이터베이스를 로드하세요'); return; }
          const sql = document.getElementById('queryInput').value.trim();
          if (!sql) { alert('쿼리를 입력하세요'); return; }
          const btn = document.getElementById('executeBtn');
          btn.disabled = true;
          btn.textContent = '⏳ 실행 중...';
          try {
            const result = db.exec(sql);
            displayResults(result);
          } catch (error) {
            displayError(error.message);
          } finally {
            btn.disabled = false;
            btn.textContent = '🚀 실행';
          }
        }
        function displayResults(results) {
          const container = document.getElementById('resultsContainer');
          const resultsDiv = document.getElementById('results');
          if (!results || results.length === 0) {
            resultsDiv.innerHTML = '<div class="success">✓ 쿼리 실행 성공 (결과: 0행)<\/div>';
            container.style.display = 'block';
            return;
          }
          const result = results[0];
          const columns = result.columns;
          const rows = result.values;
          const html = \`<div style="margin-bottom: 10px; padding: 8px; background: rgba(0,255,0,0.1); border-radius: 4px;">✓ 쿼리 실행 성공 (결과: \\${rows.length}행)<\/div><table><thead><tr>\${columns.map(col => \`<th>\\${col}<\/th>\`).join('')}<\/tr><\/thead><tbody>\${rows.map(row => \`<tr>\${row.map(value => \`<td>\\${value === null ? '<em style="opacity:0.5">NULL<\/em>' : String(value)}<\/td>\`).join('')}<\/tr>\`).join('')}<\/tbody><\/table>\`;
          resultsDiv.innerHTML = html;
          container.style.display = 'block';
        }
        function displayError(errorMsg) {
          document.getElementById('results').innerHTML = \`<div class="error">❌ 오류: \\${errorMsg}<\/div>\`;
          document.getElementById('resultsContainer').style.display = 'block';
        }
        function clearQuery() {
          document.getElementById('queryInput').value = '';
          document.getElementById('resultsContainer').style.display = 'none';
        }
        window.addEventListener('load', initDatabase);
      <\/script>
    </body>
    </html>
  `;
}

function deactivate() {}

exports.activate = activate;
exports.deactivate = deactivate;
'''

with open(out_dir / "extension.js", "w", encoding="utf-8") as f:
    f.write(js_code)
print(f"  ✓ out/extension.js")

# 5. .vsix 파일 생성 (ZIP)
print("\n📦 ZIP 파일 생성...")
with zipfile.ZipFile(output_vsix, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = Path(root) / file
            arcname = file_path.relative_to(temp_dir)
            zf.write(file_path, arcname)
            print(f"  ✓ {arcname}")

print(f"\n✅ .vsix 파일 생성 완료!")
print(f"📍 위치: {output_vsix}")
print(f"📊 파일 크기: {output_vsix.stat().st_size / 1024:.1f} KB")

# 임시 폴더 정리
shutil.rmtree(temp_dir)
print("\n✨ 완료!")
