import SpeechControl as SC
import KnowledgeControl as KC
import apiai


class RequestController:

    def __init__(self):
        self.aiToken = '786ff37f7053431bb6ef050394521fcd'  # API.ai token
        self.ai = apiai.ApiAI(self.aiToken)

    def handle_request(self, txt):
        request = self.ai.text_request()
        request.lang = 'en'
        request.session_id = 's1'

        request.query = txt

        response = request.getresponse()
        x = str(response.read())

        output = ''

        ### Convert byte code into dict ###

        try:
            x = x.replace('false', 'False')
            x = x.replace('true', 'True')
            output = eval(eval(x))
        except NameError:
            print('Error in API response')

        print(output)

       

        return output
