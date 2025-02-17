# Proxy python

## 1. Decoder hexa data :

### Prérequis :
 ```sh
    pip3 install sys
    pip3 install socket
    pip3 install threading
  ```

### 1.1 Lancement du projet :

#### 1.1.1 Tester la fonction hexdump :
Lancer une session interactive avec Python :

```sh
    python3 -i proxy.py
  ```

Ensuite entrer la ligne suivant dans la session de Python :
```sh
    hexdump("Ceci est un test de proxy !")
  ```

On devrait voir les caractères en hexadécimal.

#### 1.1.2 Tester avec Netcat :

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

## 2. Tester avec un ftp :

### Prérequis :
 ```sh
    pip3 install pyftpdlib
  ```

### 2.1 Installer et lancer le serveur FTP en local :

#### 2.1.1 Lancer le serveur FTP sur le port 21 :
 ```sh
    python3 -m pyftpdlib --port 21 --user user --password pass
  ```

Cela démarre un serveur FTP local avec :

* Utilisateur : user
* Mot de passe : pass
* Port : 21

#### 2.1.2 Lancer le proxy pour intercepter le trafic FTP :
On doit maintenant exécuter notre proxy en l'écoutant sur un autre port (2121) et en redirigeant vers le serveur FTP (127.0.0.1:21).
 ```sh
    python3 proxy.py 127.0.0.1 2121 127.0.0.1 21 True
  ```

* 127.0.0.1 2121 → Proxy écoute sur ce port.
* 127.0.0.1 21 → Il redirige vers le vrai serveur FTP sur le port 21.
* True → Le proxy attend une réponse du serveur avant d’envoyer la requête.

Le proxy est maintenant en attente de connexions.

#### 2.1.3 Tester le proxy avec un client FTP :
Exécuter le fichier python "ftp_test.py"
 ```sh
    python3 ftp_test.py
  ```

#### 2.1.4 Vérifier le trafic intercepté :
Ca genre de résultat attendu :
 ```sh
    [*] Listening on 127.0.0.1:2121
> Received incoming connection from 127.0.0.1:64332
    0000 32 32 30 20 28 76 73 46 54 50 64 20 33 2E 30 2E  220 (vsFTPd 3.0.
0010 32 29 0D 0A                                      2)..
[<==] Sending 20 bytes to localhost.
[==>]Received 11 bytes from localhost.
0000 55 53 45 52 20 75 73 65 72 0D 0A                 USER user..
[==>] Sent to remote.
[<==] Received 34 bytes from remote.
0000 33 33 31 20 50 6C 65 61 73 65 20 73 70 65 63 69  331 Please speci
0010 66 79 20 74 68 65 20 70 61 73 73 77 6F 72 64 2E  fy the password.
0020 0D 0A                                            ..
[<==] Sent to localhost.
  ```