from dataclasses import dataclass, fields


@dataclass
class Cast:
    id: int
    gender: int
    popularity: float

    @classmethod
    def from_dict(cls, dict_):
        class_fields = [field.name for field in fields(cls)]
        return cls(**{k: v for k, v in dict_.items() if k in class_fields})
