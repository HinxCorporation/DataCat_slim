# Data Cat



## how to use 

### for example , using ps

step . 1 , create venv

```powershell
python -m venv venv
```

step . 2 active env 

```
# for ps is 
.\venv\Scripts\Activate.ps1
# for linux is
source venv/bin/activate
```

step .3 . install requirements

```
pip install -r requirements.txt
```

step 4. run main in venv

```
python ./main.py
```



### setup dir list



| type         | desc               | supported |
| ------------ | ------------------ | --------- |
| relative     | ./folderA          | YES       |
| goto         | ../../folderb      | YES       |
| unix         | /dir/volume/folder | YES       |
| drive letter | D:\folder          | YES       |

```
# example for folder_paths.txt
F:\Root\volume-workbench\Python
Q:\BaiduNetdisk
```





### Test


![Test Result](https://github.com/HinxCorporation/DataCat_slim/raw/main/readme.assets/image-20230928165425256.png)
