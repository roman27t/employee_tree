from dataclasses import dataclass


@dataclass(frozen=True)
class RequestFormat:
    html: str = 'html'
    value: str = '1'

    @property
    def param_encode(self) -> str:
        return f'{self.html}={self.value}'
