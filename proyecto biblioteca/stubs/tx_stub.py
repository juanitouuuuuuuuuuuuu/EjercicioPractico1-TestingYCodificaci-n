class TxStub:
    def __init__(self, falla_commit=False, log=None):
        self.falla_commit = falla_commit
        self.log = log if log is not None else []

    def __enter__(self):
        self.log.append("BEGIN")
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.log.append("ROLLBACK")
            return False  # propaga la excepción
        if self.falla_commit:
            self.log.append("ROLLBACK")
            raise RuntimeError("Commit falló")
        self.log.append("COMMIT")
        return False
