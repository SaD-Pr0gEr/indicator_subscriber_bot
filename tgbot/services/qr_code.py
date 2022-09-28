import qrcode
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

data = "GeeksforGeekdasdasdasdasdasdasdasdasds"

qr = qrcode.QRCode(version=1,
                   box_size=10,
                   border=5)

qr.add_data(data)

qr.make(fit=True)
img = qr.make_image(fill_color='black',
                    back_color='white',
                    module_drawer=RoundedModuleDrawer())

img.save('MyQRCode2.png')
