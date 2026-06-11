class Aluno:
    PUC_EMAIL_DOMAIN = "@aluno.puc-rio.br"

    def __init__(self, id: int, nome: str, email: str, senhaHash: str):
        self.__validaNome(nome)
        self.__validaEmail(email)

        self.id = id
        self.nome = nome
        self.email = email
        self.senhaHash = senhaHash

    def __validaNome(self, nome: str):
        if len(nome.strip()) < 3:
            raise ValueError("Nome inválido")

    def __validaEmail(self, email: str):
        email = email.strip().lower()

        if not email.endswith(self.PUC_EMAIL_DOMAIN):
            raise ValueError(
                "O email deve ser institucional da PUC-Rio"
            )