from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import StrictStr

from app.models import Users


class UserFilter(Filter):
    search: Optional[StrictStr] = None

    class Constants(Filter.Constants):
        model = Users
        search_model_fields = ["id", "name", "email", "email"]
