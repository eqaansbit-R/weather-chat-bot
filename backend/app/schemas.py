from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    response: str
    city: str | None = None
    temperature: float | None = None
    feels_like: float | None = None
    description: str | None = None

class DashboardStats(BaseModel):
    total_users: int
    total_messages: int
    cities_queried: int
    avg_temperature: float
