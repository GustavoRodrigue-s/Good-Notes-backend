from flask import request, json, jsonify

import sys

sys.path.insert(1, './src')

from app.controllers import sessionController
from app.controllers import formsController
from app.controllers import categoryController
from app.controllers.UseNotesController import UseNotesController

from decorators import jwt_required, apiKey_required

def createRoutes(app):
   @app.route('/login', methods=['POST'])
   def routeLogin():
      requestData = json.loads(request.data)

      try:
         formsController.loginFormHandler(requestData)

         sessionData = sessionController.createSessionHandler(requestData)

         return jsonify(
            {
               "state": "success",
               "reason": "all right",
               "userData": sessionData
            }, 200
         )
      except Exception as e:
         respData = [e.args[0]] if type(e.args[0]) != list else e.args[0]

         return jsonify({"errors": respData, "state": "error"}, 401)

   @app.route('/register', methods=['POST'])
   def routeRegister():
      requestData = json.loads(request.data)

      try:
         formsController.registerFormHandler(requestData)

         sessionData = sessionController.createSessionHandler(requestData)

         return jsonify(
            {
               "state": "success",
               "reason": "all right",
               "userData": sessionData
            }, 200
         )
      except Exception as e:
         respData = [e.args[0]] if type(e.args[0]) != list else e.args[0]

         return jsonify({"errors": respData, "state": "error"}, 401)

   @app.route('/auth', methods=['GET'])
   @apiKey_required
   @jwt_required
   def routeTokenRequired(userId):

      return jsonify({ "state": "authorized" }, 200)

   @app.route('/logout', methods=['GET'])
   @apiKey_required
   @jwt_required
   def routeLogoutUser(userId):
      sessionController.disableSessionHandler(userId)

      return jsonify({ 'state': 'success' }, 200)

   @app.route('/getCredentials', methods=['GET'])
   @apiKey_required
   @jwt_required
   def routeGetData(userId):
      try:
         userCredentials = sessionController.getSessionCredentialsHandler(userId)

         return jsonify(
            { 'state': 'success' ,'username': userCredentials[1], 'email': userCredentials[2] }, 200
         )
      except:
         return jsonify({ "state": "unauthorized" }, 401)

   @app.route('/updateCredentials', methods=['POST'])
   @apiKey_required
   @jwt_required
   def routeUpdateCredentials(userId):

      requestData = json.loads(request.data)

      try: 
         response = sessionController.updateSessionCredentialsHandler(userId, requestData)

         return jsonify({
            'state': 'success',
            'newDatas': response
         }, 200)

      except Exception as e:
         respData = [e.args[0]] if type(e.args[0]) != list else e.args[0]

         return jsonify({'state': 'error', 'reason': respData}, 403)

   @app.route('/deleteAccountap', methods=['GET'])
   @apiKey_required
   def routeDeleteAccount(userId):
      try:
         sessionController.deleteSessionHandler(userId)

         return jsonify({'state': 'success'}, 200)
      except Exception as e:
         return jsonify({'state': 'error', 'reason': f'{e}'}, 401)

   # ----- Endpoints Categorys ------

   @app.route('/addCategory', methods=['POST'])
   @apiKey_required
   @jwt_required
   def routeAddCategory(userId):
      requestData = json.loads(request.data)

      try:
         categoryName = requestData['categoryName']

         categoryId = categoryController.createCategoryHandler(userId, categoryName)

         return jsonify({'state': 'success', 'categoryId': categoryId}, 200)
      except Exception as e:
         return jsonify({'state': 'error', 'reason': 'no category name'}, 401)

   @app.route('/deleteCategory', methods=['POST'])
   @apiKey_required
   @jwt_required
   def routeDeleteCategory(userId):
      requestData = json.loads(request.data)

      try:
         categoryId = requestData['categoryId']

         categoryController.deleteCategoryHandler(userId, categoryId)

         return jsonify({'state': 'success'}, 200)
      except Exception as e:
         return jsonify({'state': 'error', 'reason': 'no category id'}, 401)

   @app.route('/updateCategory', methods=['POST'])
   @apiKey_required
   @jwt_required
   def routeUpdateCategory(userId):
      requestData = json.loads(request.data)

      try:
         categoryController.updateCategoryHandler(userId, requestData)

         return jsonify({'state': 'success'}, 200)
      except Exception as e:
         return jsonify({'state': 'error', 'reason': 'no category id or new category name'}, 401)

   @app.route('/getCategories', methods=['GET'])
   @apiKey_required
   @jwt_required
   def routeGetCategories(userId):
      try:
         allCategories =  categoryController.getCategoriesHandler(userId)

         return jsonify({ 'state': 'success', 'categories': allCategories }, 200)
      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)
      
   # ----- Endpoints Notes ------

   @app.route('/getNotes', methods=['POST'])
   @apiKey_required
   @jwt_required
   def routeGetNotes(userId):
      requestData = json.loads(request.data)

      try:
         categoryId = requestData['categoryId']

         allNotes = UseNotesController.getNotesHandler(userId, categoryId)

         return jsonify({ 'state': 'success', 'notes': allNotes }, 200)
      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   @app.route('/addNote', methods=['POST'])
   @apiKey_required
   @jwt_required
   def routeAddNote(userId):
      requestData = json.loads(request.data)

      try:
         currentCategoryId = requestData['categoryId']

         noteDatas = UseNotesController.createNoteHandler(userId, currentCategoryId)

         return jsonify({ 'state': 'success', 'noteData': noteDatas }, 200)
      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   @app.route('/deleteNote', methods=['POST'])
   @apiKey_required
   @jwt_required
   def routeDeleteNote(userId):
      requestData = json.loads(request.data)

      try:
         noteId = requestData['noteId']
         categoryId = requestData['categoryId']

         UseNotesController.deleteNoteHandler(noteId, categoryId, userId)

         return jsonify({ 'state': 'success' }, 200)
      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)

   @app.route('/updateNote', methods=['POST'])
   @apiKey_required
   @jwt_required
   def routeUpdateNote(userId):
      requestData = json.loads(request.data)

      try:
         lastModification = UseNotesController.updateNoteHandler(userId, requestData)

         return jsonify({ 'state': 'success', 'lastModification': lastModification }, 200)
      except Exception as e:
         return jsonify({ 'state': 'error', 'reason': f'{e}' }, 401)