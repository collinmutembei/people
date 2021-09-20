from sqlmodel import Field, SQLModel


class ProfileBase(SQLModel):
    first_name: str
    last_name: str


class Profile(ProfileBase, table=True):
    id: int = Field(default=None, primary_key=True)
    deleted: bool = Field(default=False)


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileDelete(ProfileBase):
    id: int
    deleted: bool
