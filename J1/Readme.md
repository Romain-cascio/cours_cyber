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
[*] Écoute sur 127.0.0.1:2121
[==>] Connexion entrante de 127.0.0.1:57720
[<==] Reçu 28 octets du serveur distant.
0000 32 32 30 20 70 79 66 74 70 64 6C 69 62 20 32 2E  220 pyftpdlib 2.
0010 30 2E 31 20 72 65 61 64 79 2E 0D 0A              0.1 ready...
[==>] Reçu 11 octets du client local.
0000 55 53 45 52 20 75 73 65 72 0D 0A                 USER user..
[==>] Envoyé au serveur distant.
[<==] Reçu 33 octets du serveur distant.
0000 33 33 31 20 55 73 65 72 6E 61 6D 65 20 6F 6B 2C  331 Username ok,
0010 20 73 65 6E 64 20 70 61 73 73 77 6F 72 64 2E 0D   send password..
0020 0A                                               .
[<==] Envoyé au client local.
[==>] Reçu 11 octets du client local.
0000 50 41 53 53 20 70 61 73 73 0D 0A                 PASS pass..
[==>] Envoyé au serveur distant.
[<==] Reçu 23 octets du serveur distant.
0000 32 33 30 20 4C 6F 67 69 6E 20 73 75 63 63 65 73  230 Login succes
0010 73 66 75 6C 2E 0D 0A                             sful...
[<==] Envoyé au client local.
[==>] Reçu 6 octets du client local.
0000 51 55 49 54 0D 0A                                QUIT..
[==>] Envoyé au serveur distant.
[<==] Reçu 14 octets du serveur distant.
0000 32 32 31 20 47 6F 6F 64 62 79 65 2E 0D 0A        221 Goodbye...
[<==] Envoyé au client local.
[*] Plus de données, fermeture des connexions.
  ```