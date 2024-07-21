from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
import os
from typing import Optional, List
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class prod_req(BaseModel):
    name: str
    price: int
    image_url: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class prod_res(prod_req):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)


class carts_req(prod_req):
    pass



class carts_res(prod_res):
    pass
