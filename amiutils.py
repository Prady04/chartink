import os
import win32com.client
import pythoncom
import glob
from win32com.client import Dispatch
import logging



imp_tbl = [
    {'db': "C:\\Program Files\\AmiBroker\\Databases\\stockD",
    'data': "C:\\tradedb\\*.txt",
    'format': "nsepy.format"},]
    
def import_data():
    ab = win32com.client.Dispatch('Broker.Application', pythoncom.CoInitialize())
    ab.Visible = True
    for l in imp_tbl:
        logging.debug("Loading database {}".format(os.path.split(l['db'])[1]))
        print("Loading database {}".format(os.path.split(l['db'])[1]))
        print(ab.LoadDatabase(l['db']))
        f_lst = sorted(set(glob.glob(l['data'])))
        for f in f_lst:
            try:
                print("Importing datafile {}, using format {}".format(f, l['format']))
                ab.Import(0, f, l['format'])               
               
            except e:
                print("Error importing datafile {}".format(f))
            else:
                (newpath, filename) = os.path.split(f)
                try:
                    dest = os.path.join(newpath, "archive", filename)
                    if(os.path.exists(dest)):
                        os.remove(dest)
                    os.rename(f, os.path.join(newpath, "archive", filename))
                    print("Import complete")
                except Exception as e:
                    print(r'Errror archiving datafile {}'.format(e)) 
                    pass


        print("Saving Db")        
        ab.SaveDatabase()
        ab.RefreshAll()
        ab.Quit()
        print("Done..")