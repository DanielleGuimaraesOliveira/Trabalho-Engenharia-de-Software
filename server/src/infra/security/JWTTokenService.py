import jwt
from datetime import datetime, timedelta, timezone


class JWTTokenService:
    SECRET_KEY = "segredo"

    def gerar_token(self, aluno_id: int) -> str:
        payload = {
            "sub": aluno_id,
            "exp": datetime.now(timezone.utc) + timedelta(hours=2)
        }

        return jwt.encode(payload,
            self.SECRET_KEY,
            algorithm="HS256"
        )
    
    def decodifica_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])

            return int(payload["sub"])

        except jwt.ExpiredSignatureError:
            raise Exception("Token expirado")
 
        except jwt.InvalidTokenError:
            raise Exception("Token inválido")