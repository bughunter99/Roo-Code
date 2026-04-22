import sqlite3
from pathlib import Path

base = Path(r"d:\data3\Roo-Code\dc_tools")


def init_tool1() -> None:
    db_path = base / "tool1" / "tool1_sample.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS items (
          item_cd TEXT PRIMARY KEY,
          item_nm TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS orders (
          order_id TEXT PRIMARY KEY,
          customer TEXT NOT NULL,
          item_cd TEXT NOT NULL,
          order_qty INTEGER NOT NULL,
          due_date TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS production (
          prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
          order_id TEXT NOT NULL,
          produced_qty INTEGER NOT NULL,
          scrap_qty INTEGER NOT NULL,
          prod_ts TEXT NOT NULL
        );

        DELETE FROM items;
        DELETE FROM orders;
        DELETE FROM production;

        INSERT INTO items(item_cd,item_nm) VALUES
         ('ITEM-A','Widget A'),('ITEM-B','Widget B'),('ITEM-C','Widget C');
        INSERT INTO orders(order_id,customer,item_cd,order_qty,due_date) VALUES
         ('ORD-1001','ALPHA','ITEM-A',120,'2026-04-25'),
         ('ORD-1002','BETA','ITEM-B',200,'2026-04-27'),
         ('ORD-1003','GAMMA','ITEM-C',150,'2026-04-29');
        INSERT INTO production(order_id,produced_qty,scrap_qty,prod_ts) VALUES
         ('ORD-1001',110,3,'2026-04-21 09:00:00'),
         ('ORD-1002',140,5,'2026-04-21 12:10:00'),
         ('ORD-1003',60,1,'2026-04-22 08:40:00');
        """
    )
    conn.commit()
    conn.close()


def init_tool2() -> None:
    db_path = base / "tool2" / "tool2_sample.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS items (
          item_cd TEXT PRIMARY KEY,
          item_nm TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS lots (
          lot_no TEXT PRIMARY KEY,
          item_cd TEXT NOT NULL,
          work_center TEXT NOT NULL,
          start_ts TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS qc_results (
          qc_id INTEGER PRIMARY KEY AUTOINCREMENT,
          lot_no TEXT NOT NULL,
          item_cd TEXT NOT NULL,
          inspected_qty INTEGER NOT NULL,
          defect_qty INTEGER NOT NULL,
          inspect_ts TEXT NOT NULL
        );

        DELETE FROM items;
        DELETE FROM lots;
        DELETE FROM qc_results;

        INSERT INTO items(item_cd,item_nm) VALUES
         ('ITEM-A','Widget A'),('ITEM-B','Widget B'),('ITEM-C','Widget C');
        INSERT INTO lots(lot_no,item_cd,work_center,start_ts) VALUES
         ('LOT-001','ITEM-A','WC-10','2026-04-20 07:30:00'),
         ('LOT-002','ITEM-B','WC-20','2026-04-20 10:00:00'),
         ('LOT-003','ITEM-C','WC-30','2026-04-21 08:00:00');
        INSERT INTO qc_results(lot_no,item_cd,inspected_qty,defect_qty,inspect_ts) VALUES
         ('LOT-001','ITEM-A',100,2,'2026-04-20 15:00:00'),
         ('LOT-002','ITEM-B',120,8,'2026-04-20 18:20:00'),
         ('LOT-003','ITEM-C',90,1,'2026-04-21 16:45:00');
        """
    )
    conn.commit()
    conn.close()


def init_tool3() -> None:
    db_path = base / "tool3" / "tool3_sample.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS items (
          item_cd TEXT PRIMARY KEY,
          item_nm TEXT NOT NULL,
          unit TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS stock_onhand (
          item_cd TEXT NOT NULL,
          warehouse TEXT NOT NULL,
          onhand_qty INTEGER NOT NULL,
          safety_stock INTEGER NOT NULL,
          PRIMARY KEY(item_cd, warehouse)
        );
        CREATE TABLE IF NOT EXISTS stock_moves (
          move_id INTEGER PRIMARY KEY AUTOINCREMENT,
          item_cd TEXT NOT NULL,
          warehouse TEXT NOT NULL,
          move_type TEXT NOT NULL,
          qty INTEGER NOT NULL,
          move_ts TEXT NOT NULL
        );

        DELETE FROM items;
        DELETE FROM stock_onhand;
        DELETE FROM stock_moves;

        INSERT INTO items(item_cd,item_nm,unit) VALUES
         ('ITEM-A','Widget A','PCS'),('ITEM-B','Widget B','PCS'),('ITEM-C','Widget C','PCS');
        INSERT INTO stock_onhand(item_cd,warehouse,onhand_qty,safety_stock) VALUES
         ('ITEM-A','WH-01',45,50),
         ('ITEM-B','WH-01',180,80),
         ('ITEM-C','WH-02',30,40);
        INSERT INTO stock_moves(item_cd,warehouse,move_type,qty,move_ts) VALUES
         ('ITEM-A','WH-01','OUT',20,'2026-04-21 09:00:00'),
         ('ITEM-B','WH-01','IN',60,'2026-04-21 11:10:00'),
         ('ITEM-C','WH-02','OUT',10,'2026-04-22 10:05:00');
        """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_tool1()
    init_tool2()
    init_tool3()
    print("Created sample DBs under dc_tools/tool1~tool3")
