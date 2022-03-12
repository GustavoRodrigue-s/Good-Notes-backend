class App:
   def __init__(self):
      self.name = "Good Notes"

   @staticmethod
   def checkRegistrationErrors(user, usersDatabase):
      wrongInputs = []

      inputsArray = [
         { 'name': 'input-username', "value": user.username },
         { 'name': 'input-email', "value": user.email },
         { 'name': 'inputs-passwords', "value": user.password[0] },
         { 'name': 'inputs-passwords', "value": user.password[1] }
      ]

      for input in inputsArray:
         if input["value"] == '':
            wrongInputs.append({'input': input['name'], "reason": "empty input"})

      if usersDatabase['hasUserWithSomeUsername']: 
         wrongInputs.append({'input': 'input-username', "reason": "username already exists"})

      if usersDatabase['hasUserWithSomeEmail']:
         wrongInputs.append({'input': 'input-email', "reason": "email already exists"})

      if user.password[0] and user.password[1] and user.password[0] != user.password[1]:
         wrongInputs.append({'input': 'inputs-passwords', "reason": "differents passwords"})
         

      if wrongInputs != []: raise Exception(wrongInputs)

   @staticmethod
   def checkLoginErrors(user, userDatabase):

      wrongInputs = []

      inputsArray = [
         { 'name': 'input-email', "value": user.email },
         { 'name': 'input-password', "value": user.password }
      ]

      for input in inputsArray:
         if input["value"] == '':
            wrongInputs.append({'input': input['name'], "reason": "empty input"})

      if user.email and user.password:
         if not userDatabase:
            wrongInputs.append({'input': 'some', "reason": "wrong credentials"})


      if wrongInputs != []: raise Exception(wrongInputs)

   @staticmethod
   def checkNewCredentials(user, hasUserWithSomeCredentials):
      wrongValues = []

      if user['email'] == '':
         wrongValues.append({'input': 'input-email', 'reason': 'empty input'})

      if user['username'] == '':
         wrongValues.append({'input': 'input-username', 'reason': 'empty input'})

      if hasUserWithSomeCredentials['hasUserWithSomeEmail']:
         wrongValues.append({'input': 'input-email', 'reason': 'email already exists'})

      if hasUserWithSomeCredentials['hasUserWithSomeUsername']:
         wrongValues.append({'input': 'input-username', 'reason': 'username already exists'})


      if wrongValues != []: raise Exception(wrongValues)