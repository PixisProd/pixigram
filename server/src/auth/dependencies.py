from typing import Annotated

from fastapi import Depends, HTTPException, status, Cookie

from server.src.auth.utils import verify_access_token
from server.src.auth import exceptions
from server.src.config import settings


user_dependency = Annotated[dict, Depends(verify_access_token)]

