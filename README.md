first_time_permission_escalation
================================
簡介

1.單純整理網址清單，替換目錄關鍵字，過濾不重要的檔案。
  dir_list.py dir_list.txt -p "/var/web/" -u "http://test.com/" -s
2.測試網址清單的連線狀況。
  dir_list.py dir_list.txt -p "/var/web/" -u "http://test.com/" -d
3.比較有輸入和未輸入cookie的連線結果。
  dir_list.py dir_list.txt -p "/var/web/" -u "http://test.com/" -c "jessionid=xoxo"

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o  --out=OUT         output csv(default: dir_list_20150325_1657.csv)
  -d, --demo            50 reuqest (default: disable)
  -s, --skip            replace keyword only, no request  (default: disable)
  -p  --path=PATH       path keyword C:\dir\ or /var/web/
  -u  --url=URL         target url http://test.com/
  -e  --exclu=EXCLU
                        exclude file type(default:jpg|JPG|gif|GIF|png|PNG|bmp|BMP|tif|TIF|css)
  -c  --coo=COO         permission escalation need cookie
