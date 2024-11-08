from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import yt_dlp
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/submit")
def download_video(userInput: str = Form(...)):
    try:
       
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get(userInput)

        video_links = driver.find_elements("id", "video-title-link")
        video_urls = []
        for i in range(min(1, len(video_links))):  # Limit to first two videos for demonstration
            video_url = video_links[i].get_attribute("href")
            video_urls.append(video_url)

    
        driver.quit()

        for url in video_urls:
            yt_dlp.YoutubeDL().download([url])

        return JSONResponse(content={"message": "Download complete!"})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    