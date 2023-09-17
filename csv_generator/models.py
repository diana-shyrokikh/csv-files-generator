from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


USERNAME_REGEX = r"^[a-z][a-z0-9]*$"
NAME_REGEX = r"^[a-zA-Z][a-zA-Z0-9\s]*$"


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, validators=[
        RegexValidator(
            regex=USERNAME_REGEX,
            message="Username should start with letter "
                    "and contains only letters and numbers",
            code="invalid_username"
        )
    ])

    def __str__(self):
        return self.username


class DataSchema(models.Model):
    title = models.CharField(max_length=255, validators=[
        RegexValidator(
            regex=NAME_REGEX,
            message="Title should start with letter "
                    "and contains only letters and numbers",
            code="invalid_title"
        )
    ])
    modified = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} user: {self.user}"

    class Meta:
        unique_together = [
            ["title", "user"],
        ]


class SchemaColumn(models.Model):
    TYPES = [
        ("Full name", "Full name"),
        ("Job", "Job"),
        ("Email", "Email"),
        ("Domain name", "Domain name"),
        ("Phone number", "Phone number"),
        ("Company name", "Company name"),
        ("Text", "Text"),
        ("Integer", "Integer"),
        ("Address", "Address"),
        ("Date", "Date"),
    ]

    name = models.CharField(max_length=255, validators=[
        RegexValidator(
            regex=NAME_REGEX,
            message="Column name should start with letter "
                    "and contains only letters and numbers",
            code="invalid_name"
        )
    ])
    type = models.CharField(choices=TYPES, max_length=255)
    order = models.IntegerField(validators=[MinValueValidator(limit_value=0)])
    schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)

    from_range = models.IntegerField(blank=True, null=True)
    to_range = models.IntegerField(blank=True, null=True)

    def validate_range(self):
        if not self.from_range:
            self.from_range = 1

        if not self.to_range:
            self.to_range = 2

        if self.from_range < 1:
            raise ValidationError({"from_range": "'From' field must be >= 1"})

        if self.to_range < self.from_range:
            raise ValidationError({"to_range": "'To' field must be >= 'From' field"})

        return True

    def clean(self):
        if self.type in ("Integer", "Text"):
            self.validate_range()

    def __str__(self):
        return f"{self.name} {self.type}"

    class Meta:
        unique_together = [
            ["order", "schema"],
            ["name", "type", "schema"],
        ]
