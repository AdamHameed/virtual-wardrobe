from sqlalchemy.orm import Session

from app.auth.password import get_password_hash, verify_password
from app.auth.tokens import create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.services.exceptions import bad_request


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)

    def register(self, payload: RegisterRequest) -> AuthResponse:
        existing_user = self.repository.get_by_email(payload.email)
        if existing_user is not None:
            raise bad_request("A user with that email already exists.")

        user = User(
            email=payload.email,
            display_name=payload.display_name,
            hashed_password=get_password_hash(payload.password),
            is_active=True,
            extra_data=payload.extra_data,
        )
        created_user = self.repository.create(user)
        return self._build_auth_response(created_user)

    def login(self, payload: LoginRequest) -> AuthResponse:
        user = self.repository.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise bad_request("Invalid email or password.")
        if not user.is_active:
            raise bad_request("User account is inactive.")
        return self._build_auth_response(user)

    def _build_auth_response(self, user: User) -> AuthResponse:
        token = create_access_token(subject=str(user.id))
        return AuthResponse(
            access_token=token,
            token_type="bearer",
            user=user,
        )
