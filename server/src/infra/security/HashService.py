from werkzeug.security import generate_password_hash, check_password_hash


class HashService:

    def hash(self, senha: str) -> str:
        return generate_password_hash(senha)

    def verificar(self, senha_hash: str, senha: str) -> bool:
        return check_password_hash(senha_hash, senha)
