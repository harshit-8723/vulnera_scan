from pydantic import BaseModel, HttpUrl

class WebsiteInput(BaseModel):
    url: HttpUrl