from app.models import dto


def user_link(user: dto.User) -> str:
    return f"@{user.username}"
