from mysql.connector import pooling
import os, logging

DB_CONFIG = {
  "host": os.getenv("AWS_RDS_HOST"),
  "port": os.getenv("AWS_RDS_PORT"),
  "user": os.getenv("AWS_RDS_USER"),
  "password": os.getenv("AWS_RDS_PW"),
  "database": os.getenv("AWS_RDS_DB"),
  "charset": "utf8"
}

class SQLPool:
  
  def __init__(self):
    
    self.connection_pool = pooling.MySQLConnectionPool(
      pool_name = "mypool",
      pool_size = 10,
      **DB_CONFIG,
    )
    print("MySQL connection pool created.")
    
    
  def get_pool_connection(self):
    return self.connection_pool.get_connection()
  
  def get_cursor(self, query, params=None, fetch=False):
    """執行查詢或新增，fetch=True 時回傳資料"""
    conn = self.get_pool_connection()
    cursor = conn.cursor(dictionary=True)
    try:
      cursor.execute(query, params)
      if fetch:
        return cursor.fetchall()
      conn.commit()
    except Exception as e:
      conn.rollback()
      raise e  # 可自訂錯誤處理
    finally:
      cursor.close()
      conn.close()  # 歸還連線
      
      
  def check_processlist(self):
    conn = self.get_pool_connection()
    cursor = conn.cursor(dictionary=True)
    try:
      cursor.execute("SHOW FULL PROCESSLIST")
      processlist = cursor.fetchall()
      
      total = len(processlist)
      sleeping = sum(1 for p in processlist if p["Command"] == "Sleep")
      running = sum(1 for p in processlist if p["Command"] == "Query")
      long_running = [p for p in processlist if p["Command"] == "Query" and p["Time"] > 5]
      
      logging.basicConfig(level=logging.INFO)
      logger = logging.getLogger(__name__)
      logger.warning(f"Long running query > 5s: {long_running}")

      print(f"總連線數：{total}")
      print(f"Sleep 狀態連線數：{sleeping}")
      print(f"執行中查詢數：{running}")
      print(f"長時間執行中的查詢（> 5 秒）:{long_running}")
      
      for process in processlist:
        if process["Command"] == "Sleep" and process["Time"] > 10:
          cursor.execute(f"KILL {process['Id']}")
          print(f"Killed connection {process['Id']} - Sleep for {process['Time']} seconds.")
      
    finally:
      cursor.close()
      conn.close()
        
db_pool = SQLPool()          
    