from pywinauto import application, timings

import time
import os

app = application.Application()
app.start('C:\Kiwoom\KiwoomFlash2\khministarter.exe')

title = '번개 Login'
dlg = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

pass_ctrl = dlg.Edit2
pass_ctrl.SetFocus()
pass_ctrl.TypeKeys('')

cert_ctrl = dlg.Edit3
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys('')

btn_ctrl = dlg.Button0
btn_ctrl.Click()

time.sleep(50)

os.system('taskkill /im khmini.exe')