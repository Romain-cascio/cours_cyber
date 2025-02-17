# Proxy python

## Prérequis :
 ```sh
    pip3 install sys
    pip3 install socket
    pip3 install threading
  ```

## Lancement du projet :

### Tester la fonction hexdump :
Lancer une session interactive avec Python :

```sh
    python3 -i proxy.py
  ```

Ensuite entrer la ligne suivant dans la session de Python :
```sh
    hexdump("Ceci est un test de proxy !")
  ```

On devrait voir les caractères en hexadécimal.

### Tester avec Netcat :

Lancer le proxy en écoutant sur 127.0.0.1:9000 et en redirigeant le trafic vers example.com:80 :
```sh
    python3 proxy.py 127.0.0.1 9000 example.com 80 True
  ```

Dans un autre terminal, se connecter au proxy avec Netcat :
```sh
    nc 127.0.0.1 9000
  ```

Ensuite, taper une requête HTTP simple :
```sh
    GET / HTTP/1.1
    Host: example.com
  ```

Deux fois sur Entrée et si tout fonctionne, on devrait voir la requête passer à travers le proxy. (terminal du lancement du proxy)
