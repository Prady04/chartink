import requests
import threading
import perfcounters
import time 
import webbrowser

urls = ["http://localhost:5000/bullrun", "http://localhost:5000/bulle", "http://localhost:5000/beare"]

def fetch_url(url):
    response = requests.get(url)
    if response.status_code == 200:
      '''html_content = response.text
      threadid = threading.currentThread().ident
      #print(html_content)
      filename = f'{threadid}.html'
      with open( filename, "w") as file:
        file.write(html_content)

      
      webbrowser.open(filename)'''
    else:
      print("Request failed with status code:", response.status_code)
      
if __name__=="__main__":
  while True:
    threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
    perf = perfcounters.PerfCounters()
    perf.start('starting thread')
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    perf.stop('starting thread')
    perf.report()
    print('waiting for 5 minutes')
    time.sleep(5*60)
  