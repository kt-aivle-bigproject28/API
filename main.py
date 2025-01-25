from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from azure.storage.blob import BlobServiceClient
from typing import List
import os

app = FastAPI()

# Azure Blob Storage 설정
connection_string = "YOUR_KEY"
container_name = "blob-28"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

@app.post("/text_to_webtoon")
async def text_to_webtoon(text: UploadFile = File(...)):
    try:
        # Blob 컨테이너에서 이미지 파일 목록 가져오기
        image_paths = []
        blobs = container_client.list_blobs()
        
        for blob in blobs:
            # 이미지 파일 필터링
            if blob.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Blob URL 생성
                blob_client = container_client.get_blob_client(blob.name)
                image_paths.append(blob_client.url)
        
        return {"image_paths": image_paths}
    
    except Exception as e:
        return {"error": str(e)}
