from fastapi import FastAPI, File, UploadFile, Form
from PIL import Image
import pytesseract
from googletrans import Translator
import io

app = FastAPI()
translator = Translator()

@app.get("/")
def root():
    return {"status": "server running"}

@app.post("/translate")
async def translate_image(
    file: UploadFile = File(...),
    target_lang: str = Form("en")
):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # OCR
    text = pytesseract.image_to_string(image, lang="eng+ben")

    if not text.strip():
        return {
            "text": "",
            "translated": "",
            "detected_lang": ""
        }

    # Auto language detect + translate
    result = translator.translate(text, dest=target_lang)

    return {
        "text": text,
        "translated": result.text,
        "detected_lang": result.src
    }
