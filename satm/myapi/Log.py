from .models import Log

class LogRecord:

    @staticmethod
    def save(action, payload, response):
        try:
            newLog = Log()
            newLog.ACTION = action
            newLog.PAYLOAD = payload
            newLog.RESPONSE = response

            newLog.save()
        except Exception as ex:
            print(str(ex))
            raise