
class Questions(object):

	Qs_museums = ['When was the museum established?','What are the opening days of the museum?','What are the visiting hours?','What is the entry fee?','What is the average tour duration?','What are the facilities available?','Who manages the museum?','Is docent guide available?','What is the language?','What is contact email?','What is contact phone?','Which is the website?']
	Qs_temples = ['Where is temple located?', 'Where is the temple situated?', 'The temple is dedicated to whom?', 'Who is the diety?','When was the temple built?','What are the darshan hours?','What is the average darshan duration?','What are the facilities available?','Who manages the temple?','What is the language?','What is contact email?','What is contact phone?','What is the website?']
	Qs_loc = ['Where is temple located?', 'Where is the temple situated?', 'Where does this temple exist?']# 1 #
	Qs_diety = ['The temple is dedicated to whom?', 'Who is the diety?', 'Which god lives here?'] # 2 #
	Qs_age = ['When was the temple built?', 'Which period does the temple belong?'] #'Whatat is the age of the building?'] # 3 #
	#Festival info #Puja timing, Darshan hours Qs_timing 
	Qs_festival = ['What are the visiting hours?', 'When is the temple open?', 'What is the timings?' ] # 4 #
	#Prominent people associated with the temple
	Qs_people = ['Who built the temple?'] # 5 #
	#trivia, Legend, Beliefs, Interesting facts about a temple, 
	Qs_trivia = ['What is the legend?'] # 6 #
	Qs_manage = ['Who manages the temple?', 'Who overlooks temple administration?'] # 7 #
	Qs_language = ['What is the language?'] # 8 #
	Qs_address = ['What is the email?','What is the mobile or phone number?','Is there a website?','Whom to contact for more information?'] # 9 #

	temple_fact_mapping = [[0,1,2],[3,4,5],[6,7],[8,9,10],[11],[12],[13,14],[15],[16,17,18, 19]] ##temple-improved
	temple_facts = ['Location' , 'Diety', 'Age', 'Festival', 'Key-people', 'Trivia', 'Managed-by', 'Language', 'Address']

	def __init__(self, domain:str):
		self.domain = domain

	def __call__(self):
		self.fetchQs()

	def fetchQs(self):
		Qs = []
		if self.domain == 'temple':
			Qs = self.Qs_loc + self.Qs_diety + self.Qs_age + self.Qs_festival + self.Qs_people + self.Qs_trivia + self.Qs_manage + self.Qs_language + self.Qs_address # # # # # 
		elif self.domain == 'museum':
			Qs = self.Qs_museums
		return Qs

def main():
	domain = 'temple'
	questions = Questions(domain)
	print(questions.temple_fact_mapping)

if __name__ == '__main__':
    main()
