from models.db.connection import connectionDB

class UseNotesController:
   @staticmethod
   def getNotesHandler(userId, categoryId):
      allNotes = connectionDB('getNotes', {
         'categoryId': categoryId,
         'userId': userId
      })

      def noteFormated(data):
         return { 
            'id': data[0],
            'categoryId': data[1],
            'title': data[2],
            'summary': data[3],
            'content': data[4],
            'dateCreated': data[5],
            'lastModification': data[6]
         }

      allNotesFormated = list(map(noteFormated, allNotes))

      return allNotesFormated

   @staticmethod
   def createNoteHandler(userId, categoryId):

      noteDatas = connectionDB('insertNote', {
         'categoryId': categoryId,
         'userId': userId,
      })

      noteDataFormated = { 
         'id': noteDatas[0],
         'dateCreated': noteDatas[1],
         'lastModification': noteDatas[2] 
      }
      
      return noteDataFormated

   @staticmethod
   def deleteNoteHandler(noteId, categoryId, userId):
      connectionDB('deleteNote', {
         'noteId': noteId,
         'categoryId': categoryId,
         'userId': userId
      })

   @staticmethod
   def updateNoteHandler(userId, requestData):

      newLastModification = connectionDB('updateNote', {
         'noteId': requestData['noteId'],
         'categoryId': requestData['categoryId'],
         'userId': userId,
         'newTitle': requestData['newTitle'],
         'newContent': requestData['newContent'],
         'newSummary': requestData['newSummary'],
      })

      return newLastModification