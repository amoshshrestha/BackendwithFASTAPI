import os



from fastapi import Depends, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app import schemas
from backend.app.core.oauth2 import get_current_user
from backend.app.database import database
from backend.app.database.database import engine

from backend.app.routers.authentication import router as auth_router
from backend.app.routers.user import router as user_router
from backend.app.routers.admin import router as admin_router

app = FastAPI()

# for now allowing all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.Base.metadata.create_all(engine)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)




# @app.post("/upload/", tags=["uploads"])
# async def create_upload_file(
#     file: UploadFile, current_user: schemas = Depends(get_current_user)
# ):
#     try:
#         pitch_classes = [
#             "C",
#             "C#",
#             "D",
#             "D#",
#             "E",
#             "F",
#             "F#",
#             "G",
#             "G#",
#             "A",
#             "A#",
#             "B",
#         ]
#         chords = ["A", "Am", "Bm", "C", "D", "Dm", "E", "Em", "F", "G"]

#         temp_file_path = f"temp_{file.filename}"
#         with open(temp_file_path, "wb") as temp_file:
#             temp_file.write(await file.read())

#         profiler = PitchClassProfiler(temp_file_path)
#         pcp_profiles, timestamps = profiler.get_profiles(
#             window_duration=1.0, overlap=0.0
#         )

#         with open(svm_model_path, "rb") as f:
#             model = pickle.load(f)
#         results = []
#         for i, profile in enumerate(pcp_profiles):
#             profile_df = pd.DataFrame([profile], columns=pitch_classes)
#             prediction = model.predict(profile_df)
#             index = int(prediction[0])
#             predicted_chord = chords[index]
#             results.append({"timestamp": timestamps[i], "chord": predicted_chord})

#         consolidated_results = consolidate_chords(results)

#         os.remove(temp_file_path)

#         return {"filename": file.filename, "predictions": consolidated_results}
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
