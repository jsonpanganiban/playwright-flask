CAR API
-----------------------
**Default Size**
Default size/number of items being returned from API is 100. It can be changed using values (20, 50, 100)
```
curl -iX GET "http://192.99.186.16/car/query?make=ALFA+ROMEO&size=20"
curl -iX GET "http://192.99.186.16/car/query?make=ALFA+ROMEO&size=50"
curl -iX GET "http://192.99.186.16/car/query?make=ALFA+ROMEO&size=100"
```

**Page Number**
Default page number is Page 1. To change page number, use sample page parameter below.
```
curl -iX GET "http://192.99.186.16/car/query?make=ALFA+ROMEO&page=2"
curl -iX GET "http://192.99.186.16/car/query?make=ALFA+ROMEO&page=3"
```

**/car/query**

*make only*
```
curl -iX GET "http://192.99.186.16/car/query?make=ALFA+ROMEO"
```

*model only*
```
curl -iX GET "http://192.99.186.16/car/query?model=CR-V+LX"
```

*make and model*
```
curl -iX GET "http://192.99.186.16/car/query?make=MITSUBISHI&model=LANCER+EVO"
```

*year/s*
```
curl -iX GET "http://192.99.186.16/car/query?year=1965"
curl -iX GET "http://192.99.186.16/car/query?year=2020&year=2019&year=2018"
```

*make, model, year/s*
```
curl -iX GET "http://192.99.186.16/car/query?make=AUDI&model=A3+PREMIUM&year=2020&year=2019"
```

*page, size (result per page)*
```
curl -iX GET "http://192.99.186.16/car/query?make=MITSUBISHI&model=LANCER+EVO"
curl -iX GET "http://192.99.186.16/car/query?make=AUDI&model=A3+PREMIUM&year=2020&year=2019"
```

*/car/query & per page*
```
curl -iX GET "http://192.99.186.16/car/query?make=MAZDA&model=CX-3+SPORT&year=2020&year=2019&page=1"
curl -iX GET "http://192.99.186.16/car/query?year=1964&year=1963&year=1962&page=2"
curl -iX GET "http://192.99.186.16/car/query?make=MITSUBISHI&model=LANCER+EVO&page=1"
```

**/car/lot/{lot_id}**
*returns car information via lot id*
```
curl -iX GET "http://192.99.186.16/car/lot/40234580"
```

**/car/member/lot/{lot_id}**
*returns complete car information via lot id*
```
curl -iX GET "http://192.99.186.16/car/member/lot/40234580"
```