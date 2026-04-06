from datetime import date


def normalize_addresses(value: str) -> str:
   """
   Возвращает значение, в котором адрес приведен к нижнему регистру и очищен от пробелов по краям.
   """
   return value.strip().lower()



def add_short_body(email: dict) -> dict:
    """
       Возвращает email с новым ключом email["short_body"] —
       первые 10 символов тела письма + "...".
       """
    email["short_body"] = email["message"][0:10] + "... "


    return email


def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    cleaned_body = body.replace('\t', ' ').replace('\n', ' ')
    while '  ' in cleaned_body:
        cleaned_body = cleaned_body.replace('  ', ' ')
    return cleaned_body.strip()



def build_sent_text(email: dict) -> str:
    """
        Формирует текст письма в формате:

        Кому: {to}, от {from}
        Тема: {subject}, дата {date}
        {clean_body}
        """

    send_text = (f"Кому: {email['recipient']}, от {email['sender']}\n"
                 f"Тема: {email['subject']}, дата {email['date']}\n"
                 f"{email['short_body']}")
    return send_text



def check_empty_fields(subject: str, body: str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True, если поле пустое.
    """
    is_subject_empty = not subject or not subject.strip()
    is_body_empty = not body or not body.strip()

    return (is_subject_empty, is_body_empty)





def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
    masked_from = login[0:2] + "***@" + domain
    return masked_from



def get_correct_email(email_list: list[str]) -> list[str]:
    """
    Возвращает список корректных email.
    """
    valid_domains = {'.com', '.ru', '.net'}
    correct_emails = []
    for email in email_list:
        if '@' not in email:
            continue
            domain_part = email.split('@')[-1]
        if not domain_part:
            continue
        if any(email.endswith(domain) for domain in valid_domains):
            correct_emails.append(email)
        return correct_emails


    def create_email(sender: str, recipient: str, subject: str, massage: str) -> dict:
        """
        Создает словарь email с базовыми полями:
        'sender', 'recipient', 'subject', 'body'
        """
        email = {"sender": sender, "recipient": recipient, "subject": subject, "massage": massage}
        return email


    def add_send_date(email: dict) -> dict:
        """
        Возвращает email с добавленным ключом email["date"] — текущая дата в формате YYYY-MM-DD."""
        email["date"] = str(date.today())
        return email

    def extract_login_domain(address: str) -> tuple[str, str]:
        """
        Возвращает логин и домен отправителя.
        Пример: "user@mail.ru" -> ("user", "mail.ru")
        """
        login = address.split('@')[0]
        domain = address.split('@')[1]
        return (login, domain)


    def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[
        dict]:
        if not recipient_list:  # проверяем что recipient_list не пустой
            return []
        correct_recipients = get_correct_email(recipient_list)
        correct_sender = get_correct_email([sender])
        if not correct_recipients or not correct_sender:  # Проверяем корректность recipient_list и sender
            return []
        is_subject_empty, is_body_empty = check_empty_fields(subject, message)
        if is_subject_empty or is_body_empty:  # проверяем пустоту тема и тела текста
            return []
        filtered_recipients = [
            recipient for recipient in correct_recipients  # Проверяем отправку самому себе
            if normalize_addresses(recipient) != normalize_addresses(sender)
        ]
        if not filtered_recipients:
            return []
        normalized_subject = clean_body_text(subject)  # Нормализуем subject
        normalized_message = clean_body_text(message)  # Нормализуем massage
        normalized_sender = normalize_addresses(sender)  # Нормализуем sender
        sent_emails = []
        for recipient in filtered_recipients:
            normalized_recipient = normalize_addresses(recipient)  # Создаём базовое письмо для каждого получателя

            email = create_email(normalized_sender, normalized_recipient, normalized_subject, normalized_message)
            email = add_send_date(email)

            login, domain = extract_login_domain(normalized_sender)
            masked_from = mask_sender_email(login, domain)
            email["sender"] = masked_from

            add_short_body(email)

            email["sent_text"] = build_sent_text(email)

            sent_emails.append(email)

        return sent_emails

    emails = sender_email(
        recipient_list=["user1@example.com", "user2@gmail.ru", "default@study.com"],
        subject="Тема сообщения",
        message="Привет!Это моё сообщение.",
    )

    for email in emails:
        print(email["sent_text"])
