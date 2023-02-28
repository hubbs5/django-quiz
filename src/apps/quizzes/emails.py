from django.core.mail import send_mail, mail_admins
from django.template.loader import render_to_string
from decouple import config
from hashlib import md5
from typing import Tuple
import requests
from collections.abc import Iterable

import mailchimp_marketing as mcm
from mailchimp_marketing.api_client import ApiClientError

from .models import Quiz

def _init_mailchimp_client():
  client = mcm.Client()
  client.set_config({
    'api_key': config('MAILCHIMP_API_KEY'),
    'server': config('MAILCHIMP_SERVER_PREFIX')
  })
  return client


def _update_list(client, email_hash, member_info, list_id):
  try:
    resp = client.lists.set_list_member(
      list_id, email_hash, member_info
    )
  except ApiClientError as e:
    return False, e.text

  return True, resp


def _clean_user_crm_data(email: str, first_name: str=None,
                         last_name: str=None, *args, **kwargs) -> dict:
  """
  Takes input from form and formats results for use in Mailchimp

  Args:
      email (str): _description_
      first_name (str, optional): _description_. Defaults to None.
      last_name (str, optional): _description_. Defaults to None.

  Returns:
      dict: _description_
  """
  data_dict = {}
  # Inputs from form are in lists
  if isinstance(email, Iterable):
    email = email[0]
  if isinstance(first_name, Iterable):
    first_name = first_name[0]
  if isinstance(last_name, Iterable):
    last_name = last_name[0]
  data_dict['email_address'] = email
  data_dict['FNAME'] = first_name if first_name is not None else ""
  data_dict['LNAME'] = last_name if last_name is not None else ""
  return data_dict


def add_mailchimp_user(user: dict, list_id: str, tags: dict={},
                       *args, **kwargs) -> Tuple[bool, requests.Response]:
  """
  Takes user info from form and adds the user to a Mailchimp marketing list.

  Args:
      user (dict): _description_
      list_id (str): _description_
      tags (dict, optional): _description_. Defaults to {}.

  Returns:
      Tuple[bool, requests.Response]: _description_
  """
  client = _init_mailchimp_client()
  user_data = _clean_user_crm_data(**user)
  email_address = user_data["email_address"]
  
  print(f"\nAdding to mailchimp: {email_address}\n")
  email_hash = md5(email_address.encode("utf-8")).hexdigest()
  member_info = {
      "email_address": email_address,
      "status": "subscribed",
      "FNAME": user_data["FNAME"],
      "LNAME": user_data["LNAME"]
  }
  
  sub_success, sub_text = _update_subscription_list(
      client, email_hash, member_info, list_id)
  
  if sub_success:
      tag_success, tag_text = _update_tags(client, email_hash, tags, 
                                          list_id)
      if tag_success == False:
          pass
  else:
      print(f"Failure Text:\n{sub_text}\n")


def _update_subscription_list(client, email_hash, member_info, list_id):
  try:
    resp = client.lists.set_list_member(
      list_id, email_hash, member_info
    )
  except ApiClientError as error:
    return False, error.text
  
  return True, resp


def _update_tags(client, email_hash, tags, list_id):
  try:    
    resp = client.lists.update_list_member_tags(
        list_id, email_hash, tags)
  except ApiClientError as error:
    return False, error.text
  
  return True, resp


def get_quiz_tags(model: Quiz) -> dict:
  """_summary_

  Args:
      model (Quiz): _description_

  Returns:
      dict: _description_
  """
  tags = {
    "tags": [
      {
        "name": "quiz-lead",
        "status": "active"
      },
      {
        "name": f"{model.quiz_name}",
        "status": "active"
      }
    ]
  }
  return tags