from logging import getLogger

import sib_api_v3_sdk as sib
from flask import current_app
from sib_api_v3_sdk.rest import ApiException

logger = getLogger(__name__)
# Configure the API with your API key
sib_configuration = sib.Configuration()
# The API key is saved in .secrets.tolm
sib_configuration.api_key['api-key'] = current_app.config.get("SIB_API_KEY")


def send_mail(to: str, subject: str, contents: str) -> None:
    """
    Sends an email using Brevo (earlier SendInBlue).

    Args:
        to: The email address to send the email to
        subject: The subject of the email
        contents: The html formatted email contents
    """

    # Create an instance of the API to send the emails
    api_instance = sib.TransactionalEmailsApi(sib.ApiClient(sib_configuration))
    # Create th email instance
    smtp_email = sib.SendSmtpEmail(
        to=[{"email": to}],
        html_content=contents,  # content in HTML
        sender={
            "name": "AlexBlog",
            "email": "<validated_sender_email>",  # I used my email address with which I signed up for Brevo
        },
        subject=subject
    )
    try:
        # Send the email instance to be emailed
        api_instance.send_transac_email(smtp_email)
        logger.debug(f"Confirmation email sent to {to}.")
    except ApiException as e:
        logger.exception("Exception sending email", exc_info=e)
