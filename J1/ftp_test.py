import ftplib

def ftp_connect():
    ftp = ftplib.FTP()
    ftp.connect('127.0.0.1', 2121)  # Se connecter via le proxy
    ftp.login('user', 'pass')  # Se connecter avec les identifiants
    print(ftp.getwelcome())  # Afficher le message de bienvenue du serveur FTP
    ftp.quit()

if __name__ == "__main__":
    ftp_connect()
