from typing import Union

from openpyxl.workbook import Workbook

from tgbot.models.models import DrawMember


class BaseExcelManager(Workbook):

    def __init__(self, coordinates: dict):
        super(BaseExcelManager, self).__init__()
        self.sheet = self.active
        self.__configure_columns(coordinates)

    def __configure_columns(self, coordinates: dict) -> None:

        for column, value in coordinates.items():
            self.sheet[column] = value

    def insert_data(self, data_list: Union[list, tuple], file_path: str):
        """This method should be overwritten"""
        raise NotImplementedError

    def save_and_close(self, file_path: str) -> None:

        self.save(file_path)
        self.close()


class DrawMembersList(BaseExcelManager):

    def __init__(self, coordinates: dict):
        super().__init__(coordinates)

    def insert_data(self, data_list: Union[list, tuple], file_path: str):
        row = 2
        for info in data_list:
            self.sheet[row][1].value = info["phone_number"]
            self.sheet[row][2].value = info["tg_id"]
            self.sheet[row][4].value = info["tg_username"]
            row += 1
        self.save_and_close(file_path)
