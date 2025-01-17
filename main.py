from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from typing import List

app = FastAPI()

# 미리 정해둔 이미지 폴더 경로
PREDEFINED_IMAGE_FOLDER = "C:/uploads/"

@app.post("/text_to_webtoon")
async def text_to_webtoon(text: UploadFile = File(...)):
    # 텍스트 파일의 내용은 무시하고 미리 정해둔 폴더에서 이미지를 가져옵니다.
    
    # 디렉토리 존재 여부 확인
    if not os.path.exists(PREDEFINED_IMAGE_FOLDER):
        return {"error": "Predefined image folder not found"}
    
    # 디렉토리 내 이미지 파일 목록 가져오기
    image_files = [f for f in os.listdir(PREDEFINED_IMAGE_FOLDER) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # 이미지 파일 이름 리스트 생성
    image_paths = image_files  # 전체 경로 대신 파일 이름만 리스트에 저장
    print(image_paths)
    
    return {"image_paths": image_paths}

@app.get("/image/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join(PREDEFINED_IMAGE_FOLDER, image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    return {"error": "Image not found"}
