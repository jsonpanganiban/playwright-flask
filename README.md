# CAR API

### Installation
```
pip install -r requirements.txt
```
### Endpoints

**/car/query**

*make only*
```
curl -iX GET "http://127.0.0.1:5001/car/query?make=ALFA+ROMEO"
```

*lot number details*
```
 curl -iX GET "http://127.0.0.1:5001/car/lot/40234580"
 ```