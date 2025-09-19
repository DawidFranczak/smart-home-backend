from pydantic import BaseModel
class AddTagPayload(BaseModel):
    pass


class OnReadPayload(BaseModel):
    pass


class OnReadSuccessPayload(BaseModel):
    pass


class OnReadFailurePayload(BaseModel):
    pass

class AccessGrantedPayload(BaseModel):
    pass


class AccessDeniedPayload(BaseModel):
    pass