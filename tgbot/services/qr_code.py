from typing import Union

from qrcode import QRCode
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


class QrGenerator(QRCode):

    def __init__(self, data: Union[str, int], file_path: str):
        self.data = str(data)
        self.qr_path = file_path
        super().__init__(
            version=1,
            box_size=10,
            border=5,
        )

    def generate_and_save_qr(self) -> str:
        self.add_data(self.data)
        self.make(fit=True)
        img = self.make_image(fill_color='black',
                              back_color='white',
                              module_drawer=RoundedModuleDrawer())
        img.save(self.qr_path)
        return self.qr_path
