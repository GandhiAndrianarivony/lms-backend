import datetime as dt

from sqlmodel import SQLModel, Field, Column, DateTime


# class TimeStamped(SQLModel):
#     created_at: dt.datetime = Field(
#         sa_column=Column(
#             DateTime(timezone=True),
#             default=lambda: dt.datetime.now(dt.timezone.utc),
#         )
#     )
#     updated_at: dt.datetime = Field(
#         sa_column=Column(
#             DateTime(timezone=True),
#             onupdate=lambda: dt.datetime.now(dt.timezone.utc),
#             nullable=True,
#         )
#     )


class TimeStamped(SQLModel, table=False):
    created_at: dt.datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "default": lambda: dt.datetime.now(dt.timezone.utc),
            "nullable": False,
        }
    )
    updated_at: dt.datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": lambda: dt.datetime.now(dt.timezone.utc),
            "nullable": True,
        }
    )