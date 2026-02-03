import json
import os
from dataclasses import dataclass
from typing import Any


@dataclass
class RequestPolicy:
    user: dict
    ressource: str
    action: str
    context: Any | None = None


class UserPolicy:
    """
    Policy object for permission user
    Request : RequestPolicy object
    """
    def __init__(self, request: RequestPolicy):

        self.permission = self.get_permission()
        self.request = request

    def get_permission(self) -> dict:
        """ Get json file permission """
        dir_path = os.path.dirname(__file__)
        path = os.path.join(dir_path, 'permission.json')

        try:
            with open(path) as json_file:
                permission = json.load(json_file)
                return permission
        except FileNotFoundError:
            raise FileNotFoundError('Fichier de permission non trouvé')

    def is_allowed(self) -> bool:
        """
        Check if user is allowed
        rule => "role", "action", "context"
        :return true | false
        """
        rule = (
            self.permission
            .get(self.request.user["user_current_role"].value, {})
            .get(self.request.ressource, {})
            .get(self.request.action, None)
        )

        match rule:
            case None : return False
            case "*" : return True
            case dict() if len(rule) == 0 : return True
            case _ : return self.evaluation_context(rule)


    def evaluation_context(self, rule):
        """ Evaluation rule context in json permission"""
        for key, value in rule.items():
            condition = getattr(self.request.context, key)
            expected = self.request.user.get(value)
            if expected != condition:
                print("evaluation context invalide")
                return False
        print("evaluation context")
        return True
