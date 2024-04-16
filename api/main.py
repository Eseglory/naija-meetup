from fastapi import FastAPI
from .routes import users, auth, password_reset, post_content
# import uvicorn
# from os import getenv

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(password_reset.router)
# app.include_router(post_content.router)

# if __name__ == "__main__":
#     port = int(getenv("PORT, 8000"))
#     uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=True)
