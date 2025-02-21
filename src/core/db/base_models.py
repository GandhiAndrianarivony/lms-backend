from datetime import datetime, timezone
from sqlmodel import (
    SQLModel,
    Field,
    DateTime,
    # Column,
)

# class TimeStamped(SQLModel):
#     created_at: datetime = Field(
#         sa_column=Column(
#             DateTime(timezone=True),
#             default=lambda: datetime.now(timezone.utc),
#         )
#     )
#     updated_at: datetime = Field(
#         sa_column=Column(
#             DateTime(timezone=True),
#             onupdate=lambda: datetime.now(timezone.utc),
#             nullable=True,
#         )
#     )


class TimeStamped(SQLModel, table=False):
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "default": lambda: datetime.now(timezone.utc),
            "nullable": False,
        },
    )
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
            "nullable": True,
        },
    )
