import logging
import json
import os

import boto3
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# 設定
logging.basicConfig(level=logging.INFO)
load_dotenv()

# Secrets Managerから接続情報を取得
def get_db_credentials(secret_name, region_name):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        return secret
    except Exception as e:
        logging.error(f"Error retrieving secrets: {e}")
        raise

# ORMベースの設定
Base = declarative_base()

# データベースの接続設定
def get_database_engine(db_credentials):
    username = db_credentials["username"]
    password = db_credentials["password"]
    host = db_credentials["host"]
    dbname = db_credentials["dbname"]
    port = db_credentials.get("port", 3306)  # ポートが指定されていない場合はデフォルトで5432

    # PostgreSQLの接続URLを構築
    database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(database_url, echo=True)  # echo=TrueでSQLログを表示
    return engine

# セッションの作成
def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# サンプルバッチ処理
def run_batch_job():
    logging.info("Starting batch job...")
    secret_name = os.getenv("SECRET_NAME")
    region_name = os.getenv("REGION_NAME")

    if not secret_name or not region_name:
        logging.error("SECRET_NAMEまたはREGION_NAMEが設定されていません。")
        return

    # Secrets Managerから接続情報を取得
    logging.info("Getting credentials to db...")
    db_credentials = get_db_credentials(secret_name, region_name)

    # データベース接続
    logging.info("Connecting to db...")
    engine = get_database_engine(db_credentials)

    # セッションを取得してバッチ処理を実行
    logging.info("Getting Session of db...")
    session = get_session(engine)
    

    # データベースに対するクエリ例（必要に応じてテーブルやORMクラスを定義）
    logging.info("Getting data from db...")
    result = session.execute(text("SELECT 'hello world'"))
    for row in result:
        print(f"Test Query Result: {row[0]}")
    
    session.close()
    logging.info("Batch job completed.")

if __name__ == "__main__":
    run_batch_job()
