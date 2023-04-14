from django.core.mail import send_mail
from django.template.loader import render_to_string
from decouple import config
from hashlib import md5
import mailchimp_marketing as mcm
from mailchimp_marketing.api_client import ApiClientError

LIST_ID = config('MAILCHIMP_LIST_ID')

def _init_mailchimp_client():
  """
  Initialize the Mailchimp API Client
  """
  client = mcm.Client()
  client.set_config({
    'api_key': config('MAILCHIMP_API_KEY'),
    'server': config('MAILCHIMP_SERVER_PREFIX')
  })
  return client


def add_user_to_mailchimp(request):
  client = _init_mailchimp_client()
  email_hash = md5(request['email'].lower().encode('utf-8')).hexdigest()
  member_info = {
    'email_address': request['email'],
    'status': 'subscribed',
    'FNAME': request['first_name'],
    'LNAME': request['last_name']
  }

  # Add user to list
  try:
    resp = client.lists.set_list_member(
      LIST_ID, email_hash, member_info
    )
  except ApiClientError as error:
    return False, error.text

  # Update user tags
  try:
    resp = client.lists.update_list_member_tags(
      LIST_ID, email_hash, request['tag']
    )
  except ApiClientError as error:
    return False, error.text

  return True, resp
  

def send_results_email(request):
    """
    Sends email with results.
    """
    email = request['email']
    msg_plain = render_to_string(f"quizzes/email.txt", request)
    msg_html = render_to_string(f"quizzes/email.html", request)

    send_mail(
        subject="Your Results are Inside!",
        message=msg_plain,
        from_email="djangodev.welcome <welcome@djangodev.io>",
        recipient_list=[email],
        fail_silently=True,
        html_message=msg_html
    )