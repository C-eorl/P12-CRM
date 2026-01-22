from src.domain.entities.entities import User


class UserPolicy:
    def __init__(self, user: User):
        self.user = user

    def can_create_client(self) -> bool:
        return self.user.is_commercial()

    def can_update_client(self) -> bool:
        return self.user.is_commercial()

    def can_delete_client(self) -> bool:
        return self.user.is_admin()

    def can_create_contrat(self) -> bool:
        return self.user.is_gestion()

    def can_update_contrat(self) -> bool:
        return self.user.is_gestion() or self.user.is_commercial()

    def can_delete_contrat(self) -> bool:
        return self.user.is_admin()

    def can_create_event(self) -> bool:
        return self.user.is_commercial()

    def can_update_event(self) -> bool:
        return self.user.is_support() or self.user.is_gestion()

    def can_assign_support(self) -> bool:
        return self.user.is_gestion()

    def can_delete_event(self) -> bool:
        return self.user.is_admin()

    def can_create_user(self) -> bool:
        return self.user.is_gestion()

    def can_update_user(self) -> bool:
        return self.user.is_gestion()

    def can_delete_user(self) -> bool:
        return self.user.is_gestion()