import json
import logging
import os
from aligo import Aligo
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

def tool(localPath,info):
    localPath = localPath[1:-1]
    if os.path.isdir(localPath):
        ali.upload_folder(localPath, parent_file_id=info['id'])
    else:
        ali.upload_file(file_path=localPath, parent_file_id=info['id'])
    app.logger.info(f"本地文件[{localPath}] 已上传到 阿里云盘 [{info['name']}]")

@app.route('/upload', methods=["POST"])
def upload_mp4():
    info = json.loads(request.data).get("info")
    localPath = json.loads(request.data).get('path')
    if not info or not localPath:
        return Response(status=404)
    tool(localPath, info)
    return jsonify({'msg': True})


@app.route('/MP4')
def get_mp4listInfo():
    data = []
    ll = ali.get_file_list()
    for file in ll:  # 遍历文件列表
        data.append({"name": file.name, 'id': file.file_id})
    return jsonify({'data': data})


@app.route('/MP4list')
def get_mp4_list():
    id = request.args.get('id', None)
    if not id:
        return Response(status=404)
    data = []
    ll = ali.get_file_list(id)
    try:
        for file in ll:  # 遍历文件列表
            data.append({"name": file.name, 'id': file.file_id})
    except:
        return jsonify({'data': []})
    return jsonify({'data': data})

if __name__ == '__main__':
    # 阿里云盘 日志
    logger = logging.getLogger("aligo")
    logPath = os.path.join(os.getcwd(), "aligo.log")
    logger.addHandler(logging.FileHandler(logPath, encoding="utf-8"))
    logger.setLevel(logging.INFO)
    ali = Aligo(level=logging.ERROR)
    app.run(debug=False, threaded=True, host='127.0.0.1', port=57801)
