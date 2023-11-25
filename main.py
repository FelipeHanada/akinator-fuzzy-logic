from responses_sheet_handler import ResponsesSheetHandler
from app import App
from fuzzynator.fuzzynator import Fuzzynator

if __name__ == '__main__':
    responses_sheet_handler = ResponsesSheetHandler()

    fuzzynator = Fuzzynator(responses_sheet_handler, talkative=True)

    app = App(responses_sheet_handler, fuzzynator)
    app.mainloop()
