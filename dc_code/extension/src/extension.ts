import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

let currentPanel: vscode.WebviewPanel | undefined;
let dbBuffer: Buffer | undefined;

// 媛꾨떒??SQL ?꾩슦誘?
const sqlHelper = {
  generateSelectQuery: (tableName: string) => `SELECT * FROM ${tableName} LIMIT 10;`,
  generateCountQuery: (tableName: string) => `SELECT COUNT(*) as 珥앷컻??FROM ${tableName};`,
  generateDescribeQuery: (tableName: string) => `PRAGMA table_info(${tableName});`,
  
  suggestQueries: (question: string) => {
    const lower = question.toLowerCase();
    if (lower.includes('紐⑤몢') || lower.includes('?꾩껜')) {
      return { type: 'SELECT', hint: '紐⑤뱺 ?곗씠?곕? 議고쉶?⑸땲?? };
    }
    if (lower.includes('媛쒖닔') || lower.includes('紐뉕컻')) {
      return { type: 'COUNT', hint: '?곗씠??媛쒖닔瑜??몄뼱遊낅땲?? };
    }
    if (lower.includes('援ъ“') || lower.includes('?ㅽ궎留?) || lower.includes('而щ읆')) {
      return { type: 'SCHEMA', hint: '?뚯씠釉?援ъ“瑜?遊낅땲?? };
    }
    return { type: 'SELECT', hint: '?곗씠?곕? 議고쉶?⑸땲?? };
  }
};

export function activate(context: vscode.ExtensionContext) {
  console.log('SQLite AI Chat Tool ?쒖꽦?붾맖');

  const dbPath = path.join(context.extensionPath, '../../sample.db');

  // DB ?뚯씪 濡쒕뱶
  try {
    dbBuffer = fs.readFileSync(dbPath);
    console.log(`?곗씠?곕쿋?댁뒪 濡쒕뱶?? ${dbPath} (${dbBuffer.length} bytes)`);
  } catch (error) {
    vscode.window.showErrorMessage(`?곗씠?곕쿋?댁뒪 ?뚯씪??李얠쓣 ???놁뒿?덈떎: ${dbPath}`);
    return;
  }

  // "SQLite: Open Query Tool" 紐낅졊 ?깅줉
  let disposable = vscode.commands.registerCommand(
    'sqliteQuery.openQuery',
    () => openChatPanel(context)
  );

  context.subscriptions.push(disposable);

  // ?곹깭諛붿뿉 踰꾪듉 ?쒖떆
  const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
  );
  statusBarItem.command = 'sqliteQuery.openQuery';
  statusBarItem.text = '$(comment-discussion) SQLite Chat';
  statusBarItem.show();
  context.subscriptions.push(statusBarItem);
}

function openChatPanel(context: vscode.ExtensionContext) {
  const column = vscode.ViewColumn.One;

  if (currentPanel) {
    currentPanel.reveal(column);
    return;
  }

  currentPanel = vscode.window.createWebviewPanel(
    'sqliteChat',
    'SQLite AI Chat',
    column,
    {
      enableScripts: true,
      enableForms: true,
      retainContextWhenHidden: true
    }
  );

  currentPanel.webview.html = getChatWebviewContent(dbBuffer!);

  currentPanel.onDidDispose(
    () => {
      currentPanel = undefined;
    },
    undefined,
    []
  );

  // Webview?먯꽌 硫붿떆吏 ?섏떊
  currentPanel.webview.onDidReceiveMessage(
    (message) => {
      switch (message.command) {
        case 'generateQuery':
          const query = generateSQLQuery(message.question, message.tableName);
          currentPanel?.webview.postMessage({ type: 'queryGenerated', query, hint: message.hint });
          break;
      }
    },
    undefined,
    []
  );
}

function generateSQLQuery(question: string, tableName: string): string {
  const helper = sqlHelper.suggestQueries(question);
  
  switch (helper.type) {
    case 'COUNT':
      return sqlHelper.generateCountQuery(tableName);
    case 'SCHEMA':
      return sqlHelper.generateDescribeQuery(tableName);
    default:
      return sqlHelper.generateSelectQuery(tableName);
  }
}

function getChatWebviewContent(dbBuffer: Buffer): string {
  const dbBase64 = dbBuffer.toString('base64');

  return `
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>SQLite AI Chat</title>
      <script src="https://sql.js.org/dist/sql-wasm.js"></script>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
          background: var(--vscode-editor-background);
          color: var(--vscode-editor-foreground);
          height: 100vh;
          display: flex;
          flex-direction: column;
        }
        
        .header {
          padding: 15px;
          border-bottom: 1px solid var(--vscode-input-border);
          background: var(--vscode-terminal-background);
        }
        
        .header h1 {
          font-size: 18px;
          margin: 0;
          color: var(--vscode-terminal-ansiCyan);
        }
        
        .chat-container {
          flex: 1;
          overflow-y: auto;
          padding: 15px;
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        
        .message {
          display: flex;
          gap: 10px;
          margin-bottom: 15px;
          animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
          justify-content: flex-end;
        }
        
        .message-content {
          max-width: 70%;
          padding: 10px 12px;
          border-radius: 8px;
          word-wrap: break-word;
        }
        
        .message.user .message-content {
          background: var(--vscode-button-background);
          color: var(--vscode-button-foreground);
        }
        
        .message.bot .message-content {
          background: var(--vscode-input-background);
          border: 1px solid var(--vscode-input-border);
          color: var(--vscode-input-foreground);
        }
        
        .message.system .message-content {
          background: rgba(0, 212, 255, 0.1);
          color: var(--vscode-terminal-ansiCyan);
          border-left: 3px solid var(--vscode-terminal-ansiCyan);
        }
        
        .message-header {
          font-size: 11px;
          opacity: 0.7;
          margin-bottom: 5px;
        }
        
        .message-code {
          background: var(--vscode-editor-background);
          padding: 8px;
          border-radius: 4px;
          font-family: monospace;
          font-size: 12px;
          overflow-x: auto;
          margin-top: 8px;
          border: 1px solid var(--vscode-input-border);
        }
        
        .input-area {
          padding: 15px;
          border-top: 1px solid var(--vscode-input-border);
          background: var(--vscode-terminal-background);
        }
        
        .input-group {
          display: flex;
          gap: 8px;
        }
        
        .input-group input {
          flex: 1;
          padding: 8px 12px;
          background: var(--vscode-input-background);
          color: var(--vscode-input-foreground);
          border: 1px solid var(--vscode-input-border);
          border-radius: 4px;
          font-size: 13px;
        }
        
        .input-group input:focus {
          outline: none;
          border-color: var(--vscode-terminal-ansiCyan);
        }
        
        .input-group button {
          padding: 8px 16px;
          background: var(--vscode-button-background);
          color: var(--vscode-button-foreground);
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-weight: 500;
        }
        
        .input-group button:hover {
          background: var(--vscode-button-hoverBackground);
        }
        
        .table-selector {
          margin-top: 8px;
          font-size: 12px;
        }
        
        .table-selector label {
          display: block;
          margin-bottom: 5px;
          opacity: 0.8;
        }
        
        .table-selector select {
          width: 100%;
          padding: 6px;
          background: var(--vscode-input-background);
          color: var(--vscode-input-foreground);
          border: 1px solid var(--vscode-input-border);
          border-radius: 4px;
          font-size: 12px;
        }
        
        .quick-buttons {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 8px;
          margin-top: 8px;
        }
        
        .quick-btn {
          padding: 6px;
          background: rgba(0, 212, 255, 0.1);
          color: var(--vscode-terminal-ansiCyan);
          border: 1px solid var(--vscode-terminal-ansiCyan);
          border-radius: 4px;
          font-size: 11px;
          cursor: pointer;
          transition: all 0.2s;
        }
        
        .quick-btn:hover {
          background: rgba(0, 212, 255, 0.2);
        }
        
        .loading {
          display: inline-block;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: currentColor;
          animation: pulse 1.5s ease-in-out infinite;
          margin-right: 5px;
        }
        
        @keyframes pulse {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 1; }
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>?뮠 SQLite AI Chat</h1>
      </div>
      
      <div class="chat-container" id="chatContainer">
        <div class="message system">
          <div class="message-content">
            <div class="message-header">?쨼 Assistant</div>
            <div>?덈뀞?섏꽭?? SQLite ?곗씠?곕쿋?댁뒪?????吏덈Ц?댁＜?몄슂. ?? "users ?뚯씠釉붿쓽 紐⑤뱺 ?곗씠??蹂댁뿬以?</div>
          </div>
        </div>
      </div>
      
      <div class="input-area">
        <div class="table-selector">
          <label for="tableSelect">?뱤 ?뚯씠釉??좏깮:</label>
          <select id="tableSelect">
            <option>?뚯씠釉?濡쒕뱶 以?..</option>
          </select>
        </div>
        
        <div class="quick-buttons" id="quickButtons"></div>
        
        <div class="input-group">
          <input type="text" id="chatInput" placeholder="吏덈Ц???낅젰?섏꽭??.." />
          <button onclick="sendMessage()">?뱾 ?꾩넚</button>
        </div>
      </div>

      <script>
        let db = null;
        let SQL = null;
        let currentTable = 'users';
        const vscode = acquireVsCodeApi();

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
            loadTables();
            addSystemMessage('???곗씠?곕쿋?댁뒪 濡쒕뱶 ?꾨즺! ?대뼡 吏덈Ц???덉쑝?몄슂?');
          } catch (error) {
            addSystemMessage('???ㅻ쪟: ' + error.message);
          }
        }

        function loadTables() {
          try {
            const result = db.exec("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name");
            const tables = result.length > 0 ? result[0].values.map(row => row[0]) : [];
            
            const select = document.getElementById('tableSelect');
            select.innerHTML = tables.map(t => \`<option value="\${t}">\${t}</option>\`).join('');
            currentTable = tables[0] || 'users';
            
            // ??踰꾪듉 ?앹꽦
            generateQuickButtons(currentTable);
          } catch (error) {
            console.error(error);
          }
        }

        function generateQuickButtons(tableName) {
          const buttons = [
            { text: '?뱥 ?뚯씠釉?蹂닿린', query: \`users??泥섏쓬 10媛??곗씠?곕? 蹂댁뿬以?` },
            { text: '?뵢 媛쒖닔 ?뺤씤', query: \`${tableName}??紐?媛쒖쓽 ?곗씠?곌? ?덉뼱?\` },
            { text: '?룛截?援ъ“ ?뺤씤', query: \`${tableName}??而щ읆 援ъ“瑜?蹂댁뿬以?` },
            { text: '???덉젣', query: 'SQL 荑쇰━ ?덉젣瑜?蹂댁뿬以? }
          ];
          
          const container = document.getElementById('quickButtons');
          container.innerHTML = buttons.map(btn => 
            \`<button class="quick-btn" onclick="sendMessage('\${btn.query}')">\${btn.text}</button>\`
          ).join('');
        }

        document.getElementById('tableSelect').addEventListener('change', (e) => {
          currentTable = e.target.value;
          generateQuickButtons(currentTable);
        });

        function sendMessage(presetQuery = null) {
          let userMessage = presetQuery || document.getElementById('chatInput').value.trim();
          if (!userMessage) return;

          addUserMessage(userMessage);
          document.getElementById('chatInput').value = '';

          // AI ?묐떟 ?쒕??덉씠??
          setTimeout(() => {
            const response = generateAIResponse(userMessage, currentTable);
            addBotMessage(response.message);
            
            if (response.query) {
              executeQueryAndShow(response.query);
            }
          }, 300);
        }

        function generateAIResponse(question, tableName) {
          const lower = question.toLowerCase();

          if (lower.includes('?덉젣')) {
            return {
              message: '?뱴 SQL 荑쇰━ ?덉젣?ㅼ엯?덈떎:',
              query: null
            };
          }

          if (lower.includes('蹂댁뿬')) {
            return {
              message: \`??\${tableName} ?뚯씠釉붿쓣 ?쒖떆?⑸땲??\`,
              query: \`SELECT * FROM \${tableName} LIMIT 10\`
            };
          }

          if (lower.includes('紐뉕컻') || lower.includes('媛쒖닔') || lower.includes('count')) {
            return {
              message: \`?뱤 \${tableName} ?뚯씠釉붿쓽 珥?媛쒖닔瑜??뺤씤?⑸땲??\`,
              query: \`SELECT COUNT(*) as 珥앷컻??FROM \${tableName}\`
            };
          }

          if (lower.includes('援ъ“') || lower.includes('而щ읆') || lower.includes('?ㅽ궎留?)) {
            return {
              message: \`?룛截?\${tableName} ?뚯씠釉붿쓽 援ъ“?낅땲??\`,
              query: \`PRAGMA table_info(\${tableName})\`
            };
          }

          return {
            message: \`??\${tableName} ?뚯씠釉붿뿉???곗씠?곕? 議고쉶?⑸땲??\`,
            query: \`SELECT * FROM \${tableName} LIMIT 10\`
          };
        }

        function executeQueryAndShow(sql) {
          try {
            const result = db.exec(sql);
            if (result.length === 0) {
              addSystemMessage('寃곌낵: 0媛???);
              return;
            }

            const { columns, values } = result[0];
            const table = \`
              <table style="width:100%; border-collapse: collapse; font-size: 12px;">
                <tr style="background: rgba(0,212,255,0.2);">
                  \${columns.map(c => \`<th style="padding:6px; text-align:left; border: 1px solid rgba(255,255,255,0.1);">\${c}</th>\`).join('')}
                </tr>
                \${values.slice(0, 5).map(row => \`
                  <tr>
                    \${row.map(v => \`<td style="padding:6px; border: 1px solid rgba(255,255,255,0.1);">\${v === null ? 'NULL' : v}</td>\`).join('')}
                  </tr>
                \`).join('')}
              </table>
            \`;
            
            const msg = document.createElement('div');
            msg.className = 'message bot';
            msg.innerHTML = \`<div class="message-content">
              <div class="message-header">?뱤 寃곌낵</div>
              <div style="overflow-x: auto;">\${table}</div>
              <div class="message-code" style="margin-top:8px;font-size:11px;opacity:0.7;">\${sql}</div>
            </div>\`;
            document.getElementById('chatContainer').appendChild(msg);
            document.getElementById('chatContainer').scrollTop = document.getElementById('chatContainer').scrollHeight;
          } catch (error) {
            addSystemMessage('??荑쇰━ ?ㅻ쪟: ' + error.message);
          }
        }

        function addUserMessage(text) {
          const msg = document.createElement('div');
          msg.className = 'message user';
          msg.innerHTML = \`<div class="message-content">
            <div class="message-header">?뫀 You</div>
            \${text}
          </div>\`;
          document.getElementById('chatContainer').appendChild(msg);
          document.getElementById('chatContainer').scrollTop = document.getElementById('chatContainer').scrollHeight;
        }

        function addBotMessage(text) {
          const msg = document.createElement('div');
          msg.className = 'message bot';
          msg.innerHTML = \`<div class="message-content">
            <div class="message-header">?쨼 Assistant</div>
            \${text}
          </div>\`;
          document.getElementById('chatContainer').appendChild(msg);
          document.getElementById('chatContainer').scrollTop = document.getElementById('chatContainer').scrollHeight;
        }

        function addSystemMessage(text) {
          const msg = document.createElement('div');
          msg.className = 'message system';
          msg.innerHTML = \`<div class="message-content">\${text}</div>\`;
          document.getElementById('chatContainer').appendChild(msg);
          document.getElementById('chatContainer').scrollTop = document.getElementById('chatContainer').scrollHeight;
        }

        document.getElementById('chatInput').addEventListener('keypress', (e) => {
          if (e.key === 'Enter') sendMessage();
        });

        window.addEventListener('load', initDatabase);
      </script>
    </body>
    </html>
  `;
}

export function deactivate() {}

