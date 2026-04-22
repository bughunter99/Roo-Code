import Database from 'better-sqlite3';
import * as path from 'path';

export class SQLiteManager {
  private db: Database.Database | null = null;
  private dbPath: string;

  constructor(dbPath: string) {
    this.dbPath = dbPath;
  }

  connect(): boolean {
    try {
      this.db = new Database(this.dbPath);
      return true;
    } catch (error) {
      console.error('데이터베이스 연결 실패:', error);
      return false;
    }
  }

  disconnect(): void {
    if (this.db) {
      this.db.close();
      this.db = null;
    }
  }

  executeQuery(sql: string): { success: boolean; data?: any[]; error?: string } {
    if (!this.db) {
      return { success: false, error: '데이터베이스가 연결되지 않았습니다' };
    }

    try {
      const stmt = this.db.prepare(sql);
      const results = stmt.all();
      return { success: true, data: results };
    } catch (error: any) {
      return { success: false, error: error.message || '쿼리 실행 중 오류 발생' };
    }
  }

  getTables(): string[] {
    if (!this.db) {
      return [];
    }

    try {
      const stmt = this.db.prepare(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
      );
      const tables = stmt.all() as { name: string }[];
      return tables.map((t) => t.name);
    } catch (error) {
      console.error('테이블 목록 조회 실패:', error);
      return [];
    }
  }

  getTableSchema(tableName: string): any[] {
    if (!this.db) {
      return [];
    }

    try {
      const stmt = this.db.prepare(`PRAGMA table_info(${tableName})`);
      return stmt.all();
    } catch (error) {
      console.error('테이블 스키마 조회 실패:', error);
      return [];
    }
  }
}
