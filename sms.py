#!flask/bin/python
from twilio.rest import TwilioRestClient
import schedule
import time

class sms_handler:
	def __init__(self,to_number,med_name):
		self.to_number=to_number
		self.med_name=med_name
	def send_sms(self):
		twilio_account={'account_sid':'AC4a583233d431f798bc9245562cd72ff5','auth_token':'9792e9a53f3fc3f0b5cdd8eb3cba041c'}
		client = TwilioRestClient(twilio_account['account_sid'], twilio_account['auth_token'])
		message = client.messages.create(to=self.to_number, from_="+12018028495",body=self.med_name)

	def automate(self):
		schedule.every().day.at("19:51").do(self.send_sms)
		while True:
			schedule.run_pending()
			time.sleep(1)
tsws=sms_handler("+918277126791","Aspirin due in an hour")
tsws.automate();