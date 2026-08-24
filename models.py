# # from sqlalchemy import Column, Integer, String, DateTime, Boolean
# # from sqlalchemy.sql import func

# # from database import Base


# # class User(Base):
# #     __tablename__ = "users"

# #     id = Column(Integer, primary_key=True, index=True)

# #     username = Column(
# #         String(100),
# #         unique=True,
# #         index=True,
# #         nullable=False,
# #     )

# #     full_name = Column(
# #         String(255),
# #         nullable=True,
# #     )

# #     hashed_password = Column(
# #         String(255),
# #         nullable=False,
# #     )

# #     is_active = Column(
# #         Boolean,
# #         default=True,
# #         nullable=False,
# #     )

# #     created_at = Column(
# #         DateTime(timezone=True),
# #         server_default=func.now(),
# #         nullable=False,
# #     )

# from sqlalchemy import Column, Integer, String, DateTime, Boolean
# from sqlalchemy.sql import func

# from database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)

#     username = Column(
#         String(100),
#         unique=True,
#         index=True,
#         nullable=False,
#     )

#     email = Column(
#         String(255),
#         unique=True,
#         index=True,
#         nullable=True,          # nullable so existing rows aren't broken
#     )

#     full_name = Column(
#         String(255),
#         nullable=True,
#     )

#     hashed_password = Column(
#         String(255),
#         nullable=False,
#     )

#     is_active = Column(
#         Boolean,
#         default=True,
#         nullable=False,
#     )

#     created_at = Column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#         nullable=False,
#     )


from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean,
    ForeignKey, Text, JSON, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id             = Column(Integer, primary_key=True, index=True)
    username       = Column(String(100), unique=True, index=True, nullable=False)
    email          = Column(String(255), unique=True, index=True, nullable=True)
    full_name      = Column(String(255), nullable=True)
    hashed_password= Column(String(255), nullable=False)
    is_active      = Column(Boolean, default=True, nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    surveys        = relationship("Survey", back_populates="owner", cascade="all, delete-orphan")


class Survey(Base):
    __tablename__ = "surveys"

    id          = Column(Integer, primary_key=True, index=True)
    owner_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title       = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status      = Column(String(20), default="draft")   # draft | active | closed
    qr_code     = Column(Text, nullable=True)            # base64 PNG
    # When True, respondents must arrive with a valid per-person invite token (?token=...)
    requires_invite = Column(Boolean, default=False, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    owner       = relationship("User", back_populates="surveys")
    questions   = relationship("Question", back_populates="survey", cascade="all, delete-orphan", order_by="Question.order")
    responses   = relationship("Response", back_populates="survey", cascade="all, delete-orphan")
    invites     = relationship("Invite", back_populates="survey", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id          = Column(Integer, primary_key=True, index=True)
    survey_id   = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False)
    order       = Column(Integer, default=0)
    # Types: text | textarea | multiple_choice | checkbox | rating | dropdown | file | date
    type        = Column(String(30), nullable=False)
    text        = Column(Text, nullable=False)
    required    = Column(Boolean, default=False)
    options     = Column(JSON, nullable=True)   # list of strings for MCQ/dropdown/checkbox
    # Logic branching: {"if_answer": "Yes", "goto_question": 5}
    logic       = Column(JSON, nullable=True)
    min_rating  = Column(Integer, nullable=True)
    max_rating  = Column(Integer, nullable=True)

    survey      = relationship("Survey", back_populates="questions")
    answers     = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class Response(Base):
    __tablename__ = "responses"

    id              = Column(Integer, primary_key=True, index=True)
    survey_id       = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False)
    respondent_name = Column(String(255), nullable=True)
    respondent_email= Column(String(255), nullable=True)
    ip_address      = Column(String(60), nullable=True)
    submitted_at    = Column(DateTime(timezone=True), server_default=func.now())
    completion_pct  = Column(Float, default=100.0)
    # Links this response back to the unique invite link it was submitted from, if any
    invite_id       = Column(Integer, ForeignKey("invites.id", ondelete="SET NULL"), nullable=True)

    survey          = relationship("Survey", back_populates="responses")
    answers         = relationship("Answer", back_populates="response", cascade="all, delete-orphan")
    invite          = relationship("Invite", back_populates="response")


class Answer(Base):
    __tablename__ = "answers"

    id          = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    value       = Column(Text, nullable=True)       # plain text / single choice / rating
    values      = Column(JSON, nullable=True)        # multiple checkbox selections
    file_url    = Column(String(500), nullable=True) # uploaded file path

    response    = relationship("Response", back_populates="answers")
    question    = relationship("Question", back_populates="answers")


class Invite(Base):
    """A unique per-respondent survey link, generated in bulk from an uploaded CSV."""
    __tablename__ = "invites"

    id          = Column(Integer, primary_key=True, index=True)
    survey_id   = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False)
    token       = Column(String(64), unique=True, index=True, nullable=False)
    name        = Column(String(255), nullable=True)
    email       = Column(String(255), nullable=True)
    # pending | opened | completed
    status      = Column(String(20), default="pending")
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    opened_at   = Column(DateTime(timezone=True), nullable=True)
    completed_at= Column(DateTime(timezone=True), nullable=True)

    survey      = relationship("Survey", back_populates="invites")
    response    = relationship("Response", back_populates="invite", uselist=False)