"""
author: 
Description: 
Fixed: 
Usage: 
"""

from fastapi import FastAPI
# from clinic import router as clinic_router
# from favorite import router as favorite_router
# from user import router as user_router
# from pet import router as pet_router
# from available_time import router as available_router
# from species import router as species_router 
# from reservation import router as reservation_router
# from myprofile import mypage_router
# from auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
import hosts
app = FastAPI()

# app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(clinic_router, prefix="/clinic", tags=["clinic"])
# app.include_router(favorite_router, prefix="/favorite", tags=["favorite"])
# app.include_router(user_router, prefix="/user", tags=["user"])
# app.include_router(pet_router, prefix="/pet", tags=["pet"])
# app.include_router(mypage_router, prefix="/mypage", tags=["mypage"])
# app.include_router(available_router, prefix="/available", tags=["available"])
# app.include_router(species_router, prefix="/species", tags=["species"])
# app.include_router(reservation_router, prefix="/reservation", tags=["reservation"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 도메인 리스트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def test():
    redis_client = await hosts.get_redis_connection()
        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 6003)
    hosts.get_redis_connection()