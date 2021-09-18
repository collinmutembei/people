from sqlmodel import Field, SQLModel


class ProfileBase(SQLModel):
    first_name: str
    last_name: str
    surname: str


class Profile(ProfileBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ProfileCreate(ProfileBase):
    pass
