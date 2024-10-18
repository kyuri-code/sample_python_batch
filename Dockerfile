# ベースイメージにPython 3.9を指定
FROM python:3.9-slim

# タイムゾーンを東京に設定
ENV TZ=Asia/Tokyo
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを作成
WORKDIR /app

# requirements.txt（必要なライブラリ）のコピーとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pythonスクリプトのコピー
COPY . /app

# コンテナ起動時に実行するコマンドを指定
CMD ["python3", "batch_job.py"]
