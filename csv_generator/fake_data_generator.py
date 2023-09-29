from faker import Faker


def get_fake_data(
        column_type,
        from_range=None,
        to_range=None
):
    fake = Faker()

    if column_type == "Integer":
        return get_fake_int(from_range, to_range)

    if column_type == "Text":
        return get_fake_text(from_range, to_range)

    fakers = {
        "Full name": fake.name,
        "Job": fake.job,
        "Email": fake.email,
        "Domain name": fake.domain_name,
        "Phone number": fake.phone_number,
        "Company name": fake.company,
        "Address": fake.address,
        "Date": fake.date,
    }

    return fakers[column_type]()


def get_fake_text(from_range=None, to_range=None):
    fake = Faker()
    return " ".join(
        fake.sentences(max(from_range, to_range))
    )


def get_fake_int(from_range=None, to_range=None):
    fake = Faker()
    return fake.random_int(
        min=from_range, max=to_range
    )


def write_rows(rows, columns, csv_writer):
    for _ in range(int(rows)):
        data = [
            {
                column.name:
                    get_fake_data(
                        column.type,
                        column.from_range,
                        column.to_range
                    )
                for column in columns
            }

        ]

        for row in data:
            csv_writer.writerow(row)
