"""Office automation through win32com.
Works without admin because it just talks to the running app over COM."""
import win32com.client as win32

def _excel():  return win32.Dispatch("Excel.Application")
def _ppt():    return win32.Dispatch("PowerPoint.Application")
def _outlook():return win32.Dispatch("Outlook.Application")

# --- Excel --------------------------------------------------------------
def excel_new_workbook():
    app = _excel(); app.Visible = True; app.Workbooks.Add()

def excel_save():
    try:    _excel().ActiveWorkbook.Save()
    except: pass

def excel_write_cell(cell, value):
    app = _excel()
    app.ActiveSheet.Range(cell).Value = value

# --- PowerPoint ---------------------------------------------------------
def ppt_new_presentation():
    app = _ppt(); app.Visible = True
    app.Presentations.Add()

def ppt_next_slide():
    try:    _ppt().SlideShowWindows(1).View.Next()
    except: pass

def ppt_previous_slide():
    try:    _ppt().SlideShowWindows(1).View.Previous()
    except: pass

def ppt_start_slideshow():
    try:    _ppt().ActivePresentation.SlideShowSettings.Run()
    except: pass

# --- Outlook ------------------------------------------------------------
def outlook_new_mail(to="", subject="", body=""):
    app = _outlook()
    mail = app.CreateItem(0)
    mail.To = to
    mail.Subject = subject
    mail.Body = body
    mail.Display()

def outlook_open_inbox():
    app = _outlook()
    ns = app.GetNamespace("MAPI")
    ns.GetDefaultFolder(6).Display()   # 6 == olFolderInbox