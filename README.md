first_time_permission_escalation
================================
簡介

1.快速整理內部PT的網址清單，
2.測試網址清單的連線狀況，
3.比較有和沒有輸入cookie的連線狀況

使用說明

python first_time_permission_escalation.py [-htrRxioc]
    -h, --help, read me and help you
    -t, --test_mode, default test 10 requests 是否只測10個網址
    -s, --skip_mode, default is disbaled 是否測試連線狀況
    -r, --local_path, example C:\dir\\ or /var/web/ ,default 
    -R, --url_path, default is http://test.com/
    -x, --exclude_file_type, default is jpg|JPG|gif|GIF|png|PNG|bmp|BMP|tif|TIF|js|css
    -i, --ifile, default is dir_list.txt
    -o, --ofile, default is result_20140101_1200.csv
    -c, --cookie_str, example "something=abc;anthoer=123", default is 
    
使用情境
1. 輸入 dir_list.txt 過濾不要的附檔名，並且將格式轉為http/https，不測試連線直接輸出網址清單
python first_time_permission_escalation.py -i "dir_list.txt" -x "jpg|GIF" -r "/var/" -R "http://google.com" -s


2. 輸入 dir_list.txt 過濾不要的附檔名，並且將格式轉為http/https，並測試前10個網址的連線狀況
python first_time_permission_escalation.py -i "dir_list.txt" -x "jpg|GIF" -r "/var/" -R "http://google.com" -t

3. 輸入 dir_list.txt 過濾不要的附檔名，並且將格式轉為http/https，並測試全部網址的連線狀況
python first_time_permission_escalation.py -i "dir_list.txt" -x "jpg|GIF" -r "/var/" -R "http://google.com"

4. 輸入 dir_list.txt 過濾不要的附檔名，並且將格式轉為http/https，並比較有設定cookie和沒有設定cookie連線狀況
python first_time_permission_escalation.py -i "dir_list.txt" -x "jpg|GIF" -r "/var/" -R "http://google.com" -c "jsessionid=test"
