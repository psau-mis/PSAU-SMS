import json
import requests


class M360Request:
	"""
		m360 sms API integration.
	"""

	def __init__(self, app_key, app_secret, shortcode_mask):
		"""
			initialize m360 security
		"""
		self.app_key = app_key
		self.app_secret = app_secret
		self.shortcode_mask = shortcode_mask

	def send_sms(self, body, contact_no):
		"""
			for Outbound SMS
			return: JSON of request response
		"""
		payload = {
			"app_key": self.app_key,
			"app_secret": self.app_secret,
			"msisdn": contact_no,
			"content": body,
			"shortcode_mask": self.shortcode_mask,
			"is_intl": False
		}
		headers = {
			"accept": "application/json",
			"content-type": "application/json",
		}
		url = "https://api.m360.com.ph/v3/api/broadcast"
		response = requests.post(url, headers=headers, json=payload, timeout=60)
		# response.raise_for_status()
		response = json.loads(response.content)
		return response
